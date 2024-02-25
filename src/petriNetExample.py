def send_prompt_to_llm(prompt):
    """
    Mock function to simulate sending a prompt to an LLM and receiving a response.
    This is a placeholder for interaction with an actual LLM service.
    ToDo: code to query the engine + set appropriate hyperparametrs
    """
    # Simulated LLM response for the sake of example ( we are waiting for something like that)
    response = "To complete the Petri net model, consider adding a transition that represents..."
    return response + " the process of task allocation, connected to places representing 'Task Queue' and 'Processing Tasks'."

def construct_prompt(petri_net_description, metamodel_description, desired_outcomes):
    """
    Constructs a detailed prompt for the LLM, tailored for completing a Petri net model.
    """
    prompt = f"""
    I have a Petri net model designed for modeling a distributed task management system. 
    The Petri net is described as follows: {petri_net_description}. 
    According to the Petri net metamodel, which includes {metamodel_description}, 
    I need to extend the model to support {desired_outcomes}.

    Can you suggest modifications or additions to the Petri net to achieve these functionalities?
    """
    return prompt

import re

def extract_petri_net_elements(llm_response):
    """
    Extracts Petri net components (places, transitions, arcs) from the LLM response.
    This function uses simple string searching and regular expressions.
    To do: more sophisticated nlp approach such as:
    ***  Named Entity Recognition (NER), seen in IFT6285
    Identify and classify key information in text into predefined categories such as names of places 
    (in the context of Petri nets, these could be "places" and "transitions" within the model)
    *** Dependency Parsing
    Analyze the grammatical structure of a sentence to establish relationships between "tokens" (words),
    which can help in understanding how different parts of a sentence (e.g., subjects, verbs, objects) are related. 
    This is useful for extracting complex relationships or for understanding the context in which Petri net elements are mentioned.
    """
    # Define patterns for places, transitions, and other elements
    place_pattern = r"'([^']+)'\s*representing\s*'([^']+)'"
    transition_pattern = r"transition\s*that\s*represents\s*'([^']+)'"
    
    # Search for places
    places = re.findall(place_pattern, llm_response)
    transitions = re.findall(transition_pattern, llm_response)
    
    # For simplicity, arcs and other elements are not extracted in this example
    # They could be identified through similar patterns or more complex NLP techniques
    
    # Construct a simple representation of the extracted elements
    petri_net_elements = {
        'places': [{'name': match[0], 'description': match[1]} for match in places],
        'transitions': [{'description': match} for match in transitions]
    }
    
    return petri_net_elements




def user_feedback(elements):
    # Simulate user feedback mechanism
    # In a real scenario, this would involve user input
    print(f"Extracted elements: {elements}")
    user_decision = input("Accept these elements? (y/n): ")
    return user_decision.lower() == 'y'

def refine_prompt(prompt, iteration):
    # Refine the prompt based on feedback loop iteration
    return f"{prompt} Iteration {iteration}: Looking for more detailed suggestions."

def feedback_loop(initial_prompt, iterations=3):
    prompt = initial_prompt
    for iteration in range(1, iterations + 1):
        print(f"\nIteration {iteration}")
        llm_response = simulate_llm_response(prompt)
        elements = extract_petri_net_elements(llm_response)
        
        if user_feedback(elements):
            print("Updating model with accepted elements...")
            # Here, update the model with the elements (not shown)
            break
        else:
            print("Refining prompt based on feedback...")
            prompt = refine_prompt(prompt, iteration)

initial_prompt = "I have a Petri net model for a distributed task management system."
feedback_loop(initial_prompt)


def main():
    # Example details for the Petri net model
    petri_net_description = "places representing 'Idle Resources', 'Task Queue', and transitions for 'Start Task' and 'End Task'"
    metamodel_description = "places, transitions, and arcs, where places hold tokens that represent system states, and transitions change these states"
    desired_outcomes = "optimizing resource allocation and minimizing idle times"

    
    prompt = construct_prompt(petri_net_description, metamodel_description, desired_outcomes)
    
    llm_response = send_prompt_to_llm(prompt)
    
    print("LLM Response:\n", llm_response)
    
    petri_net_elements = extract_petri_net_elements(llm_response)
    print("Extracted Petri Net Elements:\n", petri_net_elements)



if __name__ == "__main__":
    main()
