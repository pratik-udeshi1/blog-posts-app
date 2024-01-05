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
