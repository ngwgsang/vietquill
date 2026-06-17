import sys
import os
import random
import time

# Add project root to sys.path to allow imports from src
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import uvicorn
from src.utils.estimators import QCModelEstimator
from src.utils.quality_evaluator import QualityEvaluator

# FLAG để chuyển đổi giữa mô hình thật và mock (để test UI nhanh)
_USE_MOCK = False

class MockParaphraser:
    def __init__(self):
        print("[MOCK] Initializing Mock Paraphraser...")
        
    def generate(self, text, num_candidates=4, **kwargs):
        # Tạo ra các câu giả lập bằng cách xáo trộn hoặc thay đổi nhẹ câu gốc
        words = text.split()
        candidates = []
        for i in range(num_candidates):
            random.shuffle(words)
            candidates.append(" ".join(words) + f" (Mock variant {i+1})")
        return candidates

class MockEstimator:
    def __init__(self):
        print("[MOCK] Initializing Mock Estimator...")
        
    def estimate(self, source, candidate):
        return {
            "lexical_score": round(random.uniform(40, 95), 2),
            "syntactic_score": round(random.uniform(40, 95), 2),
            "semantic_score": round(random.uniform(40, 95), 2),
        }

class MockQualityEvaluator:
    def __init__(self):
        print("[MOCK] Initializing Mock Quality Evaluator...")
        
    def evaluate(self, source, candidate):
        return {
            "bleu": round(random.uniform(30, 90), 2),
            "bertscore": round(random.uniform(70, 98), 2),
            "jaccard_diversity": round(random.uniform(10, 60), 2),
            "ted": round(random.uniform(20, 80), 2),
            "parascore": round(random.uniform(50, 95), 2)
        }

app = FastAPI(title="VietQuill Paraphrase API", description="API demo cho task paraphrase sử dụng mô hình vietquill-vit5-base-viqp-3e5 và velectra-base-qc-question-3e5")

# ... (CORS configuration remains same)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tên mô hình (Sử dụng đường dẫn local)
PARAPHRASER_MODEL = os.path.join(root_path, "models", "vietquill-vit5-base-viqp-3e5")
ESTIMATOR_MODEL = os.path.join(root_path, "models", "velectra-base-qc-question-3e5")

# Biến toàn cục cho model, tokenizer và estimator
tokenizer = None
model = None
device = None
estimator = None
quality_evaluator = None

class ParaphraseRequest(BaseModel):
    text: str
    num_candidates: int = 4
    num_beams: int = 5
    semantic: int = 50
    syntactic: int = 50
    lexical: int = 50

class TreeRequest(BaseModel):
    original: str
    paraphrase: str

@app.on_event("startup")
async def startup_event():
    global tokenizer, model, device, estimator, quality_evaluator
    print("\n" + "="*50)
    print(f"KHỞI TẠO HỆ THỐNG VIETQUILL {'(MOCK MODE)' if _USE_MOCK else ''}")
    print("="*50)
    
    if _USE_MOCK:
        device = "cpu"
        model = MockParaphraser()
        estimator = MockEstimator()
        quality_evaluator = MockQualityEvaluator()
        print("[OK] Đã khởi tạo Mock Components.")
        return

    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"[*] Thiết bị sử dụng: {device.upper()}")
        
        # Load Paraphraser
        print(f"[*] Đang tải Paraphraser từ: {PARAPHRASER_MODEL}...")
        tokenizer = AutoTokenizer.from_pretrained(PARAPHRASER_MODEL)
        model = AutoModelForSeq2SeqLM.from_pretrained(PARAPHRASER_MODEL)
        model.to(device)
        print(f"[OK] Đã tải xong Paraphraser.")
        
        # Initialize Estimator
        print(f"[*] Đang tải Estimator từ: {ESTIMATOR_MODEL}...")
        estimator = QCModelEstimator(model_path=ESTIMATOR_MODEL, device=device)
        print(f"[OK] Đã tải xong Estimator.")

        # Initialize Quality Evaluator
        print(f"[*] Đang khởi tạo Dashboard Evaluator...")
        quality_evaluator = QualityEvaluator(device=device)
        print(f"[OK] Đã khởi tạo xong Dashboard Evaluator.")
        
        print("\n" + "="*50)
        print("HỆ THỐNG ĐÃ SẴN SÀNG PHỤC VỤ")
        print("="*50 + "\n")
    except Exception as e:
        print(f"\n[ERROR] Lỗi nghiêm trọng khi khởi tạo: {e}")
        import traceback
        traceback.print_exc()
        print("="*50 + "\n")

