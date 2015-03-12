from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.Label import Label
from pyjamas.ui.RootPanel import RootPanel
import json
import urllib
import nltk
import pyjs


### CONSTANTS & HELPER CLASSES ###


## General UI Constants
hermione = HermioneUI()
TITLE = 'Hermione Bot'
SUBTITLE = ''
userName = ''
isFirstInteraction = True


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


## Pre-defined responses to statements and undecipherable user questions
GREETING = 'Hello, I\'m Hermione Granger and you are?'
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
class InputBox(TextBox):

	## 
	##
	def onKeyPress(self, sender, keycode, modifiers): 
		if (keycode == KEY_ENTER):
			self.setReadonly(True)
			submitInput(self.getText())
			self.setReadonly(False)
			self.resetText()
	##
	##		
	def resetText(self):
		self.setText('')

##
##
class HermioneUI():
	
	##
	##
	def onModuleLoad(self):
		title = Label().setText(TITLE)
		title.setText(TITLE)
		hermioneOutput = TextBox()
		hermioneOutput.setText(GREETING)
		hermioneOutput.setStyleName('hermione-output-box')
		hermioneOutput.setReadonly(True)
		hermioneOutput.setVisibleLength('1000px')
		hermioneOutput.setWidth('500px')
		userInput = InputBox()
		userInput.setText("")
		userInput.setVisisbleLength('200px')
		userInput.setWidth('500px')
		userInput.addInputListener(UserInputListener())
		userInput.setStyleName('user-input-box')
		mainPanel = RootPanel().add(hermioneOutput, userInput)
		mainPanel.setSpacing(15)


## LINGUISTIC UNDERSTANDING ##
## Section which takes the user's input and deciphers the user's intention
## using POS-tagging and semantic inference techniques

##
##
def submitInput(input):
	response = DEFAULT_RESPONSE

	if isFirstInteraction :
		userName = userText
		response = WELCOME
		isFirstInteraction = False
	else :
		intent = obtainUserIntent(userText)
		if intent == Intent.QUERY :
			response = deviseResponse(userText)
		elif intent == Intent.STATEMENT :
			response = DEFAULT_RESPONSE		

	hermione.hermioneOutput.addText(response)

## TODO
##
def obtainUserIntent(input):
	pass

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
	result = json.load(URL + query.encode('utf-8'))	

	## TODO: determine how to handle multiple query results

## TODO
##
def refineWikiaArticleContent():
	pass


##
##
if __name__ == '__main__' :
	hermione.onModuleLoad()

