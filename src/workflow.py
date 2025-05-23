import logging
from src.chat_templates import chat_templates
from src.models import Taxonomy

def create_taxonomy(model_generate_new, model_verify, concept = "Transistor", log = None):
    """
    Create a new taxonomy for a given concept using LLM-based prompts.

    Args:
        model_generate_new: Model used to generate new information.
        model_verify: Model used to verify and filter generated information.
        concept (str): The root concept for the taxonomy.
        log (logging.Logger, optional): Logger for info/debug output.

    Returns:
        Taxonomy: The constructed and initialized taxonomy object.
    """
    # Set up logging if not provided
    if not log:
        log = logging.getLogger("create_taxonomy")
        logging.basicConfig(level=logging.INFO)

    # Initialize the Taxonomy object with the root concept
    res = Taxonomy(concept)
    # For backward compatibility, also set a dict with root_concept (not used later)
    res = {
        "root_concept": concept,
    }

    log.info("\n\n\n\n+++++++++++++++++++++++++++\n\n\n+++++++++++++++++++=\n\n++++++++INITIAL CONTEXT++++++++\n(property groups, key features, unknown facts)\n+++++++++++++++++++++++++++\n\n\n+++++++++++++++++++=\n")

    # Step 1: Get property groups for the concept
    prompt = chat_templates['get_property_groups'].format_messages(root_concept = concept)
    res.responses.append(model_generate_new.invoke(prompt))
    # Clean up the property groups string
    res.property_groups = res.responses[-1].content.replace('\n',' ').replace('  ', ' ').strip()
    res.update_last_edit_time()
    res.update_token_usage(res.responses[-1].response_metadata['token_usage'])
    res.save()
    log.info(f"0.1.get_property_groups()\n-------------\nconcept:\t{concept}\n\n'property groups':\n{res.property_groups}\n")

    # Step 2: Get key aspects of the concept
    prompt = chat_templates['get_key_aspects'].format_messages(root_concept = concept)
    res.responses.append(model_generate_new.invoke(prompt))
    res.key_aspects = res.responses[-1].content
    res.update_last_edit_time()
    res.update_token_usage(res.responses[-1].response_metadata['token_usage'])
    res.save()
    log.info(f"0.2.get_key_aspects()\n-------------\nconcept:\t{concept}\n\n'key aspects':\n{res.key_aspects}\n")

    # Step 3: Get rare or obscure information about the concept
    prompt = chat_templates['get_rare_info'].format_messages(root_concept = concept)
    res.responses.append(model_generate_new.invoke(prompt))
    res.rare_info = res.responses[-1].content
    res.update_last_edit_time()
    res.update_token_usage(res.responses[-1].response_metadata['token_usage'])
    res.save()
    log.info(f"0.3.get_rare_info()\n-------------\nconcept:\t{concept}\n\n'rare info':\n{res.rare_info}\n")
    log.info("\n\n++++++++HIERARCHIES CONSTRUCT&UPDATE++++++++\n\n+++++++++++++++++++++++++++\n\n\n+++++++++++++++++++=\n")

    # Helper function to parse hierarchies string into a list
    def get_hierarchies_list(hierarchies_str):
        # Split by semicolon, remove empty/short entries, and add trailing semicolon
        return [v.strip()+';' for v in hierarchies_str.strip().replace('\n','').replace(';;',';').split(';') if len(v)>5]

    # Step 4: Construct initial hierarchies based on property groups
    prompt = chat_templates['get_initial_hierarchies'].format_messages(root_concept = concept, properties = res.property_groups)
    res.responses.append(model_generate_new.invoke(prompt))
    res.initial_hierarchies = res.responses[-1].content
    res.hierarchies = get_hierarchies_list(res['initial_hierarchies'])
    res.update_last_edit_time()
    res.update_token_usage(res.responses[-1].response_metadata['token_usage'])
    new_line = '\n'
    res.save()
    log.info(f"1.get_initial_hierarchies()...\n-------------\nconcept:\t{concept}\n\n'initial hierarchies list':\n{new_line.join(res.hierarchies)}\n\n")

    # Step 5: Find missing hierarchies (basic context)
    prompt = chat_templates['find_missing_hierarchies'].format_messages(root_concept = concept, current_hierarchies = '\n'.join(res.hierarchies))
    res.responses.append(model_generate_new.invoke(prompt))
    res.missing.append(res.responses[-1].content)
    res.hierarchies += get_hierarchies_list(res.missing[-1])
    res.update_last_edit_time()
    res.update_token_usage(res.responses[-1].response_metadata['token_usage'])
    res.save()
    log.info(f"2.find_missing_hierarchies()...\n-------------\nconcept:\t{concept}\n{len(get_hierarchies_list(res.missing[-1]))} new hierarchies found...\n'hierarchies new':\n{new_line.join(res.hierarchies)}\n\n")

    # Step 6: Find additional hierarchies using general key aspects as context
    current_hierarchies = '\n'.join(res.hierarchies)
    prompt = chat_templates['find_additional_hierarchies'].format_messages(root_concept = concept, context = res.key_aspects, current_hierarchies = current_hierarchies)
    res.responses.append(model_generate_new.invoke(prompt))
    res.missing.append(res.responses[-1].content)
    res.hierarchies += get_hierarchies_list(res.missing[-1])
    res.update_last_edit_time()
    res.update_token_usage(res.responses[-1].response_metadata['token_usage'])
    res.save()
    log.info(f"3.1.find_additional_hierarchies()...\ncontext = general key features info\n-------------\nconcept:\t{concept}\n{len(get_hierarchies_list(res.missing[-1]))} new hierarchies found...\n'hierarchies new':\n{new_line.join(res.hierarchies)}\n\n")

    # Step 7: Find additional hierarchies using rare info as context
    current_hierarchies = '\n'.join(res.hierarchies)
    prompt = chat_templates['find_additional_hierarchies'].format_messages(root_concept = concept, context = res.rare_info, current_hierarchies = current_hierarchies)
    res.responses.append(model_generate_new.invoke(prompt))
    res.missing.append(res.responses[-1].content)
    res.hierarchies += get_hierarchies_list(res.missing[-1])
    res.update_last_edit_time()
    res.update_token_usage(res.responses[-1].response_metadata['token_usage'])
    res.save()
    log.info(f"3.2.find_additional_hierarchies()...\ncontext = unknown rare features info\n-------------\nconcept:\t{concept}\n{len(get_hierarchies_list(res.missing[-1]))} new hierarchies found...\n'hierarchies new':\n{new_line.join(res.hierarchies)}\n\n")
    log.info("\n\n+++++++++++++++++++=\n+++++++++++++++++++++++++++\n+++++++++++++++++++=\n\n\n")

    # Step 8: Find present and distinctive features for the concept
    current_hierarchies = '\n'.join(res.hierarchies)
    # 8.1: Find present features
    prompt = chat_templates["find_present_features"].format_messages(root_concept = concept, current_hierarchies = current_hierarchies)
    res.responses.append(model_generate_new.invoke(prompt))
    res.present_features = res.responses[-1].content
    res.update_last_edit_time()
    res.update_token_usage(res.responses[-1].response_metadata['token_usage'])
    res.save()
    log.info(f"4.1.find_present_features()...\n-------------\nconcept:\t{concept}\n'present_features':\n{res.present_features}\n\n")

    # 8.2: Find distinctive features based on present features
    prompt = chat_templates["find_distinctive_features"].format_messages(root_concept = concept, properties = res.present_features)
    res.responses.append(model_generate_new.invoke(prompt))
    res.distinctive_features = res.responses[-1].content
    res.update_last_edit_time()
    res.update_token_usage(res.responses[-1].response_metadata['token_usage'])
    res.save()
    log.info(f"4.2.find_distinctive_features()...\n-------------\nconcept:\t{concept}\n'distinctive_features':\n{res.distinctive_features}\n\n")

    # Step 9: Update hierarchies again using distinctive features
    current_hierarchies = '\n'.join(res.hierarchies)
    prompt = chat_templates['find_additional_hierarchies_for_features'].format_messages(
        root_concept = concept,
        current_hierarchies = current_hierarchies,
        new_properties = res.distinctive_features
    )
    res.responses.append(model_generate_new.invoke(prompt))
    res.missing.append(res.responses[-1].content)
    res.hierarchies += get_hierarchies_list(res.missing[-1])
    res.update_last_edit_time()
    res.update_token_usage(res.responses[-1].response_metadata['token_usage'])
    res.save()
    log.info(f"5.1.find_additional_hierarchies()...\ncontext = distinct properties\n-------------\nconcept:\t{concept}\n{len(get_hierarchies_list(res.missing[-1]))} new hierarchies found...\n'hierarchies new':\n{new_line.join(res.hierarchies)}\n\n")

    # Step 10: For each hierarchy, extract taxonomical ranks (criteria)
    res.ranks = []
    for hierarchy in res.hierarchies:
        prompt = chat_templates['get_criteria_basic'].format_messages(root_concept = concept, context = hierarchy)
        res.responses.append(model_generate_new.invoke(prompt))
        # Split the response into a list of rank names
        res.ranks.append([v.strip() for v in res.responses[-1].content.split(",")])
        res.update_last_edit_time()
        res.update_token_usage(res.responses[-1].response_metadata['token_usage'])
        res.save()

    log.info(f"-------------\n\n'initial ranks':\n{res.ranks}\n")

    # Step 11: Discard redundant or irrelevant criteria using the verification model
    prompt = chat_templates["discard_criteria"].format_messages(root_concept = concept, context = res.ranks)
    res.responses.append(model_verify.invoke(prompt))
    # Remove ranks at indices specified by the model's response
    res.ranks = [v for i, v in enumerate(res.ranks) if i not in [int(n.strip()) for n in res.responses[-1].content.split(",")]]
    # Initialize depths and subconcept containers for each rank
    res.depths = [0 for v in res['ranks']]
    res.subconcepts_plain = [[] for v in res.ranks]
    res.subconcepts_trees = [{} for v in res.ranks]
    res.update_last_edit_time()
    res.update_token_usage(res.responses[-1].response_metadata['token_usage'])
    res.save()
    log.info(f"-------------\n\n'filtered ranks':\n{res.ranks}\n")

    # Return the fully initialized taxonomy object
    return res

