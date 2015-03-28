import json
import urllib
import nltk
import random
import Tkinter
from Tkinter import *
from PIL import Image, ImageTk

### CONSTANTS & HELPER CLASSES ###

## General UI Constants
TITLE = 'HermioneBot'
userName = ''
isFirstInteraction = True
background_image = Image.open('hermione.jpg')

## General URL API constants
WIKIA_API_URL = 'https://www.harrypotter.wikia.com/api/v1'
SEARCH_URI = '/Search/List/?'
ARTICLES_URI = '/Articles/AsSimpleJson?'
QUERY_RESULT_LIMIT = 25
SEARCH_QUERY_TEMPLATE = {'query' : '', 'limit' : QUERY_RESULT_LIMIT}
ARTICLE_QUERY_TEMPLATE = {'id': ''}

## Helper classes and constants for linguistic computations
class Intent:
	QUERY = 1
	STATEMENT = 2
	UNKNOWN = 3
	DEVIOUS = 4

## Pre-defined responses to statements and undecipherable user questions
GREETING = 'I\'m Hermione Granger and you are?'
WELCOME = 'Pleasure.'
RESPONSE_NOT_QUESTION = ['I\'m sorry but that is simply not a question!']
SPELLING_ERROR = ['It\'s \%s not \%s!']
NAGGING = ['I really shouldn\'t be doing this.', 'I told you that was a bad idea.']
DEFAULT_RESPONSE = ''



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
		submitQuestion = Button(gui, text="Ask Hermione", command= lambda: submitInput(userEntry, response))
		submitQuestion.place(x=985, y=600)
		gui.mainloop()


## LINGUISTIC UNDERSTANDING ##
## Section which takes the user's input and deciphers the user's intention
## using POS-tagging and semantic inference techniques

##
##
def submitInput(userEntry, systemResponse):
	userInput = userEntry.get(0.0, END)
	print(userInput)
	response = DEFAULT_RESPONSE

	if isFirstInteraction :
		global userName
		global isFirstInteraction
		userName = userInput.rstrip('\n')
		response = WELCOME
		isFirstInteraction = False
	else :
		intent = obtainUserIntent(userInput)
		if intent == Intent.QUERY :
			response = deviseResponse(userInput)
		elif intent == Intent.STATEMENT :
			response = "%s, %s" % (userName, RESPONSE_NOT_QUESTION[random.randint(0, len(RESPONSE_NOT_QUESTION)-1)])
		
		# User's Intent DEVIOUS

	systemResponse.set(response)

## TODO
##
def obtainUserIntent(input):
	return Intent.STATEMENT

## TODO
##
def deviseResponse(query):
	pass


## API INTERFACING ##
## Section which provides the methods necessary to interface with the wikia API
## Includes querying for article suggestions and optaining articles all in json format

## TODO
##
def queryWikia(query):

	SEARCH_QUERY_TEMPLATE['query'] = query
	encodedQuery = urllib.urlencode(SEARCH_QUERY_TEMPLATE)
	result = json.loads(URL + query.encode('utf-8'))	

	## TODO: determine how to handle multiple query results

## TODO
##
def refineWikiaArticleContent():
	pass

##
##
if __name__ == '__main__' :
	HermioneUI()


