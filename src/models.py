import os
import logging
import pickle
import datetime

import openai
from langchain_openai import ChatOpenAI

def ensure_directory_exists(path):
    """
    Ensure that the directory at the given path exists.
    If it does not exist, attempt to create it.
    Print status messages for success or failure.
    """
    # Validation: Check if the directory exists
    if not os.path.exists(path):
        try:
            # Directory creation
            os.makedirs(path)
            print(f"Directory created: {path}")
        except OSError as error:
            print(f"Error creating directory: {error}")
    else:
        print(f"Directory already exists: {path}")

class Taxonomy:
    """
    Class representing a taxonomy structure for organizing concepts.
    Stores metadata, hierarchical information, and methods for persistence.
    """
    def __init__(self, root_concept:str) -> None:
        # Record creation and last edit timestamps
        self.created_at             = datetime.datetime.now()
        self.last_edit_time         = datetime.datetime.now()
        # Generate a unique name for the taxonomy based on creation time
        self.name                   = 'Taxonomy_'+str(self.created_at).replace(' ','_T').replace(':','-')[:22]
        # Default save path for taxonomy files
        self.save_path              = os.getcwd()+"\\data\\taxonomies\\"
        # List of file paths where the taxonomy has been saved
        self.saved_to               = [self.save_path + self.name + '.pkl']
        # Track token usage for LLM interactions
        self.token_usage            = {'completion_tokens': 0, 'prompt_tokens': 0, 'total_tokens': 0}
        # Store the root concept of the taxonomy
        self.root_concept           = root_concept
        # Initialize token usage statistics
        self.token_usage = {
            'completion_tokens': 0,
            'prompt_tokens': 0,
            'total_tokens': 0
        }
        
        # Various properties for taxonomy construction and analysis
        self.property_groups = ""
        self.key_aspects = ""
        self.rare_info = ""
        self.initial_hierarchies = ""
        self.present_features = ""
        self.distinctive_features = ""
        
        # Lists for hierarchical and structural data
        self.hierarchies = []
        self.missing = []
        self.ranks = []
        self.subconcepts_plain = []
        self.subconcepts_trees = []
        self.depths = []
        self.responses = []
    
    def update_token_usage(self, token_usage_delta) -> None:
        """
        Update the token usage statistics by adding values from token_usage_delta.
        """
        for key in self.token_usage.keys():
            self.token_usage[key] += token_usage_delta[key]
    
    def update_last_edit_time(self) -> None:
        """
        Update the last_edit_time to the current time.
        """
        self.last_edit_time = datetime.datetime.now()

    def save(self, suffix = "") -> str:
        """
        Save the taxonomy object to a pickle file.
        Ensures the save directory exists.
        Returns the full path to the saved file.
        """
        ensure_directory_exists(self.save_path)
        full_path = self.save_path + self.name + suffix + '.pkl'
        with open(full_path, 'wb') as file:
            pickle.dump(self, file)
        if not full_path in self.saved_to:
            self.saved_to.append(full_path) 
        return full_path    
    
    def info(self) -> str:
        """
        Return a formatted string with detailed information about the taxonomy.
        Includes metadata and hierarchical structure.
        """
        info = f'''
Taxonomy info:
Created at: {self.created_at}
Last edited at: {self.last_edit_time}
Name: {self.name}
Saved to: {self.saved_to[-1]}
Save path: {self.save_path}
Property groups: {self.property_groups}
Key aspects: {self.key_aspects}
Rare info: {self.rare_info}
Initial hierarchies: {self.initial_hierarchies}
Present features: {self.present_features}
Distinctive features: {self.distinctive_features}
Root concept: {self.root_concept}
Hierarchies: {self.hierarchies}
Missing: {self.missing}
Token Usage: {self.token_usage}
'''
        for i, rank in enumerate(self.ranks):
            info += f'''
    Rank: {rank}
Sub-concepts: {self.subconcepts_plain[i]}
Sub-concept tree: {self.subconcepts_trees[i]}
Depth: {self.depths[i]}
'''
        return info

    @staticmethod
    def load(file_path:str) -> 'Taxonomy':
        """
        Load a Taxonomy object from a pickle file at the given file_path.
        Returns the loaded Taxonomy instance.
        """
        with open(file_path, 'rb') as file:
            taxonomy = pickle.load(file)
        return taxonomy
        