def generate_subconcepts(
    model_generate_new, 
    model_re_generate, 
    taxonomy: Taxonomy, 
    ranks_list_num: int, 
    stop_at_depth: int = None, 
    max_subconcepts_per_iteration: int = 15, 
    log = None
):
    # Set up logging if not provided
    if not log:
        log = logging.getLogger("generate_subconcepts")
        logging.basicConfig(level=logging.INFO)

    # Determine the maximum depth to iterate through
    if stop_at_depth:
        max_depth = stop_at_depth
    else: 
        max_depth = len(taxonomy.ranks[ranks_list_num])

    i = 0  # Current depth/iteration index
    taxonomical_context = taxonomy.ranks[ranks_list_num][0]  # Start with the first rank as context
    target_concept = taxonomy.root_concept  # Start with the root concept

    # Iterate through each rank up to the maximum depth
    while i < max_depth:
        # 1. Generate a definition for the current concept at this rank
        prompt = chat_templates["define"].format_messages(
            root_concept = taxonomy.root_concept, 
            target_concept = target_concept, 
            target_rank = taxonomy.ranks[ranks_list_num][i], 
            taxonomical_context = taxonomical_context
        )
        definition_response = model_generate_new.invoke(prompt, max_tokens=200)
        context_string = " " + definition_response.content  # Use the definition as context

        # 2. Generate a list of candidate subconcepts for the current rank
        prompt = chat_templates["list_subconcepts"].format_messages(
            root_concept = taxonomy.root_concept, 
            concept = target_concept, 
            context_string = context_string, 
            taxonomical_rank = taxonomy.ranks[ranks_list_num][i], 
            taxonomical_context = taxonomical_context, 
            subconcepts_amount = max_subconcepts_per_iteration
        )
        taxonomy.responses.append(model_generate_new.invoke(prompt, max_tokens=200))
        # Parse the response into a list of subconcepts, filtering out overly long entries
        subconcepts_list = [v.strip() for v in taxonomy.responses[-1].content.split(',') if len(v) <= 120]
        taxonomy.update_last_edit_time()
        taxonomy.update_token_usage(taxonomy.responses[-1].response_metadata['token_usage'])
        taxonomy.save()
        log.info(f"generated concepts at iteration {i}: {subconcepts_list}\n")
        
        # 3. Identify and remove redundant subconcepts using the re-generation model
        prompt = chat_templates["discard_subconcepts"].format_messages(
            root_concept = taxonomy.root_concept, 
            taxonomical_rank = taxonomy.ranks[ranks_list_num][i], 
            taxonomical_context = taxonomical_context, 
            candidate_list = subconcepts_list
        )
        taxonomy.responses.append(model_re_generate.invoke(prompt, max_tokens=200))
        redundant_subconcepts = [v.strip() for v in taxonomy.responses[-1].content.split(',') if len(v) <= 120]
        taxonomy.update_last_edit_time()
        taxonomy.update_token_usage(taxonomy.responses[-1].response_metadata['token_usage'])
        taxonomy.save()
        log.info(f"redundant subconcepts list: {redundant_subconcepts}\n")
        
        # Normalize redundant subconcepts for case-insensitive comparison
        redundant_subconcepts = [subconcept.lower() for subconcept in redundant_subconcepts]
        # Filter out redundant subconcepts from the candidate list
        subconcepts_list = [subconcept for subconcept in subconcepts_list if subconcept.lower() not in redundant_subconcepts]
        
        # 4. Post-process the filtered subconcepts for final refinement
        prompt = chat_templates["postprocess_subconcepts"].format_messages(
            root_concept = taxonomy.root_concept, 
            taxonomical_rank = taxonomy.ranks[ranks_list_num][i],
            subconcept_candidates = subconcepts_list
        )
        taxonomy.responses.append(model_re_generate.invoke(prompt, max_tokens=300))
        subconcepts_list = [v.strip() for v in taxonomy.responses[-1].content.split(',') if len(v) <= 120]
        taxonomy.update_last_edit_time()
        taxonomy.update_token_usage(taxonomy.responses[-1].response_metadata['token_usage'])
        log.info(f"postprocessed concepts: {subconcepts_list}\n")
        
        # 5. Add the final subconcepts to the taxonomy's plain list for this rank
        taxonomy.subconcepts_plain[ranks_list_num] += subconcepts_list
        # Set the target concept for the next iteration to the current subconcepts
        target_concept = subconcepts_list
        
        i += 1  # Move to the next depth/rank
        taxonomy.depths[ranks_list_num] += 1  # Increment the depth for this rank
        taxonomy.save()
        # Update the taxonomical context for the next iteration
        taxonomical_context += " > " + taxonomy.ranks[ranks_list_num][i]
    return taxonomy

