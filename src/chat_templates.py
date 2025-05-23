from langchain.prompts import ChatPromptTemplate
chat_templates = {}

# GET PROPERTY GROUPS FOR ROOT CONCEPT
#
# Name: chat_template_get_property_groups
# Parameters: root_concept
# Description: Identifies the distinct groups into which all distinguishing properties of the specified root concept can be classified.
# Expected Result: Returns a comma-separated list of group names representing the primary dimensions of property variation for the concept.

chat_templates['get_property_groups'] = ChatPromptTemplate.from_messages(
        [
            ("system", '''Role: You are a highly skilled scientific expert.
             Task: Identify into how many different groups can all distinguishing properties of the concepts of type "{root_concept}" be divided? List the names of all necessary groups, separated by commas, without comments and without focusing on the specific properties themselves.
             Constraints: Skip explanations and return group names in a comma-separated format.
             '''
),
            ("human", '''''')
        ]
    )

# GET KEY ASPECT DESCRIPTIONS FOR SUB-CONCEPT DISTINCTION
#
# Name: chat_template_get_key_aspects
# Parameters: root_concept
# Description: Identifies the minimal set of key feature descriptions required to accurately differentiate all sub-concepts of the given root concept and determine their correct hierarchical order.
# Expected Result: Returns a semicolon-separated list of concise descriptions representing the most critical distinguishing aspects of the concept.

chat_templates['get_key_aspects'] = ChatPromptTemplate.from_messages(
        [
            ("system", '''Role: You are a highly skilled scientific expert.
Task: How many descriptions of the "{root_concept}" key features are sufficient to correctly distinguish between all "{root_concept}" sub-concepts and properly order them inside taxonomical hierarchy?
Constraints: Please skip any explanations and respond with a list of descriptions separated by semicolon.
             '''
),
            ("human", '''''')
        ]
    )

# GET RARE AND OVERLOOKED TAXONOMICAL FEATURES
#
# Name: chat_template_get_rare_info
# Parameters: root_concept
# Description: Generates a list of brief but insightful descriptions revealing rare, surprising, or underappreciated taxonomical ranks and criteria that distinguish sub-concepts of the given root concept.
# Expected Result: Returns a semicolon-separated list of concise descriptions highlighting rare classification features, newly discovered criteria, and unconventional distinctions within the taxonomy.

chat_templates['get_rare_info'] = ChatPromptTemplate.from_messages(
        [
            ("system",'''Role: You are a highly skilled scientist and ontology expert. 	
Given the concept of "{root_concept}", construct a descriptions that uncover overlooked or underappreciated rare taxonomical features (criteria or ranks). 
A taxonomical rank is a hierarchical level that classifies concepts based on a variable property inherent to sub-concepts within the rank.
The importance and representativeness of a rank depend on how accurately it reflects a significant and variable property that affects the distinction of concepts within the hierarchy. I am interested in the most unexpected and odd ranks. 
A criterion is a specific property or characteristic used to differentiate and classify concepts within a particular rank, serving as the basis for organizing sub-concepts according to their variations. 
Provided descriptions must be sufficient for a deeper taxonomical analysis. Focus on revealing hidden or unaccounted-for ranks of sub-concepts (e.g., unique material characteristics, rare physical or functional parameters, unusual types of interactions related to "{root_concept}"). Keep descriptions brief but as informative as possible. Include at least one surprising aspect that challenges traditional views of "{root_concept}" classification. Include information about newely found criteria and ranks that changed their place inside broader taxonomy. Highlight significant but often unnoticed distinctions between similar sub-classes of "{root_concept}". Keep answers very short but informative, include as much rare criteria and ranks as you can. 
Provide only the list of descriptions separated by semicolon(;) and dont include any additional explanations.
'''),
            ("human", '''''')
        ]
    )

# GENERATE INITIAL INDEPENDENT HIERARCHY DESCRIPTIONS
#
# Name: chat_template_get_initial_hierarchies
# Parameters: root_concept, properties
# Description: Analyzes a list of property categories related to a root concept and constructs a minimal set of independent taxonomy hierarchies. Each hierarchy is described concisely, including its purpose, key classification dimensions, and how it organizes sub-concepts of the root concept.
# Expected Result: Returns semicolon-separated hierarchy descriptions, each beginning with a hierarchy name and explaining the classification rationale based on distinct property groups. The format is strict, concise, and free of examples or commentary.

