
from abc import ABC, abstractmethod
class DiagramExtractor(ABC):
    def __init__(self, diagram_data):
        self.diagram_data = diagram_data

    @abstractmethod
    def extract_elements(self):
        pass

    @abstractmethod
    def create_extraction_patterns():
        pass

    @abstractmethod
    def encode_to_llm_prompt(self):
        """Encode extracted elements into a prompt for the LLM."""
        pass