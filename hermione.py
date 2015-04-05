## Resources for querying API and parsing results
import json
import urllib
import urllib2

## Resources for performing POS tagging & lamda expressions
from nltk import RegexpParser
from nltk.data import load
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

grammar = r"""
	NP: {<DT|PRP\$>?<JJ>*<NN|NNS>+}
		{<NNP>+}
		{<PRP>}
		{<WP|WP\$|WRB>}
	VP: {<VB|VBD|VBG|VBN|VBP|VBZ|MD><NP|IN>?}
"""
parser = RegexpParser(grammar)

## Pre-defined responses to statements and undecipherable user questions
GREETING = 'I\'m Hermione Granger and you are?'
WELCOME = 'Pleasure.'
RESPONSE_TO_NONSENSE = ['I\'m sorry but that is simply not a question!']
SPELLING_ERROR = ['It\'s \%s not \%s!']
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
		responseLabel = Label(gui, textvariable=response, anchor='nw', font=("Helvetica", 16), bg='white', fg='black', wraplength=200)
		response.set(GREETING)
		responseLabel.place(x=920, y=105, relwidth=.175, relheight=.425)	

		# User Text Area
		userEntry = Text(gui, font=("Helvetica", 14), bg='white', bd=0, highlightcolor="white", fg='black')
		userEntry.place(x=950, y=525, relwidth=.15, relheight=.1)
		submitButton = Button(gui, text="Reply", command= lambda: submitInput(userEntry, response, submitButton))
		submitButton.place(x=990, y=600)
		gui.mainloop()


## LINGUISTIC UNDERSTANDING ##
## Section which takes the user's input and deciphers the user's intention
## using POS-tagging and semantic inference techniques

##
##
def submitInput(userEntry, systemResponse, submitButton):
	userInput = userEntry.get(0.0, END).rstrip('\n')
	userEntry.delete(0.0, END)
	
	## TEMP: to see & verify POS tagging
	print("User Input : %s" % userInput)

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
		print("POS-Tagged User Input : %s " % tagged_input)
		intent = obtainUserIntent(tagged_input)
		
		if intent == Intent.QUERY :
			print("HERMIONE IS THINKING...")
			response = deviseAnswer(tagged_input)
		elif intent == Intent.STATEMENT :
			print("HERMIONE IS VERIFYING...")
			response = deviseRebuttle(tagged_input)
		elif intent == Intent.NONSENSE :
			print("HERMIONE THINKS YOU ARE UNCLEAR...")
			response = "%s, %s" % (userName, RESPONSE_TO_NONSENSE[random.randint(0, len(RESPONSE_TO_NONSENSE)-1)])

	systemResponse.set(response)

## This method takes the POS tagged user input and determines what the intention of the user was
## returns Intent.NONSENSE, Intent.QUERY or Intent.STATEMENT
##
def obtainUserIntent(taggedInput):

	intent = Intent.NONSENSE	

	## If the sentence ends with a question mark or starts with a Wh-pronoun or adverb
	## then safely assume it is a question
	if isQuestion(taggedInput):
		intent = Intent.QUERY
	elif isStatement(taggedInput):
		intent = Intent.STATEMENT

	return intent

## This method checks that the POS-tagged input suggests that the user has asked a question
## returns True or False
##
def isQuestion(taggedInput):

	## Helper Information
	firstWordTag = taggedInput[0][1]
	lastToken = taggedInput[len(taggedInput)-1][0]
	lastWordTag = taggedInput[len(taggedInput)-1][1]
	secondLastWordTag = taggedInput[len(taggedInput)-2][1]

	# If starts or ends with WH, ends with ? or starts with Auxilliary verb -- it is a question
	if firstWordTag.startswith('WP') or (firstWordTag.startswith('WRB') or lastToken == '?'):
		return True
	elif lastWordTag.startswith('WP') or lastWordTag.startswith('WP'):
		return True
	elif secondLastWordTag.startswith('WP') or secondLastWordTag.startswith('WP'):
		return True
	elif (firstWordTag.startswith('VBZ') or firstWordTag.startswith('VBP')) or firstWordTag.startswith('MD'):
		return True

	return False

