import stanza
from apted import APTED
from apted.helpers import Tree
from vietquill.evaluation.metrics.base_metric import BaseMetric
    
_nlp = None

def _init_vi_pipeline():
    global _nlp
    if _nlp is not None:
        return _nlp
    try:
        _nlp = stanza.Pipeline(
            lang="vi",
            processors="tokenize,pos,constituency",
            use_gpu=True
        )
    except Exception:
        stanza.download("vi")
        _nlp = stanza.Pipeline(
            lang="vi",
            processors="tokenize,pos,constituency",
            use_gpu=True
        )
    return _nlp

class TEDMetric(BaseMetric):
    """
    Compute a normalized Tree Edit Distance (TED) similarity over bracket trees.
    """
    def __init__(self, max_depth: int = 3):
        self.max_depth = max_depth
        self.total_sim = 0.0
        self.count = 0

    def normalize_tree(self, tree_string: str) -> str:
        """
        Convert a standard bracket tree to a '{' '}' style with depth truncation.
        """
        res = []
        depth = -1
        leaf = False
        for c in tree_string:
            if c in ['{', '}']:
                continue
            if c == '(':
                leaf = False
                depth += 1
            elif c == ')':
                leaf = False
                depth -= 1
                if depth < self.max_depth:
                    res.append('}')
                    continue
            elif c == ' ':
                leaf = True
                continue
            if depth <= self.max_depth and not leaf and c != ')':
                res.append(c if c != '(' else '{')
        return ''.join(res)

    def tree_edit_distance(self, lintree1: str, lintree2: str) -> float:
        """
        Return normalized TED: raw_edit_distance / (nodes1 + nodes2).
        """
        try:
            t1 = Tree.from_text(lintree1)
            t2 = Tree.from_text(lintree2)
        except Exception:
            return 1.0

        n1 = lintree1.count('{')
        n2 = lintree2.count('{')
        if (n1 + n2) == 0:
            return 0.0
        
        ted = APTED(t1, t2).compute_edit_distance()
        return ted / (n1 + n2)

    def score(self, sentence1, sentence2):
        """
        Compute syntactic similarity score in [0, 1].
        """
        s1 = (sentence1 or "").strip()
        s2 = (sentence2 or "").strip()
        if not s1 and not s2:
            return 1.0
        if not s1 or not s2:
            return 0.0

        nlp = _init_vi_pipeline()
        doc1 = nlp(s1)
        doc2 = nlp(s2)

        if not doc1.sentences or not doc2.sentences:
            return 0.0
        
        try:
            tree1 = str(doc1.sentences[0].constituency)
            tree2 = str(doc2.sentences[0].constituency)
        except Exception:
            return 0.0

        t1n = self.normalize_tree(tree1)
        t2n = self.normalize_tree(tree2)
        ted_norm = self.tree_edit_distance(t1n, t2n)
        sim = max(0.0, min(1.0, 1.0 - ted_norm))
        return sim

    def update(self, y_true, y_pred):
        self.total_sim += self.score(y_true, y_pred)
        self.count += 1

    def compute(self):
        if self.count == 0:
            return 0.0
        return self.total_sim / self.count

    def reset(self):
        self.total_sim = 0.0
        self.count = 0
