# Import necessary functions from the src.models and src.workflow modules
from src.models import init_models, start_session
from src.workflow import create_taxonomy, generate_subconcepts_for_all_ranks, integrate_subconcepts

# Set the API key for authentication with the external service (e.g., OpenAI)
api_key = "your_api_key_here"  # Replace with your actual API key

# Start a logging session using the provided API key
log = start_session(api_key = api_key) 

# Initialize the models required for taxonomy generation and processing
# Returns four models: for generating, re-generating, verifying, and integrating concepts
model_generate_new, model_re_generate, model_verify, model_integrate = init_models(log)

# Define the root concept for which the taxonomy will be created
concept = "Transistor"

# Create the initial taxonomy structure for the given concept using the generation and verification models
taxonomy = create_taxonomy(model_generate_new, model_verify, concept, log)

# Set the maximum depth to which the taxonomy will be expanded
stop_at_depth = 3

# Set the maximum number of subconcepts to generate per iteration
max_subconcepts_per_iteration = 15

# Expand the taxonomy by generating subconcepts for all ranks up to the specified depth and limit
taxonomy = generate_subconcepts_for_all_ranks(
    model_generate_new, 
    model_re_generate, 
    taxonomy, 
    stop_at_depth, 
    max_subconcepts_per_iteration, 
    log
)

# Integrate the generated subconcepts into the taxonomy using the integration model
taxonomy = integrate_subconcepts(model_integrate, taxonomy, log)

# Log the final taxonomy structure using the info method of the taxonomy object
log.info(f"Final Taxonomy: {taxonomy.info()}")