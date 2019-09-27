
ELASTIC_SEARCH_IMAGE = "localhost:9200/"  # See Readme for search image reference


def make_es_query(search_str, from_, size, sentiment_flag=None):
    """Returns ElasticSearch query for search_str,
        Matches fields
            'title'
            'body'
            'sentiment' (if sentiment_flag is provided)
    """

    # init
    query_dict = {'query': {'bool': {'must': []}}}

    body_title_query = {
        "bool": {
            "should": [{
                "match": {
                    "title": search_str
                }
            }, {
                "match": {
                    "body": search_str
                }
            }]
        }
    }

    query_dict['query']['bool']['must'].append(body_title_query)

    if sentiment_flag is not None:
        sentiment_query = {
            "bool": {
                "filter": [{
                    "term": {
                        "sentiment": sentiment_flag
                    }
                }]
            }
        }

        query_dict['query']['bool']['must'].append(sentiment_query)

    query_dict['size'] = size
    query_dict['from'] = from_

    return query_dict


def es_search(search_str, from_=0, size=100, sentiment_flag=None):
    """Searches for search_str and returns the documents
    matching in a ElasticSearch image.

    See make_es_query for details about how the search is done."""

    from elasticsearch import Elasticsearch

    es = Elasticsearch([ELASTIC_SEARCH_IMAGE])

    query_dict = make_es_query(search_str, from_, size, sentiment_flag)

    res = es.search(index="documents", body=query_dict)

    return res