chat_templates['get_initial_hierarchies'] = ChatPromptTemplate.from_messages(
        [
            ("system", '''Role: You are a highly skilled scientific expert in conceptual modeling and taxonomy.

Task:
Using the provided list of distinguishing property categories for the concept "{root_concept}": "{properties}", determine the minimal number of independent hierarchies required to represent all combinations of these categories.
Create concise descriptions for each hierarchy that explain what it deals with, its purpose, and the key property groups used for classification. The descriptions should also indicate how sub-concepts of "{root_concept}" can be classified based on these criteria, without specific examples.
Each description must begin with the hierarchy’s name, followed by a colon (e.g., "Hierarchy 1: Evolutionary Classification: This hierarchy classifies biological species based on...").

Rules:
Each hierarchy description must not exceed 50 tokens.
Never use semicolons (;) and newlines (\\n) in the descriptions.
Keep responses concise, avoiding unnecessary elaboration or speculation.
Stop generating if irrelevant or nonsensical content is produced.
Provide only the hierarchy descriptions, separated by semicolons (;) in the output.
Summarize the key criteria in one sentence at the end of each hierarchy.
Skip any additional explanations or comments.
             
Format:
Hierarchy 1: [description]; Hierarchy 2: [description of the next hierarchy];
             
Instructions:
Continue in this format for each hierarchy. Generate as many semicolon-separated hierarchies as necessary and finish with the new line.
'''
),
            ("human", '''''')
        ]
    )

# FIND AND DESCRIBE MISSING TAXONOMICAL HIERARCHIES
#
# Name: chat_template_find_missing_hierarchies
# Parameters: root_concept, current_hierarchies
# Description: Analyzes an existing set of taxonomical hierarchies for a given root concept to identify whether any essential classification dimensions are missing. If the current hierarchies are insufficient to fully represent all distinguishing properties of the concept, it generates concise descriptions for the minimal number of new hierarchies required to ensure completeness.
# Expected Result: Returns semicolon-separated descriptions of newly required hierarchies only. If no additional hierarchies are needed, returns an empty response. Each description must begin with the hierarchy’s name and describe its purpose, focus, and key classification criteria.

chat_templates["find_missing_hierarchies"] = ChatPromptTemplate.from_messages(
        [
            ("system", '''Role: You are an expert in conceptual modeling and taxonomy.

Task:
You are given a set of current hierarchical classification descriptions for the root concept "{root_concept}".
These hierarchies are intended to create a well-structured taxonomy that classifies the root concept and all its sub-concepts across multiple levels.
The goal is to improve the existing structure either by confirming the sufficiency of the existing hierarchies or introducing new ones. 
To achieve this, review the provided hierarchies and assess whether they are both sufficient and complete for optimal classification. Specifically, check if any key properties of the root concept, which could define sub-concepts, are missing or not accounted for in the current hierarchies.
Determine if the hierarchical structures can potentially classify future sub-concepts based on the key properties expected in their parent concepts.
If the current hierarchies are insufficient or incomplete, identify the minimun number of new hierarchies needed to ensure consistency and completeness, then formulate and describe them.
If new hierarchies are required, list them. If no new hierarchies are needed, return an empty response.

Rules:
Each hierarchy description must be a single, concise block of text.
Each description must begin with the hierarchy’s name, followed by a colon (e.g., "Hierarchy 1: Evolutionary Classification: This hierarchy classifies biological species based on...").
The description should cover what the hierarchy deals with, its purpose, key property groups, and criteria used for classification (without specific examples). End with a brief summary of key criteria.
Keep each description under 50 tokens.
Never use semicolons (;) and newlines (\\n) in the descriptions.
Output only new hierarchies, omitting any existing ones.
Stop generating if irrelevant or nonsensical content is produced.
Always separate the hierarchies by semicolons (;) in the output.
Provide no additional text besides the list of hierarchies.

Current Hierarchies:
{current_hierarchies}

Format:
Hierarchy X: [description]; Hierarchy X+1: [next description];

Instructions:
Continue in this format for each hierarchy. Generate as many semicolon-separated hierarchies as necessary and finish with the new line.
'''
),
            ("human", '''''')
        ]
    )

