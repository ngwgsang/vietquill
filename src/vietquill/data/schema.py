from pydantic import BaseModel, Field

class ParaphraseSchema(BaseModel):
    """
    Schema for a paraphrase example.
    """
    pair_id: str = Field(..., description="The unique identifier for the paraphrase pair.")
    sentence1: str = Field(..., description="The source sentence.")
    sentence2: str = Field(..., description="The paraphrased sentence.")