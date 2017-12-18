# Team Horace coding test

## Elasticsearch data image
An Elasticsearch v5.6.3 image prepackaged with data is available at https://hub.docker.com/r/meltwater/horace-coding-test/

```
# Start the Elasticsearch container with the coding test dataset preloaded
sudo docker run -p 9200:9200 -p 9300:9300 meltwater/horace-coding-test:latest
```

The documents that we are interested in are in the *documents* index and all docs are of *document* type. You can use

```
curl "localhost:9200/documents/_search?pretty=true" 
```

to see how the indexed data looks like.

Example doc:

```json
{
    "title": "Volvo S80 2007 deadlock noise",
    "body": "The volvo s80 car seems to be giving a deadlock noise when I push it hard",
    "keyPhrases": [
        "Volvo",
        "S80",
        "noise"],
    "sentiment": "n"
}
```

Note that the documents are in many different languages, not only english.

## Problem description

### The search UI

The customer wants to build a search application looking like this:

*Note:* you **do not** have to create any UI parts for this assignment - focus on the *REST API*.

```
+-----------------------------------------------------------------------+
|                                               Show only docs          |
|     Query:                                    with sentiment          |
|   +--------------------------------------+     +---+---+---+          |
|   |  search query input field            |     | p | n | v |          |
|   +--------------------------------------+     +---+---+---+          |
|                                                                       |
|     Result list:                                    Word cloud:       |
|   +--------------------------------------+    +-------------------+   |
|   |                                      |    |                   |   |
|   |    <title of result #1>       p      |    |                   |   |
|   |        text text text                |    |    Volvo          |   |
|   | -------------------------------------|    |                   |   |
|   |                                      |    |          Sweden   |   |
|   |    <title of result #2>       n      |    |                   |   |
|   |        text text text                |    |  XC60             |   |
|   | -------------------------------------|    |                   |   |
|   |                                      |    |                   |   |
|   |                                      |    |            V90    |   |
|   |                                      |    | Gothenburg        |   |
|   |                                      |    |                   |   |
|   |                                      |    |                   |   |
|   |                                      |    +-------------------+   |
|   |                                      |                            |
|   |                                      |                            |
|   +--------------------------------------+                            |
|                                                                       |
|                                                                       |
+-----------------------------------------------------------------------+
```

- In the query form field the user can insert a string
- On enter (or dynamically as the user types), the result list and the word cloud, is updated with the matching documents 
- The query language syntax is up to you - but no complex boolean syntax is required, choose something simple
- In the result list part the *title*, *body* and the *sentiment* fields of the matching documents are displayed
- In the sentiment filter to the upper right, the user can click check boxes for positive (p), neutral (n) and negative (v) sentiment. The result is filtered to only show docs that matches
- In the lower/middle right part a word cloud is displayed with the most relevant key phrases for the matching documents (taken from the *keyPhrases* field)


### Your task

Using the provided elasticsearch image with pre-loaded data we want you to create a *RESTful web service* with *JSON* responses serving the *search API* on top of elasticsearch. There's no need to create an actual web-UI, only the REST API and service that drives the UI is needed.

The API design is up to you, but imagine that another team, in another time zone, will build the web UI on top of your service.


### Non functional requirements:

- You can use any language, framework and build tool you want. Consider choosing something you're comfortable and productive with.
- Add a short documentation on how to build, run and test your service locally
    - Assume that we have started the provided docker image locally
    - Assume that we can test your API with curl, and/or whatever testing tools/scripts/uis you provide together with the code or its documentation
- The request format and URL endpoints/http methods etc is up to you to design, but the responses should be JSON in some form
- Deployment architecture is out of scope - assume that it will be run locally for now 
- It is a plus if you give us the original git repo history (with more than 1 commit) so we can see how the code evolved over time 

### Requested functionality

The below is a list of requirements given by 'the customer' - implement as much as you can in the given time frame.

- The user wants to be able to send in a *query string* that should be *matched* against the contents of the *title* and *body* fields, 
    - Matching documents, filters and other result data, should be returned in JSON format
- The user wants to be able to *filter on sentiment* (i.e only see docs that are negative (*v*), positive (*p*), neutral (*n*)) or a combination of p,v,n
- The user wants to be able to get back the *top N values from the keyPhrases field* for the documents matching the query, so he or she can make a word cloud. (see [terms aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html) ) 
- The service should only return a maximum of 100 docs per response 
    - But there should be a way to get the full result list by executing several requests and paging through the results (see [pagination](https://www.elastic.co/guide/en/elasticsearch/guide/master/pagination.html))
