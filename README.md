

# REST API for ElasticSearch image in Python
This project is based on the problem formulation given in the[Meltwater Horace Coding test](https://hub.docker.com/r/meltwater/horace-coding-test/). In that problem, a customer has specified the following requirement on a RESTful API:

1. The user wants to be able to send in a *query string* that should be *matched* against the contents of the *title* and *body* fields, 
    - Matching documents, filters and other result data, should be returned in JSON format_

2. The user wants to be able to *filter on sentiment* (i.e only see docs that are negative (*v*), positive (*p*), neutral (*n*)) or a combination of p,v,n
3.  The service should only return a maximum of 100 docs per response 
    - But there should be a way to get the full result list by executing several requests and paging through the results.

4. The user wants to be able to get back the *top N values from the keyPhrases field* for the documents matching the query, so he or she can make a word cloud.  


# Implementation and results
A Restful API has been implemented in Python, using Flask API and a Python module for Elastic search.

*Results*: 
- [x] Requirement 1 
- [x] Requirement 2 (partially)
- [x] Requirement 3

Requirement 4 has not been fulfilled. 

# Installation 
1. Install and configure the Docker container according to the orginal project
2. Clone/download this project
3. Install its dependencies found in requirements.txt (perferably in a virtual environment)
4. Start the Flask application by running ```restapi.py```
4. Run ```test.py``` to evaluate. 

# Usage
This REST api has one end-point:
```localhost:5002/search```, hereby shortend ```/search```

With parameters 
* ```str``` (the search string)
* ```size``` (number of documents to return (100 default))
* ```from``` (starting position of documents (0 default))
* ```sentiment``` (sentiment (either n, p or v), default None)

E. g.
```/search?str=my search string&size=150&from=50&sentiment=n```

## Examples

```/search?str=xc90```

Returns a JSON-object that matches the string "xc90". The matching documents from the search is stored in the JSON object ```data['hits']['hits']```. It is also accompanied with META-data from ElasticSearch (such as number of total hits).
(By default, the maximum number of hits are 100 unless specified otherwise by the ```size```-parameter) 

### Example with sentiment
The request ```/search?volvo&sentiment=p``` returns documents matching "volvo" AND has a positive sentiment. See below "A note on matching".


### Example with pagination

The request ```/search?str=volvo&size=10&from=0``` yields the first 10 matching documents to "volvo".
To retrieve the remaining matching documents (11-20), make the request ```/search?str=volvo&size=10&from=10```. 


## A note on matching
The matching is done by finding the search string in EITHER the document title or its body text. If the search string has several words (e. g. "volvo xc90"), documents returned does have at least both of those words in either the title, the body text, or both.

When searching by sentiment, the resulting document list is not correct (hence requirement 3 only partially fulfilled). The error most likely lies in the logic sent to the ElasticSearch image. Example: "volvo xc90" yields 42 hits. Forcing the sentiment to be positive ('p'), more than 100 hits are retrived. By inspection, these seem to have only "volvo" (only one of the two words) and a positive sentiment.  