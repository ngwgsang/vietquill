from vietquill.evaluation import BLEUMetric, LexicalEstimator

# Reference and candidate sentences
original = "Hôm nay trời đẹp quá, mình muốn đi dạo công viên."
paraphrase = "Thời tiết hôm nay thật tuyệt, tôi muốn tản bộ trong công viên."

# 1. Traditional Metrics
bleu = BLEUMetric()
score = bleu.score(original, paraphrase)
print(f"BLEU Score: {score:.4f}")

# 2. Aspect Estimators (Lexical, Semantic, Syntactic)
lex_est = LexicalEstimator()
estimation = lex_est.estimate(original, paraphrase)
print(f"Lexical Change Score: {estimation['lexical_score']}%")