# IDENTIFY ADDITIONAL HIERARCHIES BASED ON NEW INFORMATION
#
# Name: chat_template_find_additional_hierarchies
# Parameters: root_concept, current_hierarchies, context
# Description: Evaluates whether the current taxonomical hierarchies for the root concept remain sufficient in light of newly provided contextual information. If not, it generates concise descriptions for the minimal number of additional hierarchies needed to maintain classification completeness.
# Expected Result: Returns semicolon-separated descriptions of new hierarchies, each explaining its focus, purpose, and key property dimensions. If no additional hierarchies are needed, returns an empty response. Descriptions must follow a strict format and remain under 50 tokens.

chat_templates["find_additional_hierarchies"] = ChatPromptTemplate.from_messages(
        [
            ("system", '''Role: You are an expert in conceptual modeling and taxonomy.

Task:
You are provided with the current hierarchical classification descriptions for the root concept "{root_concept}".
You are also given new information that may affect the classification of "{root_concept}".
The goal is to improve the existing structure and move towards a well-structured taxonomy that fully classifies the root concept and its sub-concepts across multiple levels, either by confirming the sufficiency of the existing hierarchies or introducing new ones.
Examine the current hierarchies in light of the new information, and evaluate whether additional hierarchies are required based on this analysis.
If new hierarchies are required, identify the minimum number of new hierarchies needed to account for the newly provided information and maintain a coherent classification, then formulate and describe them.
If no new hierarchies are necessary, return an empty response.

Rules:
Each hierarchy description must be a single, concise block of text.
Each description must begin with the hierarchy’s name, followed by a colon (e.g., "Hierarchy 1: Evolutionary Classification: This hierarchy classifies biological species based on...").
The description should cover what the hierarchy deals with, its purpose, key property groups, and criteria used for classification (without specific examples). End with a brief summary of key criteria.
Keep each description under 50 tokens.
Never use semicolons (;)a nd newlines (\\n) in the descriptions.
Output only new hierarchies, omitting any existing ones.
Stop generating if irrelevant or nonsensical content is produced.
Always separate the hierarchies by semicolons (;) in the output.
Provide no additional text besides the list of hierarchies.

Current Hierarchies:
{current_hierarchies}

New information:
{context}

Format:
Hierarchy X: [description]; Hierarchy X+1: [next description];
             
Instructions:
Continue in this format for each hierarchy. Generate as many semicolon-separated hierarchies as necessary and finish with the new line.
'''
),
            ("human", '''''')
        ]
    )

# EXTRACT PRESENTLY REPRESENTED PROPERTIES FROM EXISTING HIERARCHIES
#
# Name: chat_template_find_present_features
# Parameters: root_concept, current_hierarchies
# Description: Analyzes the current set of hierarchical classification descriptions for a given root concept and extracts all unique properties or qualities that are explicitly represented in these hierarchies.
# Expected Result: Returns a semicolon-separated list of property names that are already covered by the provided hierarchies, with no explanations or duplicates.

chat_templates["find_present_features"] = ChatPromptTemplate.from_messages(
        [
            ("system", '''Role: You are a highly skilled scientific expert. 

Task:
I will provide you with a root concept and a list of hierarchies. Each hierarchy describes a classification system that organizes specific properties or qualities of the concept. Please analyze these hierarchies carefully and determine what properties of concepts they cover.

Context:
Root concept: {root_concept}

Hierarchies:
{current_hierarchies}

Rules:
Skip any explanations in the respond. Provide all unique key properties represented in hierarchies in the following semicolon separated format like this:
property 1; property 2; property 3

Instruction:
Continue in this format for each found property.
'''
),
            ("human", '''''')
        ]
    )

# IDENTIFY HIGHLY DISTINCTIVE FEATURES NOT COVERED BY EXISTING HIERARCHIES
#
# Name: chat_template_find_distinctive_features
# Parameters: root_concept, properties
# Description: Analyzes a list of properties already covered by existing hierarchies for the specified root concept, and identifies additional properties that are highly distinctive and introduce new dimensions of classification.
# Expected Result: Returns a semicolon-separated list of properties that are clearly different from the existing ones, enabling the expansion of taxonomy into new and non-overlapping classification criteria.

chat_templates["find_distinctive_features"] = ChatPromptTemplate.from_messages(
        [
            ("system", '''Role: You are a highly skilled scientific expert. 

Task:
I will provide you with a list of properties covered by existing hierarchies. Based on this list, identify properties that differ the most from the covered ones and that could introduce entirely new aspects of the concept.

Context:
Root concept: "{root_concept}"
Covered properties: 
{properties}

Rules:
Skip any explanations in the respond. Provide only highly distinct key properties in the following semicolon separated format like this:
property 1; property 2; property 3

Instruction:
Continue in this format for each found property.
'''
),
            ("human", '''''')
        ]
    )

