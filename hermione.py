import json
import urllib
import nltk
import pyjs
from pyjamas.ui import usedUIComponents


### CONSTANTS & HELPER CLASSES ###


## General UI Constants
hermione = HermioneGUI()
TITLE = 'Hermione Bot'
SUBTITLE = ''
userName = ''
isFirstInteraction = True
usedUIComponents = ['TextBox', 'RootPanel', 'Label']


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
class HermioneInputBox(TextBox):

	## 
	##
	def onKeyPress(self, sender, keycode, modifiers): 
		if (keycode == KEY_ENTER):
			self.setReadonly(True)
			submitInput(self.getText())
			self.setReadonly(False)
			resetText(self)
	##
	##		
	def resetText(self):
		self.setText('')

##
##
class HermioneGUI():
	
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
		userInput = HermioneInputBox()
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

##
##
def obtainUserIntent(input) :

##
##
def deviseResponse(query) :


## API INTERFACING ##
## Section which provides the methods necessary to interface with the wikia API
## Includes querying for article suggestions and optaining articles all in json format

##
##
def queryWikia(query) :

	SEARCH_QUERY_TEMPLATE['query'] = query
	encodedQuery = urllib.urlencode(SEARCH_QUERY_TEMPLATE)
	result = json.load(URL + query.encode('utf-8'))	

##
##
def refineWikiaArticleContent() :

##
##
if __name__ == '__main__' :
		hermione.onModuleLoad

