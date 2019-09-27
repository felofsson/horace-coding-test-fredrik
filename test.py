import requests

ELASTIC_SEARCH_PATH = "http://127.0.0.1:5002/search"


def test_connectivity():
    r = requests.get(ELASTIC_SEARCH_PATH + "?str=volvo")

    print("Attempting a get at endpoint, status code: %s, (200 = good :) )" % r.status_code)

    print("\n")


def test_pagination():
    """Retrives documents from the search image in 2 different ways,
        1. All at the same time
        2. By "smarter" pagination, by 10s and 10s

        Stores the result from each query, and compares the documents by id. """

    override_total_size = 1000
    search_str = "volvo"  # Has to match more than total size

    print("Testing pagination of max %s documents. search_str = %s" % (override_total_size, search_str))

    # Getting all in the same query
    params = {'str': search_str, 'size': override_total_size, 'from': 0}
    r = requests.get(ELASTIC_SEARCH_PATH, params=params)
    data = r.json()

    list_of_hits = data['hits']['hits']
    total_num_hits = len(list_of_hits)

    # Getting all by pagination
    list_of_hits_by_pagination = []
    start_no = 0
    pagination_size = 10

    while start_no < override_total_size:
        params = {'str': search_str, 'size': pagination_size, 'from': start_no}
        r = requests.get(ELASTIC_SEARCH_PATH, params=params)
        data = r.json()
        list_of_hits_by_pagination.extend((data['hits']['hits']))

        if len(data['hits']['hits']) == 0: # Stop retrieving more documents when there is no longer any result
            break

        start_no = start_no + pagination_size

    count = 0

    # Compare the id's of documents, retrived in two different ways
    for (item1, item2) in zip(list_of_hits, list_of_hits_by_pagination):
        if item1['_id'] == item2['_id']:
                count = count + 1

    print("...%s of %s equal when testing pagination." % (count, total_num_hits))


def test_search():

    print("Testing search with several keywords. Should be present in either BODY, TITLE or both.\n")
    search_str = "volvo xc90"  # Has to match more than total size

    params = {'str': search_str, 'size': 10000}
    r = requests.get(ELASTIC_SEARCH_PATH, params=params)
    data = r.json()

    words_to_look_for = search_str.split()  # split by space

    matching_count = 0

    for document in data['hits']['hits']:
        body_text = document['_source']['body']
        title_text = document['_source']['title']

        # We expect to find a match in either body, title or both for ANY of the search str's words
        text = (body_text + " " + title_text).lower()

        for word in words_to_look_for:
            if word.lower() in text:
                matching_count = matching_count + 1
                break

    print("We found search_str words present in " + str(matching_count) + " documents")
    print("Total number of documents matched by ES: " + str(len(data['hits']['hits'])))


def test_search_sentiment():

    search_str = "volvo xc90"  # Has to match more than total size
    sentiment_list = ['n', 'p', 'v', None]

    print("Testing search for a specific sentiments")
    print(sentiment_list)
    print("search_str = %s" % search_str)

    sentiment_counter = dict()

    for sentiment in sentiment_list:

        params = {'str': search_str, 'sentiment': sentiment, 'size': 1000}
        r = requests.get(ELASTIC_SEARCH_PATH, params=params)

        data = r.json()

        sentiment_counter[sentiment] = len(data['hits']['hits'])

    print("Distribution:")
    print(sentiment_counter)
    print("Sum of n, p, v = " + str(sum([sentiment_counter[k] for k in sentiment_counter if k is not None])))

    print("\n")


if __name__ == "__main__":

    """Tests features of the REST api"""

    # Testing connectivity
    test_connectivity()

    # The user wants to be able to send in a query string that should be matched against
    # the contents of the title and body fields,
    test_search()


    # The user wants to be able to filter on sentiment 
    # (i.e only see docs that are negative (v), positive (p),
    # neutral (n))
    test_search_sentiment()

    #The service should only return a maximum of 100 docs per response
    # But there should be a way to get the full result list by executing
    # several requests and paging through the results (see pagination)
    test_pagination()
