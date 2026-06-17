from vietquill.data import ViQPDataset, ViSPDataset
from logging import getLogger

logger = getLogger(__name__)

def test_load_viqp():
    dataset = ViQPDataset()
    ds = dataset.load()
    assert "train" in ds
    assert "test" in ds
    logger.info("[OK] ViQP dataset loaded successfully.")

def test_load_visp():
    dataset = ViSPDataset()
    ds = dataset.load()
    assert "train" in ds
    assert "validation" in ds
    assert "test" in ds
    logger.info("[OK] ViSP dataset loaded successfully.")

if __name__ == "__main__":
    test_load_viqp()
    test_load_visp()