def generate_subconcepts_for_all_ranks(
    model_generate_new, 
    model_re_generate, 
    taxonomy: Taxonomy, 
    stop_at_depth: int = None, 
    max_subconcepts_per_iteration: int = 15, 
    log = None
):
    """
    Generate subconcepts for all taxonomical ranks in the taxonomy.

    Args:
        model_generate_new: Model used to generate new concepts.
        model_re_generate: Model used to refine and filter concepts.
        taxonomy (Taxonomy): The taxonomy object to expand.
        stop_at_depth (int, optional): Maximum depth to generate subconcepts for each rank.
        max_subconcepts_per_iteration (int): Maximum number of subconcepts to generate per iteration.
        log (logging.Logger, optional): Logger for info/debug output.

    Returns:
        Taxonomy: The updated taxonomy with generated subconcepts.
    """
    if not log:
        log = logging.getLogger("generate_subconcepts_for_all_ranks")
        logging.basicConfig(level=logging.INFO)
    # Iterate through all available ranks in the taxonomy
    for i in range(len(taxonomy.ranks)):
        # Generate subconcepts for the current rank using the helper function
        taxonomy = generate_subconcepts(
            model_generate_new, 
            model_re_generate, 
            taxonomy, 
            i, 
            stop_at_depth, 
            max_subconcepts_per_iteration, 
            log
        )
        # Log the depth reached for the current rank
        log.info(f"depth of rank {taxonomy.ranks[i]}: {taxonomy.depths[i]}")
        # Save the taxonomy state after processing each rank
        taxonomy.save()
    return taxonomy