@app.post("/api/paraphrase")
async def generate_paraphrase(request: ParaphraseRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Văn bản đầu vào không được để trống")
    if model is None or estimator is None or quality_evaluator is None:
         raise HTTPException(status_code=503, detail="Hệ thống đang được khởi tạo hoặc chưa sẵn sàng")
    
    try:
        if _USE_MOCK:
            time.sleep(1) # Giả lập delay
            candidates_text = model.generate(request.text, request.num_candidates)
        else:
            # Chuẩn hoá (làm tròn) về bội số gần nhất của 5
            sem_norm = round(request.semantic / 5) * 5
            syn_norm = round(request.syntactic / 5) * 5
            lex_norm = round(request.lexical / 5) * 5
            
            # Prefix cho task
            input_text = f"paraphrase: SEM_{sem_norm} SYN_{syn_norm} LEX_{lex_norm} {request.text}"
            
            # Tokenize
            encoding = tokenizer(
                input_text, 
                return_tensors="pt", 
                padding=True, 
                truncation=True, 
                max_length=256
            )
            input_ids = encoding["input_ids"].to(device)
            attention_mask = encoding["attention_mask"].to(device)
            
            # Generate
            outputs = model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_length=256,
                num_beams=max(request.num_beams, request.num_candidates),
                num_return_sequences=request.num_candidates,
                early_stopping=True,
                no_repeat_ngram_size=2
            )
            
            # Decode
            candidates_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        
        # Evaluate each candidate
        results = []
        for cand in candidates_text:
            # 1. Model-based scores (from QC Model)
            qc_scores = estimator.estimate(request.text, cand)
            
            # 2. Metric-based scores (for Dashboard)
            metric_scores = quality_evaluator.evaluate(request.text, cand)
            
            # Calculate Overall Score (Average of all metrics for now, or just semantic)
            overall_score = round(
                (qc_scores["semantic_score"] + qc_scores["syntactic_score"] + qc_scores["lexical_score"]) / 3, 
                2
            )

            results.append({
                "text": cand,
                "scores": qc_scores,
                "metrics": metric_scores,
                "overall_score": overall_score
            })
            
        # Determine "best" (highest overall score)
        if results:
            best_idx = 0
            max_overall = -1
            for i, res in enumerate(results):
                if res["overall_score"] > max_overall:
                    max_overall = res["overall_score"]
                    best_idx = i
            results[best_idx]["is_best"] = True

        return {
            "original": request.text,
            "candidates": results
        }
    except Exception as e:
         import traceback
         traceback.print_exc()
         raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tree")
async def get_trees(request: TreeRequest):
    try:
        if _USE_MOCK:
            time.sleep(0.5)
            return {
                "original_tree": f"(S (NP {request.original}) (VP (V mock) (NP tree)) )",
                "paraphrase_tree": f"(S (NP {request.paraphrase}) (VP (V mock) (NP tree)) )"
            }
            
        from src.utils.metrics.ted_metric import _init_vi_pipeline
        nlp = _init_vi_pipeline()
        
        doc1 = nlp(request.original)
        doc2 = nlp(request.paraphrase)
        
        tree1 = str(doc1.sentences[0].constituency) if doc1.sentences else ""
        tree2 = str(doc2.sentences[0].constituency) if doc2.sentences else ""
        
        return {
            "original_tree": tree1,
            "paraphrase_tree": tree2
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e), "original_tree": "", "paraphrase_tree": ""}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    static_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if not os.path.exists(static_path):
        return "UI index.html not found. Please ensure the static directory is correctly set up."
    with open(static_path, "r", encoding="utf-8") as f:
        return f.read()

# Phục vụ thư mục static
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
