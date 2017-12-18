


# {
#   "name" : "_s2y5_v",
#   "cluster_name" : "docker-cluster",
#   "cluster_uuid" : "l5lfJXWdTnKVsIe93ir99g",
#   "version" : {
#     "number" : "5.6.3",
#     "build_hash" : "1a2f265",
#     "build_date" : "2017-10-06T20:33:39.012Z",
#     "build_snapshot" : false,
#     "lucene_version" : "6.6.1"
#   },
#   "tagline" : "You Know, for Search"
# }

# https://marcobonzanini.com/2015/02/02/how-to-query-elasticsearch-with-python/

# The REST API for search is accessible from the _search endpoint. This example returns
# all documents in the bank index:

# https://stackoverflow.com/questions/17309889/how-to-debug-a-flask-app
# https://www.codementor.io/sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq

# Cut off frequency
# https://www.elastic.co/guide/en/elasticsearch/reference/1.4/query-dsl-match-query.html


# {
#     "title": "Volvo S80 2007 deadlock noise",
#     "body": "The volvo s80 car seems to be giving a deadlock noise when I push it hard",
#     "keyPhrases": [
#         "Volvo",
#         "S80",
#         "noise"],
#     "sentiment": "n"
# }

def make_es_query(search_str):
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

    # print(query_dict)
    return query_dict


def es_search(search_str):

    from elasticsearch import Elasticsearch

    es = Elasticsearch(['localhost:9200/'])

    query_dict = make_es_query(search_str)

    res = es.search(index="documents", body=query_dict)

    return res


if __name__ == "__main__":


    d = es_search("volvo xc90")

    for hit in d['hits']['hits']:
        print(hit)
    