def integrate_subconcepts(
    model_integrate, 
    taxonomy: Taxonomy, 
    log = None
):
    """
    Integrate the generated subconcepts into the taxonomy structure using a model.

    Args:
        model_integrate: Model used to integrate subconcepts into a hierarchical structure.
        taxonomy (Taxonomy): The taxonomy object containing subconcepts.
        log (logging.Logger, optional): Logger for info/debug output.

    Returns:
        Taxonomy: The updated taxonomy with integrated subconcept trees.
    """
    if not log:
        log = logging.getLogger("integrate_subconcepts")
        logging.basicConfig(level=logging.INFO)
    # Iterate through all ranks in the taxonomy
    for i in range(len(taxonomy.ranks)):
        # Prepare the prompt for integrating subconcepts for the current rank
        prompt = chat_templates["integrate_subconcepts"].format_messages(
            root_concept = taxonomy.root_concept, 
            subconcepts = taxonomy.subconcepts_plain[i]
        )
        # Invoke the integration model to build the hierarchical structure
        taxonomy.responses.append(model_integrate.invoke(prompt))
        # Store the resulting taxonomy tree for the current rank
        taxonomy.subconcepts_trees[i] = taxonomy.responses[-1]['taxonomy']
        # Update metadata and save the taxonomy state
        taxonomy.update_last_edit_time()
        taxonomy.update_token_usage(taxonomy.responses[-1].response_metadata['token_usage'])
        taxonomy.save()
    return taxonomy
