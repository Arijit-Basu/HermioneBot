## Resources for querying API and parsing results
import re, collections, json, urllib, urllib2, random

## Resources for performing POS tagging & lamda expressions
from nltk import RegexpParser
from nltk.data import load
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize

## GUI Resources
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
	NP: {<DT|PRP\$>?<JJ|JJS>*<NN|NNS>+}
		{<NNP|NNPS><IN><DT>?<NNP|NNPS>}
		{<NNP|NNPS>+}
		{<PRP>}
		{<JJ>+}
		{<WP|WP\s$|WRB>}
	VP: {<VB|VBD|VBG|VBN|VBP|VBZ|MD><NP|IN>?}
	PP: {<IN><NN|NNS|NNP|NNPS|CD>}
"""
parser = RegexpParser(grammar)

## Pre-defined responses to statements and undecipherable user questions
GREETING = 'I\'m Hermione Granger and you are?'
WELCOME = 'Pleasure.'
RESPONSE_TO_NONSENSE = ['I\'m sorry but that is simply not a question!', 'Is that a real question. Well it\'s not very good now is it?', 'Honestly %s, that is not funny, you\'re lucky I don\'t report you to the headmaster' % userName, 'I hope you\'re pleased with yourself. We could have all been killed, or worse... expelled!']
SPELLING_ERROR = 'It\'s %s, not %s!'
MUST_ENTER_INPUT = 'It appears you haven\'t asked a question. How do you expect me to perform any magic without a question?'
NO_INFORMATION_AVAILABLE = 'Even \"Hogwarts: A History\" couldn\'t answer that question. Perhaps try a different question.'

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
		responseLabel.place(x=925, y=105, relwidth=.175, relheight=.425)	

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
			if response[0:3].lower() == 'he ' or response[0:4].lower() == 'she ' or response[0:5].lower() == 'they ':
				response = "Well, %s%s" % (response[0].lower(), response[1:len(response)])
		elif intent == Intent.NONSENSE :
			print("HERMIONE THINKS YOU ARE UNCLEAR.")
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

## This method takes as input the tagged user input and processes it to determine and appropriate response
## returns an answer to the user's question
##
def deviseAnswer(taggedInput):

	# Before querying the wiki -- perform spell check!
	for word in [word for word in taggedInput if len(word[0]) > 3 and (word[1].startswith('N') or word[1].startswith('J') or word[1].startswith('V'))]:
		correctSpelling = spellCheck(word[0])
		if not correctSpelling == word[0]:
			return SPELLING_ERROR % (correctSpelling, word[0])

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
	
	# Replace 'you' with 'Hermione' in queries and keywords
	addHermioneQuery = False
	
	for query in queries:
		if 'your' in query or 'you' in query:
			addHermioneQuery = True

	for keyword in additionalSearchKeywords:
		if 'your' in keyword or 'you' in keyword:
			addHermioneQuery = True

	queries = [query.replace('your', '').replace('you', '') for query in queries]
	additionalSearchKeywords = [keyword.replace('your', '').replace('you', '') for keyword in additionalSearchKeywords]

	if addHermioneQuery:
		queries.append('Hermione Granger')

	for query in queries:
		additionalSearchKeywords = [keyword.replace(query, "") for keyword in additionalSearchKeywords]	
	additionalSearchKeywords = [value for value in additionalSearchKeywords if value != ' ' and value != '']
	queries = [value for value in queries if value != '']

	print("Wikia Queries : %s " % queries)
	print("Search Keywords : %s " % additionalSearchKeywords)

	if queries:

		# First query wikia to get possible matching articles
		articleIDs = queryWikiaSearch(queries)
	
		# If the search result did not return anything respond with no results respone 
		if articleIDs:
			answer = queryWikiaArticles(articleIDs, queries, additionalSearchKeywords) 

	print("Hermione's Response: %s" % answer)
	return answer

## This method takes as input a word and verifies the spelling based on pre-defined Harry Potter vocabulary
## returns True if there is a spelling error
##
def spellCheck(word):
	correctSpelling = correct(word)
	if correctSpelling:
		return correctSpelling
	return 

## The following code was based off norvig.com/spell-correct.html
## written by Peter Norvig explaining how Google spell check performs fast and efficient spell checking
## hp-lexicon.txt --- Harry Potter vocabulary file with correct spellings of HP spells, made-up words and character names
##
def words(text): return re.findall('[a-zA-Z]+', text) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('hp-lexicon.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)


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
		try:
			results = urllib2.urlopen(searchUrl)
			resultData = json.load(results)
		except HTTPError: 
			continue

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

		if answerWithScore[1] > answerScore:
			answerScore = answerWithScore[1]
			answer = answerWithScore[0]

			# If response has to do with Hermione replace 3rd person pronouns with 1st person pronouns
			for query in queries:
				if 'Hermione' in query.rsplit(" "):
					answer.replace('she', 'I').replace('her', 'my')

			# Replace any keyword hinting at Hermione with the proper personal pronoun and if followed by 'is' replace with 'am'
			answer = answer.replace('Hermione\'s', 'my').replace('Hermione Granger is', 'I am').replace('Hermione is', 'I am').replace('Hermione Jean Granger', 'I').replace('Hermione Granger', 'I').replace('Hermione', 'I')

		if not answer: 
			try:
				sentences = sent_tokenize(resultData['sections'][0]['content'][0]['text'].replace('b.', 'born'))
				# Replace any keyword hinting at Hermione with the proper personal pronoun and if followed by 'is' replace with 'am'
				answer = ' '.join(sentences[0:2]).replace('Hermione\'s', 'my').replace('Hermione Granger is', 'I am').replace('Hermione is', 'I am').replace('Hermione Jean Granger', 'I').replace('Hermione Granger', 'I').replace('Hermione', 'I')

			except IndexError:
				continue
	
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
					
					if refinement in sentence:
							sentenceScore = sentenceScore + 0.5 + (sentence.count(refinement)/len(sentence.rsplit(" ")))

					for query in queries:
						
						if ' '.join([query, refinement]) in sentence:
							sentenceScore = sentenceScore + 0.25
						if ' '.join([refinement, query]) in sentence:
							sentenceScore = sentenceScore + 0.25

				## loop through queries to see if they're in the sentence
				for query in queries:
					
					if query in sentence:
						sentenceScore = sentenceScore + 1 + sentence.count(query)/len(sentence.rsplit(" "))
						if not query == specificQuery:
							sentenceScore = sentenceScore + 0.5
					
					for word in query.split(" "):
						if word in sentence:
							sentenceScore = sentenceScore + 1/len(queries)


				## If score in top two re-adjust scores and sentences
				if sentenceScore > secondSentenceScore:
					if sentenceScore > firstSentenceScore:
						secondSentence = firstSentence
						secondSentenceScore = firstSentenceScore
						firstSentence = sentence
						firstSentenceScore = sentenceScore
					else:
						secondSentence = sentence
						secondSentenceScore = sentenceScore

	if firstSentence:
		if len(firstSentence) + len(secondSentence) > 250 or secondSentenceScore < firstSentenceScore:
			secondSentence = ''
			secondSentenceScore == 0
		return [' '.join([firstSentence, secondSentence]), firstSentenceScore + secondSentenceScore]
	else:
		return ['', 0]


## Main method --- starting point of program, initializes Bot
##
if __name__ == '__main__' :
	HermioneUI()