## This method checks that the POS-tagged input suggests that the user has input a statement
## returns True or False
##
def isStatement(taggedInput):
	
	## First parse the information to find the NPs and verify that starts with NP followed by verb phrase
	result = parser.parse(taggedInput)
	subtrees = result.subtrees()
	
	i = 0
	for subtree in subtrees:
		if i == 1 and not subtree.label() == 'NP':
			break
		if i == 2 and subtree.label() == 'VP':
			return True
		i = i + 1

	return False

## TODO
##
def deviseAnswer(taggedInput):

	# Default Answer
	answer = NO_INFORMATION_AVAILABLE

	result = parser.parse(taggedInput)
	print("Regexp Parser Result for input %s : " % taggedInput),
	print(result)
	
	# Determine the query to enter into the wikia search and add any additional 
	# search terms now so that when article refinement is performed the most accurate reply is returned
	queries = []
	additionalSearchKeywords = []

	## GENERAL STRATEGY:
	## Look through tagged input then fetch whole sentence fragments through subtrees.
	## 1. If starts with Auxillary Verb then take the first NP as the query 
	## and everything to the right becomes additional search keywords.
	## 2. If starts with WH-NP then take rightmost NP and everything in between becomes 
	## additional search keywords
	## 3. If ends with WH-NP then take first NP and everything in between becomes 
	## additional search keywords

	queryPhraseType = 3

	## Helper Information
	firstWordTag = taggedInput[0][1]
	lastToken = taggedInput[len(taggedInput)-1][0]
	lastWordTag = taggedInput[len(taggedInput)-1][1]
	secondLastWordTag = taggedInput[len(taggedInput)-2][1]

	if firstWordTag.startswith('WP') or firstWordTag.startswith('WRB'):
		queryPhraseType = 2
	elif lastWordTag.startswith('WP') or lastWordTag.startswith('WP'):
		queryPhraseType = 3
	elif secondLastWordTag.startswith('WP') or secondLastWordTag.startswith('WP'):
		queryPhraseType = 3
	elif (firstWordTag.startswith('VBZ') or firstWordTag.startswith('VBP')) or firstWordTag.startswith('MD'):
		queryPhraseType = 1

	i = 0
	for subtree in result.subtrees():

		# Skip the first subtree (which is the entire tree)
		if i == 0:
			i = i + 1
			continue
		
		if queryPhraseType == 2 or queryPhraseType == 1:
			if i == 1:
				i = i + 1
				continue
			elif subtree.label() == 'NP':
				queries.append(' '.join([str(a[0]) for a in subtree.leaves()]))
			else:
				additionalSearchKeywords.append(' '.join([str(a[0]) for a in subtree.leaves()])) 

		else:
			if subtree.label() == 'NP':
				queries.append(' '.join([str(a[0]) for a in subtree.leaves()]))
			elif not i == 0:
				additionalSearchKeywords.append(' '.join([str(a[0]) for a in subtree.leaves()]))

		i = i + 1

	if (queryPhraseType == 3 and len(queries) > 1) and (lastWordTag.startswith('W') or secondLastWordTag.startswith('W')) :
		queries = queries[0:len(queries)-1]

	# Remove any useless words from the keywords 
	additionalSearchKeywords = [keyword.replace("'s", "") for keyword in additionalSearchKeywords]
	
	for query in queries:
		additionalSearchKeywords = [keyword.replace(query, "") for keyword in additionalSearchKeywords]	
	additionalSearchKeywords = [value for value in additionalSearchKeywords if value != ' ' and value != '']

	print("Wikia Queries : %s " % queries)
	print("Search Keywords : %s " % additionalSearchKeywords)

	if queries:

		# First query wikia to get possible matching articles
		articleIDs = queryWikiaSearch(queries)
	
		# If the search result did not return anything respond with no results respone 
		if articleIDs:
			answer = queryWikiaArticles(articleIDs, queries, additionalSearchKeywords) 
		##else: TODO: Perform spell check

	##else: TODO: Perform spell check

	return answer


