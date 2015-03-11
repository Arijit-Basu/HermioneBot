from enum import Enum
import json
import urllib
import nltk

### CONSTANTS & HELPER CLASSES ###

## General URL API constants
WIKIA_API_URL = 'https://www.harrypotter.wikia.com/api/v1'
SEARCH_URI = '/Search/List/?'
ARTICLES_URI = '/Articles/AsSimpleJson?'
QUERY_RESULT_LIMIT = 25
SEARCH_QUERY_TEMPLATE = {'query' : '', 'limit' : QUERY_RESULT_LIMIT}
ARTICLE_QUERY_TEMPLATE = {'id': ''}

## Helper classes and constants for linguistic computations
class Intents(Enum):
	QUERY = 1
	STATEMENT = 2
	UNKNOWN = 3

## Pre-defined responses to statements and undecipherable user questions
GREETINGS = ['Hello there, my name is Hermione']
RESPONSE_NOT_QUESTION = ['']
SPELLING_ERROR = ['It\'s \%s not \%s']

### CORE FUNCTIONALITY ###

## GUI ## 
## Section which builds the basic structure for the Hermione GUI, reads from stdin 
## and prints to stdout

##
##
##
##
def buildHermione() :

##
##
##
##
def chat() :


##
##
##
## 
def shutdownHermione() :


## LINGUISTIC UNDERSTANDING ##
## Section which takes the user's input and deciphers the user's intention
## using POS-tagging and semantic inference techniques

##
##
##
##
def obtainUserIntent(input) :


##
##
##
##
def deviseResponse(userIntent, refinedQuery) :


## API INTERFACING ##
## Section which provides the methods necessary to interface with the wikia API
## Includes querying for article suggestions and optaining articles all in json format

##
##
##
##
def queryWikia(query) :

	SEARCH_QUERY_TEMPLATE['query'] = query
	encodedQuery = urllib.urlencode(SEARCH_QUERY_TEMPLATE)
	result = json.load(URL + query.encode('utf-8'))	


##
##
##
##
def refineWikiaArticleContent() :