# INTRODUCE NEW HIERARCHIES TO COVER ADDITIONAL PROPERTIES
#
# Name: chat_template_find_additional_hierarchies_for_features
# Parameters: root_concept, current_hierarchies, new_properties
# Description: Evaluates whether new properties not currently represented in existing hierarchies of the root concept require the creation of new classification hierarchies. If so, generates concise, non-redundant descriptions for the minimum number of new hierarchies needed to ensure full coverage.
# Expected Result: Returns semicolon-separated descriptions of additional hierarchies that integrate the new properties. Each description starts with a hierarchy name and concisely defines its classification purpose and key property groups. If all new properties are already covered, returns an empty response.

chat_templates["find_additional_hierarchies_for_features"] = ChatPromptTemplate.from_messages(
        [
            ("system", '''Role: You are an expert in conceptual modeling and taxonomy.

Task:
You are provided with the current hierarchical classification descriptions for the root concept "{root_concept}." Additionally, you are given a list of new properties that require integration into the taxonomy. Your objective is to evaluate the current hierarchies in light of these new properties and determine whether they are already covered or whether new hierarchies need to be introduced to account for them.
If the existing hierarchies are sufficient to cover these properties, provide an empty response. Otherwise, identify the minimum number of new hierarchies required to account for the newly provided properties to ensure the full classification of the root concept and its sub-concepts and maintain a coherent classification, then formulate and describe them.

Rules:
Each hierarchy description must be a single, concise block of text.
Each description must begin with the hierarchy’s name, followed by a colon (e.g., "Hierarchy 1: Evolutionary Classification: This hierarchy classifies biological species based on...").
The description should cover what the hierarchy deals with, its purpose, key property groups, and criteria used for classification (without specific examples). End with a brief summary of key criteria.
Keep each description under 50 tokens.
Never use semicolons (;)a nd newlines (\\n) in the descriptions.
Output only new hierarchies, omitting any existing ones.
Stop generating if irrelevant or nonsensical content is produced.
Always separate the hierarchies by semicolons (;) in the output.
Provide no additional text besides the list of hierarchies.

Current Hierarchies:
{current_hierarchies}

New Properties: 
{new_properties}

Format:
Hierarchy X: [description]; Hierarchy X+1: [next description];
             
Instructions:
Continue in this format for each hierarchy. Generate as many semicolon-separated hierarchies as necessary and finish with the new line.
'''
),
            ("human", '''''')
        ]
    )

# IDENTIFY UNIQUE CLASSIFICATION CRITERIA FOR ROOT CONCEPT
#
# Name: chat_template_get_criteria_basic
# Parameters: root_concept, context
# Description: Extracts a list of the most suitable and non-redundant classification criteria (distinctive properties) for organizing the root concept into taxonomical ranks. Ensures that the criteria are semantically unique and avoid overlapping features.
# Expected Result: Returns a comma-separated list of concise, clearly distinguishable criteria for taxonomic classification, based on the provided context and concept-specific distinctions.

chat_templates['get_criteria_basic'] = ChatPromptTemplate.from_messages(
        [
            ("system", '''Role: You are a highly skilled scientist and ontology expert.  
Task: To list the most appropriate criteria for classifying the "{root_concept}" root concept into taxonomical ranks. Ensure that the criteria are unique and avoid repetition of similar properties. Remember that a criterion is a distinct feature or property used to highlight differences between concepts while grouping similar ones based on shared attributes.  
Context: {context}  
Constraints: Skip explanations and return criteria in a comma-separated format, ensuring no redundant or similar criteria.
             '''
),
            ("human", '''''')
        ]
    )

# DISCARD REDUNDANT OR INCORRECT TAXONOMICAL CRITERIA LISTS
#
# Name: chat_template_discard_criteria
# Parameters: root_concept, context
# Description: Reviews multiple candidate lists of taxonomical classification criteria for the given root concept and identifies which lists are redundant, inaccurate, or unsuitable. Only the IDs of such lists are returned.
# Expected Result: Returns a comma-separated list of integer IDs (starting from 0) corresponding to the redundant or incorrect criteria lists. If no redundant lists are found, returns `None`.

