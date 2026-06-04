"""
VietQuill: Quality-Controlled Paraphrase Generation for Vietnamese Language
Copyright (C) 2026 - Sang Quang Nguyen

This script is part of VietQuill.
"""

# Add the project root to sys.path to allow imports from src
import sys
import os
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

import stanza
from apted import APTED
from apted.helpers import Tree
from src.utils.metrics.base_metric import BaseMetric
    
# ---------------------------
# Lazy init for Vietnamese NLP
# ---------------------------
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
        # Auto-download VI models if missing, then retry once
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
    The tree is first depth-truncated/normalized, then APTED distance is computed
    and converted to a similarity in [0, 1].
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
            return 1.0 # Max distance if parsing fails

        n1 = lintree1.count('{')
        n2 = lintree2.count('{')
        if (n1 + n2) == 0:
            return 0.0  # identical-empty
        
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

        # Use the first sentence’s constituency tree from each doc
        if not doc1.sentences or not doc2.sentences:
            return 0.0
        
        try:
            tree1 = str(doc1.sentences[0].constituency)
            tree2 = str(doc2.sentences[0].constituency)
        except Exception:
            # In case constituency is unavailable
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

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Compute Syntactic Similarity using Tree Edit Distance (TED)."
    )

    parser.add_argument(
        "--text1",
        type=str,
        required=True,
        help="First sentence"
    )

    parser.add_argument(
        "--text2",
        type=str,
        required=True,
        help="Second sentence"
    )

    parser.add_argument(
        "--max_depth",
        type=int,
        default=3,
        help="Maximum tree depth for normalization"
    )

    args = parser.parse_args()

    metric = TEDMetric(max_depth=args.max_depth)
    score = metric.score(args.text1, args.text2)

    print("---" * 30)
    print(f"Metric      : Tree Edit Distance (TED)")
    print(f"Max Depth   : {args.max_depth}")
    print(f"Sentence 1  : {args.text1}")
    print(f"Sentence 2  : {args.text2}")
    print(f"TED Score   : {score:.4f} (Similarity)")
