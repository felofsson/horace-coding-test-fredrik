def make_es_query(search_str, from_, size, sentiment):
    """Returns ElasticSearch query for search_str,
        Matches fields
            'title'
            'body'

        If search_str is several words, e. g. "volvo xc90",
        the whitespace is assumed to be an AND and the
        query ensures BOTH "volvo" and "xc90" to be present in
        EITHER 'title' or 'body'.


    """

    # init
    query_dict = {"query": {"bool": {
        "should": []
    }
    }
    }

    search_fields = ['title', 'body']
    for field in search_fields:
        query_dict['query']['bool']['should'].append({'match': {field: {'query': search_str,
                                                                        'operator': 'and'}}})

    if sentiment is not None:
        query_dict['query']['bool']['filter'] = {"match": {"sentiment": sentiment}}

    query_dict['size'] = size
    query_dict['from'] = from_

    return query_dict


def es_search(search_str, from_=0, size=100, sentiment=None):
    """Searches for search_str and returns the documents
    matching in the ElasticSearch image.

    See make_es_query for details about how the search is done."""

    from elasticsearch import Elasticsearch

    es = Elasticsearch(['localhost:9200/'])

    query_dict = make_es_query(search_str, from_, size, sentiment)

    res = es.search(index="documents", body=query_dict)

    return res


if __name__ == "__main__":


    d = es_search("volvo xc90", sentiment='p')

    print(d['hits']['total'])

    for hit in d['hits']['hits']:
        print(hit)