chat_templates["discard_criteria"] = ChatPromptTemplate.from_messages(
        [
            ("system", '''Role: You are a highly skilled ontology expert.				
Task: Your goal is to diligently and painstakingly inspect every given list of taxonomical criteria from the provided context. Skip lists containing accurate distinctive differentiation criteria for the taxonomical classification of the {root_concept} root concept. You must find only IDs of the redundant, unnecessary or just wrong lists.

Context: Candidate lists are: 
{context}

Constraints: Provide the IDs (ID count starts from 0) of redundant lists in a comma-separated format or None if redundant lists are abscent.

Acceptable answers format exampes: 
0, 3, 5
None
1, 7, 3

Inacceptable answers format exampes (comma-separated): 
one, two, five,
"None"
1, 3-5,  
"6", "7" 
redundant lists are: ...
[l1,l2]
list, another list

'''),
            ("human", "Provide IDs of the redundant lists")
        
        ]
    )

# DEFINE TARGET CONCEPT WITHIN TAXONOMICAL CONTEXT
#
# Name: chat_template_define
# Parameters: root_concept, target_concept, target_rank, taxonomical_context
# Description: Generates a concise, accurate description of a target concept within a taxonomy, focusing on its defining characteristics and how its sub-classes differ from those of neighboring and parent concepts at the same hierarchical level. The definition emphasizes classification distinctions and contextualizes the target rank within the broader taxonomic structure.
# Expected Result: Returns a single descriptive string formatted as:
# Root Concept; Target Concept; Target Rank: [description of defining features, sub-class variations, and distinguishing aspects].
# The output must be compact, clearly structured, and avoid lists, explanations, or special formatting symbols.

chat_templates["define"] = ChatPromptTemplate.from_messages(
        [
            ("system", '''Role: 
You are a scientific expert specializing in "{root_concept}" classification.

Task: 
You will be provided with the taxonomy root concept name, target concept name, taxonomical rank of the target concept's sub-concepts ("Target Rank") and taxonomical ranks hierarchy. Analyze the provided context to clarify the broader taxonomical structure. You must generate an accurate and concise description of the target concept, target taxonomical rank, and the key features of the target concept sub-concepts of chosen rank. Highlight the key features and differences of the target concept's sub-classes in comparison to sub-classes of its parent concept (neighboring concepts at the previous hierarchical level). Also include information about target concept specifics in the context of the chosen "Target Rank".
Focus on how these differences help in distinguishing the sub-classes of the target concept at the "Target Rank" level. Keep the description simple, clear, and concise, emphasizing the distinctions between classification approach of the target concept compared to related higher-level concepts.

Constraints: 
Skip explanations. Provide only one fitting description. Include the root concept's name, target rank, most important specifics of both, and key differences that distinguish iits sub-classes from each other, as well as from the sub-classes of its parent and neighboring concepts. Avoid uncommon delimiters and special symbols, and do not use lists or extra spaces between symbols.

Examples: 

Root concept: Carnivora, Target Concept: Canidae, Target Rank: Genus
Taxonomical Rank Hierarchy: Order > Family > Genus > Species
Carnivora; Canidae; Genus: includes Canis (wolves, dogs), Vulpes (foxes), Lycaon (African wild dogs), and Cuon (dholes). Key traits of Canidae are long snouts, non-retractable claws, and strong social structures, especially in Canis. They rely on endurance hunting rather than ambush, have a strong sense of smell, and are typically omnivorous. Indicators of Canidae include bushy tails, forward-facing eyes for depth perception, a highly developed sense of smell and adaptability to diverse environments.

Root concept: NLP, Target Concept: Machine Translation, Target Rank: Language Model Used
Taxonomical Rank Hierarchy: Task > Approach > Language Model Used
NLP; Machine Translation; Language Model Used: includes statistical models, rule-based models, and neural machine translation (NMT) models. NMT models excel in fluency and context handling compared to statistical models. Sub-concepts differ by algorithmic complexity and their ability to manage long-range dependencies and ambiguity.

Root concept: Vehicles, Target Concept: Car, Target Rank: Fuel Type
Taxonomical Rank Hierarchy: Type > Category > Fuel Type > Engine Type
Vehicles; Car; Fuel Type: includes gasoline, electric, hybrid, hydrogen, and solar. Gasoline prioritizes power and range, while electric focuses on sustainability and lower emissions. Sub-concepts differ in energy efficiency, environmental impact, and refueling methods.

Root concept: Clothing, Target Concept: Jacket, Target Rank: Material
Taxonomical Rank Hierarchy: Type > Garment > Material > Insulation Type
Clothing; Jacket; Material: includes leather, wool, and synthetic. Leather provides durability, wool offers warmth, and synthetics are lightweight and water-resistant. Sub-concepts differ in weather resistance, breathability, and overall comfort'''
),
            ("human", '''Root concept: {root_concept}; Target Concept: {target_concept}; Target Rank: {target_rank}
Taxonomical Rank Hierarchy: {taxonomical_context}\n''')
        ]
    )

