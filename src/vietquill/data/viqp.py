from datasets import load_dataset
from vietquill.data.base import BaseDataset
from vietquill.data.registry import DATASET_REGISTRY
from vietquill.data.schema import ParaphraseSchema
from vietquill.utils import generate_pair_id

class ViQPDataset(BaseDataset):
    """
    Dataset class for the ViQP dataset.
    """
    DS_NAME = "viqp"
    HF_REPO = DATASET_REGISTRY[DS_NAME]

    def load(self):
        return load_dataset(self.HF_REPO)

    def load_pairs(self):

        ds = self.load()

        return ds.map(
            lambda x: ParaphraseSchema(
                pair_id=generate_pair_id(x["original_text"], x["paraphrase_text"]),
                sentence1=x["original_text"],
                sentence2=x["paraphrase_text"]
            ).model_dump()
        )
    