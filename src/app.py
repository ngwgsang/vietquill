import sys
import os

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

app = FastAPI(title="VietQuill Paraphrase API", description="API demo cho task paraphrase sử dụng mô hình vietquill-vit5-base-viqp-3e5 và velectra-base-qc-question-3e5")

# Cấu hình CORS
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

@app.on_event("startup")
async def startup_event():
    global tokenizer, model, device, estimator, quality_evaluator
    print("\n" + "="*50)
    print("KHỞI TẠO HỆ THỐNG VIETQUILL")
    print("="*50)
    
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
    if tokenizer is None or model is None or estimator is None or quality_evaluator is None:
         raise HTTPException(status_code=503, detail="Hệ thống đang được khởi tạo hoặc chưa sẵn sàng")
    
    try:
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
         raise HTTPException(status_code=500, detail=str(e))

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
