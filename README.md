# TaxoRankExpand

TaxoRankExpand is an automated taxonomy generation tool that leverages large language models (LLMs) to construct, expand, and integrate hierarchical taxonomies for any root concept. It uses the [LangChain](https://github.com/langchain-ai/langchain) framework and OpenAI models to iteratively build and refine taxonomical structures.

## Features

- **Automated Taxonomy Creation:** Generates property groups, key aspects, rare features, and initial hierarchies for a given concept.
- **Iterative Expansion:** Expands taxonomies by generating and refining subconcepts for each rank.
- **Integration:** Merges generated subconcepts into a hierarchical tree structure.
- **Persistence:** Saves taxonomy objects for later inspection or reuse.
- **Logging:** Detailed logging of each step for transparency and debugging.

## Project Structure

- `main.py`: Entry point for running taxonomy generation.
- `src/models.py`: Contains the `Taxonomy` class, model initialization, and session management.
- `src/workflow.py`: Implements the workflow for taxonomy creation, expansion, and integration.
- `src/chat_templates.py`: Defines prompt templates for LLM interactions.
- `requirements.txt`: Python dependencies.

## Installation

1. Clone the repository.
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
    
## Usage

1. Set your OpenAI API key in main.py:
2. Run the main script:
    ```sh
    python main.py
    ```
3. The script will:
 - Initialize models and logging.
 - Create a taxonomy for the specified concept (default: "Transistor").
 - Expand the taxonomy up to a specified depth.
 - Integrate subconcepts into a hierarchical structure.
 - Save results and logs in the data/taxonomies/ and logs/ directories.

## Customization

 - Change the root concept by modifying the concept variable in main.py.
 - Adjust taxonomy depth and number of subconcepts per iteration via stop_at_depth and max_subconcepts_per_iteration.

## Requirements

 - Python 3.8+
 - openai
 - langchain
 - langchain-openai

## License

MIT License

### For more details, see the source code in the src/ directory.