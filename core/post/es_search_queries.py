def custom_search_query(search_query):
    return {
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "title": {
                                "query": search_query,
                                "operator": "and",
                                "boost": 2.0
                            }
                        }
                    },
                    {
                        "match": {
                            "content": {
                                "query": search_query,
                                "operator": "and"
                            }
                        }
                    },
                    {
                        "fuzzy": {
                            "content": {
                                "value": search_query,
                                "fuzziness": 2
                            }
                        }
                    }
                ]
            }
        }
    }


def custom_search_query2(search_query):
    return {
        "query": {
            "multi_match": {
                "query": search_query,
                "fields": ["title^{}".format(10.0), "content"],
                "type": "best_fields",  # Change the type as needed (best_fields, most_fields, cross_fields)
                "tie_breaker": 0.3  # Adjust the tiebreaker value as needed
            }
        }
    }
