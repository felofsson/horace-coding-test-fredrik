

import requests


def test_connectivity():
    r = requests.get("http://127.0.0.1:5002/search?str=volvo")

    print("Attempting a get at endpoint, status code: %s, (200 = good :) )" % r.status_code)


def test_pagination():


    total_size = 100
    search_str = "volvo"  # Has to match more than total size

    print("Testing pagination of %s documents. search_str = %s" % (total_size, search_str))

    # Getting all in the same query
    params = {'str': search_str, 'size': total_size, 'from': 0}
    r = requests.get("http://127.0.0.1:5002/search", params=params)
    data = r.json()

    list_of_hits = data['hits']['hits']

    # Getting all one-by-one
    list_of_hits2 = []
    for from_no in range(0, total_size):
        params = {'str': search_str, 'size': 1, 'from': from_no}
        r = requests.get("http://127.0.0.1:5002/search", params=params)
        data = r.json()
        list_of_hits2.append((data['hits']['hits'][0]))

    # Getting all by pagination
    list_of_hits3 = []
    start_no = 0
    end_no = total_size
    pagination_size = 10

    while start_no < total_size:
        params = {'str': search_str, 'size': pagination_size, 'from': start_no}
        r = requests.get("http://127.0.0.1:5002/search", params=params)
        data = r.json()
        list_of_hits3.extend((data['hits']['hits']))

        start_no = start_no + pagination_size

    count = 0
    for (item1, item2, item3) in zip(list_of_hits, list_of_hits2, list_of_hits3):
        if item1['_id'] == item2['_id']:
            if item2['_id'] == item3['_id']:
                count = count + 1

    print("...%s of %s equal when testing pagination." % (count, total_size))


def test_search():

    print("Testing search with several keywords. Should be present in either BODY, TITLE or both.\n")
    search_str = "volvo xc90"  # Has to match more than total size

    params = {'str': search_str, }
    r = requests.get("http://127.0.0.1:5002/search", params=params)
    data = r.json()

    words_to_match = search_str.split()  # split by space

    count = 0
    matching_count = 0


    fields = ['body', 'title']
    matching_dict = {}

    matching_dict['body'] = 0
    matching_dict['title'] = 0
    matching_dict['both_body_title'] = 0
    matching_dict['none'] = 0

    for document in data['hits']['hits']:
        count = count + 1
        body_text = document['_source']['body']
        title_text = document['_source']['title']

        all_words_in_all_fields = True
        res = {}
        for field in fields:
            res[field] = False
            text = document['_source'][field]

            all_words_in_field = True # assumption

            for word in words_to_match:
                if not(word.lower() in text.lower()):
                    all_words_in_field = False

            res[field] = all_words_in_field

        if res['body'] and res['title']:
            matching_dict['both_body_title'] += 1

        elif res['body']:
            matching_dict['body'] += 1
        elif res['title']:
            matching_dict['title'] += 1
        else:
            matching_dict['none'] += 1


        all_words_in_field = True  # default

        for word in words_to_match:
            if not (word in body_text.lower() or word in title_text.lower()):
                all_words_in_field = False

        if all_words_in_field:
            matching_count += 1



    print("...Total documents matched %s, of which %s contained %s in the BODY text, TITLE text or both." % (
    count, matching_count, words_to_match))
    print("...Distribution::")
    print("...", matching_dict)
    print("...(Summarizes to %s)" % (matching_dict['body'] + matching_dict['title'] + matching_dict['both_body_title']))


def test_search_sentiment():

    search_str = "volvo xc90"  # Has to match more than total size
    print("Testing search for a specific sentiment (search_str = %s)" % search_str)

    sentiment_list = ['n','p','v', None]

    for sentiment in sentiment_list:

        params = {'str': search_str, 'sentiment': sentiment, 'size': 100}
        r = requests.get("http://127.0.0.1:5002/search", params=params)

        data = r.json()


        print("...sentiment: %s - Matched total of %s documents\n" %  (sentiment, len(data['hits']['hits'])))


if __name__ == "__main__":

    """Tests features of the REST api"""

    #Testing connectivity
    test_connectivity()

    # The user wants to be able to send in a query string that should be matched against
    # the contents of the title and body fields,
    #
    #Matching documents, filters and other result data, should be returned in JSON format
    test_search()


    #The user wants to be able to filter on sentiment 
    # (i.e only see docs that are negative (v), positive (p),
    # neutral (n)) or a combination of p,v,n
    test_search_sentiment()


    #The service should only return a maximum of 100 docs per response
    # But there should be a way to get the full result list by executing
    # several requests and paging through the results (see pagination)
    test_pagination()

