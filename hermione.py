## Resources for querying API and parsing results
import json
import urllib
import urllib2

## Resources for performing POS tagging & lamda expressions
from nltk.parse import ShiftReduceParser
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize

## GUI Resources
import Tkinter
from Tkinter import *
from PIL import Image, ImageTk

## General Resources
import random



### CONSTANTS & HELPER CLASSES ###

## General UI Constants
TITLE = 'HermioneBot'
userName = ''
isFirstInteraction = True
background_image = Image.open('hermione.jpg')

## General URL API constants
WIKIA_API_URL = 'http://www.harrypotter.wikia.com/api/v1'
SEARCH_URI = '/Search/List/?'
ARTICLES_URI = '/Articles/AsSimpleJson?'
QUERY_RESULT_LIMIT = 25
SEARCH_QUERY_TEMPLATE = {'query' : '', 'limit' : QUERY_RESULT_LIMIT}
ARTICLE_QUERY_TEMPLATE = {'id': ''}

## Helper classes and constants for linguistic computations
class Intent:
	QUERY = 1
	STATEMENT = 2
	NONSENSE = 3
	DEVIOUS = 4

## Pre-defined responses to statements and undecipherable user questions
GREETING = 'I\'m Hermione Granger and you are?'
WELCOME = 'Pleasure.'
RESPONSE_TO_NONSENSE = ['I\'m sorry but that is simply not a question!']
SPELLING_ERROR = ['It\'s \%s not \%s!']
NAGGING = ['I really shouldn\'t be doing this.', 'I told you that was a bad idea.']
MUST_ENTER_INPUT = ''
NO_INFORMATION_AVAILABLE = ''



### CORE FUNCTIONALITY ###

## GUI ## 
## Section which builds the basic structure for the Hermione GUI, reads from stdin 
## and prints to stdout

##
##
class HermioneUI:

	##
	##
	def __init__(self):

		# Basic GUI & Layout initialization 
		gui = Tkinter.Tk()
		gui.title(TITLE)

		# Set Background
		background = ImageTk.PhotoImage(background_image)
		background_label = Tkinter.Label(gui, image=background)
		background_label.place(x=0, y=0, relwidth=1, relheight=1)
		gui.wm_geometry("1250x685+20+40")

		# Response Text Area
		response = StringVar()
		responseLabel = Label(gui, textvariable=response, anchor='nw', font=("Helvetica", 20), bg='white', fg='black', wraplength=200)
		response.set(GREETING)
		responseLabel.place(x=930, y=125, relwidth=.175, relheight=.35)	

		# User Text Area
		userEntry = Text(gui, font=("Helvetica", 16), bg='white', bd=0, highlightcolor="white", fg='black')
		userEntry.place(x=950, y=525, relwidth=.15, relheight=.1)
		submitButton = Button(gui, text="Reply", command= lambda: submitInput(userEntry, response, submitButton))
		submitButton.place(x=985, y=600)
		gui.mainloop()


## LINGUISTIC UNDERSTANDING ##
## Section which takes the user's input and deciphers the user's intention
## using POS-tagging and semantic inference techniques

##
##
def submitInput(userEntry, systemResponse, submitButton):
	userInput = userEntry.get(0.0, END).rstrip('\n')
	
	## TEMP: to see & verify POS tagging
	print(userInput)

	response = ''

	# If the user did not input anything then return the default response
	if userInput == '':
		response = MUST_ENTER_INPUT 

	# On first user input then store the input as their username
	elif isFirstInteraction :
		global userName
		global isFirstInteraction
		userName = userInput
		response = WELCOME
		isFirstInteraction = False
		submitButton.config(text='Ask Hermione')

	# Otherwise - determine the user's intent based one POS tagged sentence 
	# and devise an answer, rebuttle or appropriate reply
	else :
		
		## Perform POS-tagging on user input
		tagged_input = pos_tag(word_tokenize(userInput))
		print(tagged_input)
		intent = obtainUserIntent(tagged_input)
		
		if intent == Intent.QUERY :
			response = deviseAnswer(tagged_input)
		elif intent == Intent.STATEMENT :
			response = deviseRebuttle(tagged_input)
		elif intent == Intent.NONSENSE :
			response = "%s, %s" % (userName, RESPONSE_TO_NONSENSE[random.randint(0, len(RESPONSE_TO_NONSENSE)-1)])
		# TODO: User's Intent DEVIOUS - easter egg

	systemResponse.set(response)

## TODO
##
def obtainUserIntent(taggedInput):

	intent = Intent.NONSENSE	

	## If the sentence ends with a question mark or starts with a Wh-pronoun or adverb
	## then safely assume it is a question
	if isQuestion(taggedInput):
		intent = Intent.QUERY

	else :
		intent = Intent.STATEMENT

	return intent

## TODO
##
def isQuestion(taggedInput):

	## Helper Information
	firstWordTag = taggedInput[0][1]
	lastToken = taggedInput[len(taggedInput)-1][0]

	# If starts with WH or ends with ? -- it is a question
	if firstWordTag.startswith('WP') or (firstWordTag.startswith('WRB') or lastToken == '?'):
		return True

	return False

## TODO
##
def isStatement(taggedInput):
	pass



## TODO
##
def deviseAnswer(taggedInput):

	# Answer to reply with 
	answer = NO_INFORMATION_AVAILABLE
	
	# TEMP: Find the noun after the verb - handles who/what is/are ... 
 	foundVerb = False
	query = ''
	for item in taggedInput:
		if item[1].startswith('V') and not foundVerb :
			foundVerb = True
		elif foundVerb and not item[1] == '.':
			query += ' '
			query += item[0]

	# First query wikia to get possible matching articles
	articleID = queryWikiaSearch(query)
	
	# If the search result did not return anything respond with no results respone 
	if articleID:
		answer = queryWikiaArticle(articleID)

	# Return result
	return answer


## TODO
##
def deviseRebuttle(taggedInput):
	pass

## API INTERFACING ##
## Section which provides the methods necessary to interface with the wikia API
## Includes querying for article suggestions and optaining articles all in json format

## TODO
##
def queryWikiaSearch(query):

	articleID = ''

	# Format Search Query URL
	SEARCH_QUERY_TEMPLATE['query'] = query
	searchUrl = WIKIA_API_URL
	searchUrl += SEARCH_URI
	searchUrl += urllib.urlencode(SEARCH_QUERY_TEMPLATE)
	
	# Open URL and fetch json response data
	results = urllib2.urlopen(searchUrl)
	resultData = json.load(results)
	
	# If there is a response then take the first result article
	# and return the url
	if resultData['total'] > 0 :
		articleID = resultData['items'][0]['id']

	print(articleID)
	return articleID

## TODO
##
def queryWikiaArticle(articleID):

	answer = ''
	
	# Format Article URL
	ARTICLE_QUERY_TEMPLATE['id'] = articleID
	articleUrl = WIKIA_API_URL
	articleUrl += ARTICLES_URI
	articleUrl += urllib.urlencode(ARTICLE_QUERY_TEMPLATE)

	# Open URL and fetch json response text
	results = urllib2.urlopen(articleUrl)
	resultData = json.load(results)
	print(resultData)

	# TODO: Optimize answer refinement
	# Right now - just fetches first sentence of first section of text
	answer = sent_tokenize(resultData['sections'][0]['content'][0]['text'].replace('b.', 'born'))[0]

	return answer


## TODO
##
def refineWikiaArticleContent():
	pass

##
##
if __name__ == '__main__' :
	HermioneUI()


