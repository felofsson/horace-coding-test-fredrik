

import requests


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


if __name__ == "__main__":

    # 1
    # The user wants to be able to send in a query string that should be matched against
    # the contents of the title and body fields,
    #
    #Matching documents, filters and other result data, should be returned in JSON format






    #The service should only return a maximum of 100 docs per response
    # But there should be a way to get the full result list by executing
    # several requests and paging through the results (see pagination)
    test_pagination()