class Model:
    """
    Wrapper class for initializing a Large Language Model (LLM) with specific parameters.
    Stores configuration and provides access to the underlying model.
    """
    def __init__(self, name:str, model_checkpoint:str, temperature = 1, top_p = 1, presence_penalty = 1, frequency_penalty = 0) -> None:
        # Initialize the LLM with the provided parameters
        self.model              = ChatOpenAI(
                model               = model_checkpoint, 
                temperature         = temperature, 
                top_p               = top_p, 
                presence_penalty    = presence_penalty, 
                frequency_penalty   = frequency_penalty
            )
        self.name               = name
        self.temperature        = temperature
        self.model_checkpoint   = model_checkpoint
        self.top_p              = top_p
        self.presence_penalty   = presence_penalty
        self.frequency_penalty  = frequency_penalty
        # Store a formatted string with model configuration info
        self.info               = f'''model name: {name}
model checkpoint: {model_checkpoint}
temperature: {temperature}
top p: {top_p}
presence penalty: {presence_penalty}
frequency penalty: {frequency_penalty}'''

def start_session(api_key = None): 
    """
    Initialize logging, create a log file, and set up the OpenAI API key.
    Returns the logger instance.
    """
    start_time = datetime.datetime.now()
    log = logging.getLogger("TaxoRankExpand")
    logs_path = os.getcwd()+"\\logs\\"
    ensure_directory_exists(logs_path)
    log_name = 'TaxoRankExpand_0.1__'+str(start_time).replace(' ','_').replace(':','-')[:21]+'.log'
    logging.basicConfig(filename=logs_path+log_name, level=logging.INFO)
    log.info("start_session()")
    # Set your OpenAI API key
    if not api_key:
        log.info("OPENAI API KEY NOT PROVIDED!!")
    else:
        os.environ["OPENAI_API_KEY"] = api_key
    openai.api_key = os.environ["OPENAI_API_KEY"]
    return log

def init_models(log = None):
    """
    Initialize and configure multiple LLM models for different taxonomy construction tasks.
    Returns the initialized model instances.
    """
    if not log:
        log = logging.getLogger("init_models()")
        logging.basicConfig(level=logging.INFO)
    log.info(f"init_models()..")
    
    # Verification model: Used for verifying taxonomy data
    llm_verify              = Model('verify',       'gpt-4o-mini',  
                                    temperature = 0.9,    top_p = 0.90,   presence_penalty = 1.00,   frequency_penalty = 0.00) 
    log.info(f"{llm_verify.info}\nmodel init successfully..")
    model_verify            = llm_verify.model
    
    # Re-Generation model: Used for regenerating or refining taxonomy data
    llm_re_generate         = Model('re-generate',  'gpt-4o-mini',
                                    temperature = 1.3,    top_p = 0.90,   presence_penalty = 0.50,   frequency_penalty = 1.00)
    log.info(f"{llm_re_generate.info}\nmodel init successfully..")
    model_re_generate       = llm_re_generate.model
    
    # New concept generation model: Used for generating new taxonomy concepts
    llm_generate_new        = Model('generate new',  'gpt-4o',
                                    temperature = 1.0,    top_p = 0.98,   presence_penalty = 1.00,   frequency_penalty = 1.20)
    log.info(f"{llm_generate_new.info}\nmodel init successfully..")
    model_generate_new      = llm_generate_new.model
    
    # Integration model: Used for integrating taxonomy data, with structured JSON output
    model_integrate = Model('integrate',  'gpt-4o-mini',
                                    temperature = 1.3,    top_p = 0.90,   presence_penalty = 0.50,   frequency_penalty = 1.00).model.with_structured_output(method="json_mode")
    
    log.info(f"model_generate_new, model_re_generate, model_verify models initialized")
    return model_generate_new, model_re_generate, model_verify, model_integrate
