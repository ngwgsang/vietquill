from abc import ABC, abstractmethod
from datasets import DatasetDict

class BaseDataset(ABC):

    @abstractmethod
    def load(self) -> DatasetDict:
        pass