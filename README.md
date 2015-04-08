# HermioneBot
A natural language chatbot knowledgeable in Harry Potter trivia. 

## Wikia API
This application uses the wikia harry potter API to retrieve related search queries and articles from the website as linguistic input for the response generator.
url: https://www.harrypotter.wikia.com/api/v1

## Alpha Version - HW5 Q2 Milestone
### Updates
27-03-2015: No longer using pyjs for lack of debugging & support. Now using Tkinter to create a desktop application.

*NOTE*: This application requires wifi access in order to retrieve data from the wikia servers.

## Purpose
This project is being build for a linguistics course at McGill University LING 550 - Computational Linguistics.

## Dependencies
- python 2.7.6+ 
- nltk
- nltk.data 
- Treebank Part of Speech Tagger (Maximum entropy) 
- Punkt Tokenizer Models

### To Download: 
1. run python
2. import nltk
3. nltk.download()

This will open a gui application where you will be able to select the packages to install, they will download to the directory: /Users/your_user/nltk_data

## Submission #1 
The bot currently handles only simple question queries such as Who/What is/are <NP>.
The application remembers the username and uses it when replying in certain scenarios.
If the question does not either start with WH-word or end with a '?' then the application will assume the input as nonsensical.
Statements will be handled for the final submission.

### Happy Path: 
1. Enter name > Click "Reply"
2. Ask one of the following (or similar) questions (on loop):
	- "Who is Hermione Granger?" 
	- "Who is Harry?"
	- "What is Hogwarts?"
	- "What is herbology?"
	- "What are the houses at Hogwarts?" 
	- "What was the battle of Hogwarts?"
	- "What's a muggle?"

## Final Submission

### Functionality
	- Determine user intent based on syntax of POS-tagged input text: QUERY or UNKNOWN
		- if UNKNONWN Hermione returns sassy-quip as it's likely the user input nonsense
		- if QUERY:
			- if response contains 'you' or 'your' change to 'Hermione' given context
			- first perform spell check! (see below)
			- perform parse on POS-tagged input text to select a set of queries to enter into wikia and additional keywords to help refine solution
			- parse uses a technique known as NP-chunking based on a small grammar used to detect simple NP segments in the input
			- fetches relevant articleIDs for all query input and then searches through the sentences in the text
			- the sentences are scored based on appearance of relevant search terms (queries and keywords)
			- most probable 1 or 2 sentences are returned
			- if response contains 'Hermione' change to 'I' or 'my' given context
			- if no results based on query return 'no info available' type response
	- Spell Checker:
		- performs edit-distance of word against pre-defined list of Harry Potter vocabulary 
		- uses split, replace, transpose, delete, insert operations
		- returns word with high probability of having been mispelled by the user

### Happy Path:
1. Enter name -> Click "Reply"
2. Ask a question adhering to the following syntax (as provided by the Penn Treebank POS tagger):
	- Any phrase ending in a question mark '?':
	
	**Examples**: 
	- ''
	- ''
	
	- Any phrase starting with a WH-pronoun or adverb (What('s), Who('s), Where('s), When('s), Why('s), How('s)))
		
	**Examples**:
	- 'What is Harry Potter known for?'
	- 'Who's Cedric?'
	- 'Who was Cho Chang?'
	- 'When did Bellatrix escape from Azkaban?'
	- 'Who is the love of Hermione's life?'
	- 'Who is Parvati?'
	- 'What is the Yule Ball?'
	- 'Who is Moaning Myrtle?'
	- 'Where is Gringotts?'
	- 'Where is Hogwarts located?'
	- 'What is the Tale of Three Brothers?'
	- 'Who are Death Eaters?'
	- 'What are the Unforgivable Spells?'
	- 'Who transformed into Scabbers?'
	
	- Any phrase ending in a WH-pronoun:
	
	**Examples**:
	- ''
	
	- Any phrase starting with a singular present verb or modal (Is, Does, Are, Can, Could, Should, Would, Were, Was, etc...)

	**Examples**:
	- 'Is Hufflepuff the kindest house?'
	- '' 

3. Type in nonsensical phrase or a statement-like sentence to receive Hermione-like remark

	**Examples**:
	- '' 
	- ''

4. Type in a question or statement with an incorrectly spelled HP-specific spell/ or character name:
	
	**Examples**:	
	- 'What is quiddich?' -> 'It's Quidditch, not quiddich!
	- 'Who is Professor Quirel?' -> 'It's Quirrel, not Quirel!' 
	- 'What is Wingardium Leviosar?' -> 'It's Leviosa, not Leviosar!'
	- ''
	- ''

### Remarks
This is a largely probabilistic model which doesn't always obtain optimal results, for many queries, where there exists a wikia article containing a high occurence of relevant information/keywords based on that query, it will return the answer or related information.  However, this does not always happen.  The problem space is very large and there are many more optimizations and refinements that could be made to improve the system. Although, given the time and resource constraint I am satisfied with what I've been able to achieve and learn from this project thus far.
