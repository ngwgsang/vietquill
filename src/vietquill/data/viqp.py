from datasets import load_dataset
from .base import BaseDataset
from .registry import DATASET_REGISTRY

class ViQPDataset(BaseDataset):
    """
    Dataset class for the ViQP dataset.
    """
    DS_NAME = "viqp"
    HF_REPO = DATASET_REGISTRY[DS_NAME]

    def load(self):
        return load_dataset(self.HF_REPO)

    def load_questions(self):

        ds = self.load()

        return ds.map(
            lambda x: {
                "pair_id": x["pair_id"],
                "sentence1": x["original_text"],
                "sentence2": x["paraphrase_text"]
            }
        )
    