## This method takes the POS-tagged user input, queries wikia and returns relevant information
## If the user is correct --- an appropriate response is selected from a pre-defined list
## If the user is incorrect --- an appropriate response is selected form a pre-defined list
## If the answer is hazy (ie. low probability that the article matched the input) then system responds accordingly
## If the article had something similar but not exact then the system responds with this refined result
##
def deviseRebuttle(taggedInput):
	return 'You are correct'


## TODO
##
def spellCheck(word):
	pass

## API INTERFACING ##
## Section which provides the methods necessary to interface with the wikia API
## Includes querying for article suggestions and optaining articles all in json format

## This method queries the wikia given the query and finds the most accurate article to perform further search 
## returns --- the most relevant articleID
##
def queryWikiaSearch(queries):

	articleIDs = []

	# Loop through all queries and find all matching articleIDs to search
	for query in queries:
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
			articleIDs.append([resultData['items'][0]['id'], query])

	return articleIDs

## This method uses wikia's API to fetch the article as a json given the articleID 
## returns --- the response as decided by the searchRefinement
##
def queryWikiaArticles(articleIDs, queries, searchRefinement):
	
	answer = ''
	answerScore = 0

	for articleID in articleIDs:
		# Format Article URL
		ARTICLE_QUERY_TEMPLATE['id'] = articleID[0]
		articleUrl = WIKIA_API_URL
		articleUrl += ARTICLES_URI
		articleUrl += urllib.urlencode(ARTICLE_QUERY_TEMPLATE)

		# Open URL and fetch json response text
		results = urllib2.urlopen(articleUrl)
		resultData = json.load(results)
		
		answerWithScore = refineWikiaArticleContent(articleID[1], resultData, queries, searchRefinement)
		print(answerWithScore[0])
		print(answerWithScore[1])
		if answerWithScore[1] > answerScore:
			answerScore = answerWithScore[1]
			answer = answerWithScore[0]

		if not answer: 
			sentences = sent_tokenize(resultData['sections'][0]['content'][0]['text'].replace('b.', 'born'))
			answer = ' '.join(sentences[0:2])

	
	return answer

## This method takes the json article and searches it for similar text based on the search refinement
## returns --- response most similar to the search refinement
##
def refineWikiaArticleContent(specificQuery, articleData, queries, searchRefinement):
	
	## top two sentences
	firstSentenceScore = 0
	secondSentenceScore = 0
	firstSentence = ''
	secondSentence = ''

	## loop through sections
	for section in articleData['sections']:
		## loop through content
		for content in section['content']:
			## fetch text and loop through sentences
			if not 'text' in content:
				continue
			for sentence in sent_tokenize(content['text'].replace('b.', 'born')):
				sentenceScore = 0

				## loop through refinements to see if they're in the sentence
				for refinement in searchRefinement:
					if refinement in sentence.rsplit(" "):
							sentenceScore = sentenceScore + (1 * sentence.rsplit(" ").count(refinement))
					if refinement in sentence:
						sentenceScore = sentenceScore + 0.5
					for query in queries:
						if ' '.join([query, refinement]) in sentence:
							sentenceScore = sentenceScore + 0.5
						if ' '.join([refinement, query]) in sentence:
							sentenceScore = sentenceScore + 0.5

				## loop through queries to see if they're in the sentence
				for query in queries:
					if query in sentence:
						sentenceScore = sentenceScore + 1 + (0.25 * sentence.rsplit(" ").count(query))
						if not query == specificQuery:
							sentenceScore = sentenceScore + 0.5

				## If score in top two re-adjust scores and sentences
				if sentenceScore > secondSentenceScore:
					if sentenceScore >= firstSentenceScore:
						secondSentence = firstSentence
						secondSentenceScore = firstSentenceScore
						firstSentence = sentence
						firstSentenceScore = sentenceScore
					else:
						secondSentence = sentence
						secondSentenceScore = sentenceScore

	if firstSentence:
		if len(firstSentence) > 150 or secondSentenceScore < firstSentenceScore:
			secondSentence = ''
			secondSentenceScore == 0
		return [' '.join([firstSentence, secondSentence]), firstSentenceScore + secondSentenceScore]
	else:
		return ['', 0]

##
##
if __name__ == '__main__' :
	HermioneUI()


