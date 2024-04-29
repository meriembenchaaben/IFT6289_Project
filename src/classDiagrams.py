import re
import json
from diagram_extractors import DiagramExtractor

class ClassDiagramExtractor(DiagramExtractor):
    def __init__(self, diagram_data):
        self.diagram_data = diagram_data
        self.extraction_patterns = self.create_extraction_patterns()

    def create_extraction_patterns(self):
        patterns = {
            'classes': r'Class\s+([A-Za-z0-9_]+)',
            'attributes': r'([a-z][A-Za-z0-9_]*):\s*([A-Za-z0-9_]+)',
            'methods': r'([a-z][A-Za-z0-9_]*\(\)):\s*([A-Za-z0-9_]+)'
        }
        return patterns

    def extract_elements(self):
        elements = {}
        for element, pattern in self.extraction_patterns.items():
            elements[element] = re.findall(pattern, self.diagram_data, re.IGNORECASE)
        return elements

    @staticmethod
    def load_class_diagram(json_file_path):
        with open(json_file_path, 'r') as file:
            return json.load(file)

    def encode_to_llm_prompt(self):
        classes_text = []
        for cls in self.diagram_data["classes"]:
            cls_name = cls["name"]
            attributes = ', '.join([f'{attr["name"]}:{attr["type"]}' for attr in cls.get("attributes", [])])
            methods = ', '.join([f'{method["name"]}({", ".join([f"{param["name"]}:{param["type"]}" for param in method.get("parameters", [])])}):{method["returnType"]}' for method in cls.get("methods", [])])
            classes_text.append(f'{cls_name} with attributes {attributes} and methods {methods}')
        relationships_text = ', '.join([f'{rel["from"]} {rel["type"]} {rel["to"]}' for rel in self.diagram_data.get("relationships", [])])
        return f'Classes: {"; ".join(classes_text)}. Relationships: {relationships_text}.'
