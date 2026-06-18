import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import torch
import uvicorn

# Sử dụng trực tiếp thư viện vietquill
from vietquill import AutoModelForControllableParaphraseGeneration, AutoModelForParaphraseQualityEstimation
from vietquill.evaluation.metrics.bleu_metric import BLEUMetric
from vietquill.evaluation.metrics.bertscore_metric import BERTScoreMetric
from vietquill.evaluation.metrics.jaccard_metric import JaccardMetric
from vietquill.evaluation.metrics.ted_metric import TEDMetric
from vietquill.evaluation.metrics.parascore_metric import ParaScoreMetric

class DemoQualityEvaluator:
    def __init__(self, device="cpu"):
        print("[*] Khởi tạo các metrics truyền thống (BLEU, BERTScore, Jaccard, TED, ParaScore)...")
        self.bleu = BLEUMetric()
        self.bertscore = BERTScoreMetric(device=device)
        self.jaccard = JaccardMetric()
        self.ted = TEDMetric()
        self.parascore = ParaScoreMetric(batch_size=1)
        
    def evaluate(self, source, candidate):
        try:
            return {
                "bleu": round(self.bleu.score(source, candidate) * 100, 2),
                "bertscore": round(self.bertscore.score(source, candidate) * 100, 2),
                "jaccard_diversity": round((1 - self.jaccard.score(source, candidate)) * 100, 2),
                "ted": round(self.ted.score(source, candidate) * 100, 2),
                "parascore": round(self.parascore.score_free(source, candidate) * 100, 2)
            }
        except Exception as e:
            print(f"Lỗi tính metric: {e}")
            return {"bleu": 0, "bertscore": 0, "jaccard_diversity": 0, "ted": 0, "parascore": 0}

app = FastAPI(title="VietQuill Paraphrase API", description="API demo cho task paraphrase sử dụng thư viện VietQuill")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None
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
    global model, estimator, quality_evaluator
    print("\n" + "="*50)
    print(f"KHỞI TẠO HỆ THỐNG VIETQUILL")
    print("="*50)

    try:
        print("[*] Đang khởi tạo Generator (AutoModelForControllableParaphraseGeneration)...")
        model = AutoModelForControllableParaphraseGeneration()
        print("[OK] Hoàn tất Generator.")
        
        print("[*] Đang khởi tạo Estimator (AutoModelForParaphraseQualityEstimation)...")
        estimator = AutoModelForParaphraseQualityEstimation()
        print("[OK] Hoàn tất Estimator.")

        print("[*] Đang khởi tạo Dashboard Evaluator...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        quality_evaluator = DemoQualityEvaluator(device=device)
        print("[OK] Hoàn tất Dashboard Evaluator.")
        
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
        candidates_text = model.paraphrase(
            request.text, 
            semantic=request.semantic,
            syntactic=request.syntactic,
            lexical=request.lexical,
            num_candidates=request.num_candidates,
            num_beams=request.num_beams
        )
        
        results = []
        for cand in candidates_text:
            qc_scores = estimator.estimate(request.text, cand)
            metric_scores = quality_evaluator.evaluate(request.text, cand)
            
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
        from vietquill.evaluation.metrics.ted_metric import _init_vi_pipeline
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

static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
