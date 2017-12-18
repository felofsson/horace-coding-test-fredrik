def make_es_query(search_str, from_, size):
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

    query_dict['size'] = size
    query_dict['from'] = from_

    # print(query_dict)
    return query_dict


def es_search(search_str, from_=0, size=100):

    from elasticsearch import Elasticsearch

    es = Elasticsearch(['localhost:9200/'])

    query_dict = make_es_query(search_str, from_, size)

    res = es.search(index="documents", body=query_dict)

    return res


if __name__ == "__main__":


    d = es_search("volvo xc90")

    print(d['hits']['total'])

    for hit in d['hits']['hits']:
        print(hit)




