import json
from transformers import GPTJForCausalLM, AutoTokenizer, AutoModelForCausalLM,GPT2Tokenizer, GPT2LMHeadModel, GPTNeoForCausalLM ,XLNetForSequenceClassification, XLNetTokenizer, T5ForConditionalGeneration, T5Tokenizer, BertTokenizer, BertForMaskedLM
import re
from semanticMapping import dynamic_semantic_mapping
from semantic_extractor import SemanticExtractor

# Load the ontology from the JSON file
with open('def-sponsor00/meriembchaaben/data/modeling_languages_ontology.json', 'r') as file:
    ontology = json.load(file)

# Load the pre-trained GPT-J model and tokenizer
#model_name = "EleutherAI/gpt-j-6B"  # will be replaced with the best  model

#tokenizer = AutoTokenizer.from_pretrained(model_name)
#model = GPTJForCausalLM.from_pretrained(model_name)

#model_name = "gpt-neo"  # This loads the "small" version of GPT-2
#tokenizer = GPT2Tokenizer.from_pretrained(model_name)
#model = GPT2LMHeadModel.from_pretrained(model_name)



# Load pre-trained T5 model and tokenizer
#model_name = "t5-large"  # You can choose other T5 variants like "t5-base", "t5-large", etc.
#tokenizer = T5Tokenizer.from_pretrained(model_name)
#model = T5ForConditionalGeneration.from_pretrained(model_name)


#model_name = "EleutherAI/gpt-neo-1.3B"
#model = GPTNeoForCausalLM.from_pretrained(model_name)
#tokenizer = GPT2Tokenizer.from_pretrained(model_name)

#model_name = "bert-large-uncased"  # You can choose other BERT variants like "bert-large-uncased", "bert-base-cased", etc.
#tokenizer = BertTokenizer.from_pretrained(model_name)
#model = BertForMaskedLM.from_pretrained(model_name)



#model_name = "t5-large"  # You can choose other T5 variants like "t5-base", "t5-large", etc.
#tokenizer = T5Tokenizer.from_pretrained(model_name)
#model = T5ForConditionalGeneration.from_pretrained(model_name)



model_name = "TheBloke/LLaMA-Pro-8B-GPTQ"
model = AutoModelForCausalLM.from_pretrained(model_name,
                                             device_map="auto",
                                             trust_remote_code=False,
                                             revision="main")
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)


print('model loaded :', model_name)

def find_metamodel_elements(data, formalism_name):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == formalism_name and "metamodel" in value:
                print('metamodel found ...')
                print(value["metamodel"])
                return value["metamodel"]
            else:
                result = find_metamodel_elements(value, formalism_name)
                if result:
                    return result  # Return immediately if result is found
    elif isinstance(data, list):
        for item in data:
            result = find_metamodel_elements(item, formalism_name)
            if result:
                return result  # Return immediately if result is found
    return None  # Ensure that None is returned if no result is found






def generate_text( prompt, max_length=150):


    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    print(input_ids)

    output = model.generate(input_ids, temperature=0.7, do_sample=True, top_p=0.95, top_k=40, max_new_tokens=512, max_length=max_length, num_return_sequences=1)
    print("outputt: ..... ", output)
    return tokenizer.decode(output[0], skip_special_tokens=True)



def generate_prompt_for_formalism(formalism_name, current_model, metamodel_elements,desired_functionality=None, specific_constraints=None):
    """
    Generates a prompt for the LLM based on the metamodel elements of a given formalism,
    the current model, and optionally, desired functionality and constraints.
    
    :param formalism_name: The name of the formalism to generate the prompt for.
    :param current_model: A string representing the current state of the model under construction.
    :param desired_functionality: (Optional) A string describing the desired functionality to be added.
    :param specific_constraints: (Optional) A string describing any specific constraints that must be adhered to.
    :return: A prompt string for the LLM.
    """
    # Navigate the ontology to find the metamodel for the given formalism
    
   
    
    # Construct the prompt using the current model and metamodel elements
    if metamodel_elements:
        #metamodel_description = ', '.join(metamodel_elements)
        prompt_parts = [
            f"I am developing a {formalism_name} which currently includes: {current_model}.",
            f"suggest missing elements",
            f"It should also contain elements such as: {metamodel_elements}."
        ]
        
        # If desired functionality is provided, add it to the prompt
        if desired_functionality:
            prompt_parts.append(f"The model needs to support: {desired_functionality}.")
        
        # If specific constraints are provided, add them to the prompt
        if specific_constraints:
            prompt_parts.append(f"This should adhere to the following constraints: {specific_constraints}.")
        
        prompt_parts.append("suggest missing elements:")
        
        # Semantic Mapping
       #### semantic_description = '. '.join([f"A {key} is represented as a {value} in natural language" for key, value in dynamic_semantic_mapping.items()])
        ####  prompt_parts.append(semantic_description)
        prompt = " ".join(prompt_parts)

        return prompt
    else:
        return f"Formalism '{formalism_name}' not found in the ontology."



def create_extraction_patterns(metamodel_description):
    """
    Creates extraction patterns based on the metamodel description.
    """
    # Simple pattern generation: create word boundary patterns for each element in the metamodel
    patterns = {element: re.compile(r'\b' + re.escape(element) + r'\b', re.IGNORECASE) for element in metamodel_description.split(', ')}
    return patterns

def extract_model_elements(llm_response, extraction_patterns):
    """
    Extracts model elements from the LLM response based on dynamic extraction patterns.
    """
    extracted_elements = {}
    
    for element, pattern in extraction_patterns.items():
        # Find all matches for each pattern
        matches = pattern.findall(llm_response)
        if matches:
            # Remove duplicates and keep matches
            extracted_elements[element] = list(set(matches))

    return extracted_elements



def get_user_feedback(extracted_elements):
    """
    Asks the user for feedback on the extracted elements.
    """
    print("The following elements were extracted from the model completion suggestion:")
    for element, values in extracted_elements.items():
        print(f"{element.capitalize()}: {', '.join(values)}")
    
    feedback = input("Are these elements correct? (yes/no): ")
    if feedback.lower() == 'yes':
        print("Model completion accepted by the user.")
        return True
    else:
        print("Model completion rejected by the user. Please refine the prompt or provide additional details.")
        return False

def main():
    print('start')
    formalism_name = "ClassDiagrams"
    current_model = "Classes: Customer, Product; Attributes: Customer(name, address), Product(name, price)"
    metamodel_description= find_metamodel_elements(ontology,formalism_name)
    # Generate dynamic extraction patterns based on the metamodel description
    extraction_patterns = create_extraction_patterns(metamodel_description)
    #extractor = SemanticExtractor()


    # Start the feedback loop
    completed = False
    while not completed:
        # Generate the prompt using the current state of the model
        prompt = generate_prompt_for_formalism(formalism_name,current_model,metamodel_description)
        print(f"Prompt to LLM:\n{prompt}\n")

        # Generate text from the LLM
        llm_response = generate_text(prompt)
        print(f"LLM Response:\n{llm_response}\n")

        # Extract elements from the LLM response
        extracted_elements = extract_model_elements(llm_response, extraction_patterns)
        print(f"Extracted Elements:\n{extracted_elements}\n")

        # Get user feedback
        completed = get_user_feedback(extracted_elements)

        if not completed:
            # Here, you might adjust the prompt based on user feedback before the next iteration
            # For example, ask the user for additional details to refine the next LLM request
            additional_details = input("Please provide additional details to improve the model completion: ")
            current_model += " " + additional_details  # Append additional details to the current model state

if __name__ == "__main__":
    main()