dynamic_semantic_mapping = {
    "UML": {
        "Entity": "Class, Interface",
        "Relationship": "Association, Generalization, Dependency",
        "Attribute": "Field, Property",
        "Behavior": "Method, Operation",
        "Event": "Signal Event, Time Event",
        "State": "State, Pseudostate"
    },
    "BPMN": {
        "Entity": "Process, Lane, Pool",
        "Event": "Start Event, End Event, Intermediate Event",
        "Gateway": "Exclusive Gateway, Parallel Gateway, Inclusive Gateway",
        "Activity": "Task, Sub-Process",
        "Flow": "Sequence Flow, Message Flow"
    },
    "ER": {
        "Entity": "Entity, Weak Entity",
        "Relationship": "Relationship, Identifying Relationship",
        "Attribute": "Key Attribute, Descriptive Attribute",
        "Constraint": "Participation Constraint, Cardinality Constraint"
    },
    # Add other formalisms with their specific semantic mappings as needed
}
