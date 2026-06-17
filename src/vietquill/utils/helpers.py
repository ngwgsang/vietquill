from uuid import uuid4, uuid5, NAMESPACE_DNS

def generate_random_id() -> str:
    """Generates a unique UUID string."""
    return str(uuid4().hex)

def generate_pair_id(sentence1: str, sentence2: str) -> str:
    """Generates a unique pair ID for paraphrase pairs."""
    combined_sentences = f"{sentence1} [sep] {sentence2}"
    return str(uuid5(NAMESPACE_DNS, combined_sentences).hex)
