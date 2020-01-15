import Model.fact_dict as fact_container_dict


def get_list_of_facts():
    """used to obtain the details(keys) of the facts extracted"""
    keys = []

    # unit the 3 dict obtained through the fact collection
    all_dict = {**fact_container_dict.facts_on_phrases, **fact_container_dict.facts_on_quotes,
                **fact_container_dict.facts_on_colon}

    for key in all_dict:
        keys.append(key)

    return keys