# GENERATE DISTINCTIVE SUB-CONCEPTS FOR TAXONOMY EXPANSION
#
# Name: chat_template_list_subconcepts
# Parameters: root_concept, concept, taxonomical_rank, taxonomical_context, context_string, subconcepts_amount
# Description: Generates a list of the most relevant and distinctive sub-concepts for a given target concept at a specified taxonomical rank. The sub-concepts must be exactly one level below the target concept and fit coherently into the overall taxonomical structure rooted in the specified root concept.
# Expected Result: Returns a comma-separated list of {subconcepts_amount} high-quality sub-concepts suitable for taxonomy construction. The results should be precise, non-redundant, and appropriate for the given rank and hierarchy level.

chat_templates["list_subconcepts"] = ChatPromptTemplate.from_messages(
        [
            ("system", '''Role: You are the best Taxonomical Classification expert in the whole world. And also you possess all available knowledge about "{root_concept}" classification.
Instruction: Use all your knowledge, expertise, and context, to perform excellent sub-concepts list generation. You will be given context, information about the taxonomical rank of target sub-concepts, and information about the root concept of taxonomy and the currently processed concept. First, analyze all available data, identify all the sub-concepts of the target concept and taxonomical rank, choose among them concepts matching the current taxonomy, and choose exactly the {subconcepts_amount} best distinctive accurate and correct concepts among them. Then provide those chosen concepts as a response. 
Here is the relevant context: {context_string}
Constraints: All generated sub-concepts must be part of the "{taxonomical_rank}" taxonomical rank in the taxonomy. The root concept of the taxonomy is the "{root_concept}" super-concept. We are currently at the "{taxonomical_rank}" level in the hierarchy ({taxonomical_context}). Use this information, to better understand the broader taxonomical structure, and generate new concepts more accurately and effectively. 
             '''),
            ("human", "The root concept of the current taxonomy is {root_concept}. List only the most important subconcepts of \"{concept}\" in the context of \"{taxonomical_rank}\". Those subconcepts should be used for iterative taxonomy construction, so you must include ONLY sub-concepts that are only one level lower in the hierarchy than \"{concept}\" concept. Don't include instances of {concept}! Skip explanations and use a comma-separated format like this: important subconcept, another important subconcept, another important subconcept, etc.")
        ]
    )

# DISCARD REDUNDANT SUB-CONCEPTS
#
# Name: chat_template_discard_subconcepts
# Parameters: root_concept, taxonomical_rank, taxonomical_context, candidate_list
# Description: Filters out redundant or incorrect sub-concepts from a provided list of candidates.
# Expected Result: Returns a comma-separated list of redundant sub-concepts.

chat_templates["discard_subconcepts"] = ChatPromptTemplate.from_messages(
        [
            ("system", '''Role:
You are the best AI taxonomy expert in the world — a genius ontologist, who possesses all available knowledge about the {root_concept} nature and classification. 
Context:
Scientists are developing a new valuable {root_concept} taxonomical classification. They have formed the list of candidate terms. Some of them must be inserted as concepts into the current taxonomy. However, some other candidates are unnecessary or redundant and must be discarded.
Instruction:
You must diligently and painstakingly inspect every given candidate from that list. Your goal is to find all redundant subcategory candidates and make a complete list of them. So later other members of the crew would be able to filter them out. 
Discard not all concepts but only needless ones.
If there are no redundant sub-concepts in the provided list - leave response empty.
Use all your knowledge, expertise, and context to find and select all redundant and wrong subcategories from the given list. Non-selected candidates must be accurate and correct in the context of {root_concept} taxonomical classification and current taxonomical rank. Candidate term must be considered as redundant either if it is not a {root_concept} sub-category, or if it is not an acceptable sub-concept of current taxonomical rank (We are currently at the "{taxonomical_rank}" level in the hierarchy ({taxonomical_context})). '''),
            ("human", "The list of candidates is \"{candidate_list}\". Provide the list of redundant subconcepts in a comma-separated format like this: redundant subconcept, other redundant subconcept, another redundant subconcept, etc."),
            ("ai", "Redundant sub-concepts: ")
        ]
    )

# POSTPROCESS SUB-CONCEPTS LIST FOR TARGET CONCEPT AND TAXONOMICAL RANK
#
# Name: chat_template_postprocess_subconcepts
# Parameters: root_concept, concept, context_string, taxonomical_rank, taxonomical_context
# Description: Refines and verifies the list of sub-concepts for the specified concept, ensuring they align with the given taxonomical rank and context.
# Expected Result: Returns a comma-separated list of true sub-concepts.

chat_templates["postprocess_subconcepts"] = ChatPromptTemplate.from_messages(
        [
            ("system", '''Role: 
You are an exceptional expert in Taxonomical Classification, possessing unparalleled knowledge about "{root_concept}".

Instruction: 
Use the provided context to accurately generate a list of true sub-concepts. You will be given the root concept, the taxonomical rank, and a list of sub-concept candidates. Your task is to correctly identify the true sub-concepts based on the combined information.
Constraints: 
Skip explanations. Provide the answer in a comma-separated format, listing only the true sub-concepts, like this: true subconcept, another true subconcept, etc. Ensure the final list follows a consistent format for all sub-concepts.

Examples: 
root concept: 'Software', taxonomical rank: 'User Interface Type', sub-concept candidates: 'GUI', 'CLI', 'VUI'. Provide the true sub-concepts.
Graphical User Interface (GUI) based Software, Command-Line Interface (CLI) Software, Software with Voice User Interface (VUI) support

root concept: 'Wound', taxonomical rank: 'Location', sub-concept candidates: 'Hands', 'Knees', 'Elbows'.  Provide the true sub-concepts.
Wounded Hand, Wounded Knee, Wounded Elbow 

root concept: 'Vehicle', taxonomical rank: 'Energy Source', sub-concept candidates: 'Gasoline', 'Electricity', 'Hydrogen'. Provide the true sub-concepts.
Gasoline-powered Vehicle, Electric Vehicle, Hydrogen-powered Vehicle.
             
root concept: 'Disease', taxonomical rank: 'Body System Affected', sub-concept candidates: 'Respiratory', 'Cardiovascular', 'Digestive'. Provide the true sub-concepts.
Respiratory Disease, Cardiovascular Disease, Digestive Disease.
             
root concept: 'Food', taxonomical rank: 'Cuisine', sub-concept candidates: 'Italian', 'Mexican', 'Japanese'. Provide the true sub-concepts.
Italian Cuisine, Mexican Cuisine, Japanese Cuisine.

'''),
            ("human", "root concept: '{root_concept}', taxonomical rank: '{taxonomical_rank}', sub-concept candidates: {subconcept_candidates}. Provide true sub-concepts.\n"),
#            ("ai", "true sub-concepts: ")
        ]
    )

# INTEGRATE SUB-CONCEPTS INTO TREE STRUCTURE
#
# Name: chat_template_integrate_subconcepts
# Parameters: root_concept, subconcepts
# Description: Converts a flat list of sub-concepts into a hierarchical tree structure rooted at the specified root concept. Each sub-concept may have its own nested sub-concepts, and the result is returned as a JSON object containing a nested dictionary under the key `"taxonomy"`.
# Expected Result: Returns a JSON object in the format:
# {
#   "taxonomy": {
#     "RootConcept": ["SubConcept1", "SubConcept2", ...],
#     "SubConcept1": ["NestedSubConceptA", ...],
#     ...
#   }
# }

chat_templates["integrate_subconcepts"] = ChatPromptTemplate.from_messages(
        [
            ("system", '''Return a JSON object with key 'taxonomy' and a value of dictionary with subconcepts tree structure. The tree should be a dictionary with keys as the names of the sub-concepts and values as lists of their sub-concepts. The tree should be structured in a way that each sub-concept is a key in the dictionary, and its value is a list of its sub-concepts. The root concept is {root_concept} and subconcepts are {subconcepts}.'''
),
            ("human", '''''')
        ]
    )

