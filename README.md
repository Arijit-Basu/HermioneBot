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

	**note:** you can follow Hermione's computation as many of the system inputs and intermediate states are logged in the terminal

### Happy Path:
1. Enter name -> Click "Reply"
2. Ask a question adhering to the following syntax (as provided by the Penn Treebank POS tagger):
	**I.** Any phrase ending in a question mark '?':
	
	**Examples**: 
	- 'In what year did Harry win the Triwizard Tournament?'
	- 'Quidditch is a sport?'
	
	**II.** Any phrase starting with a WH-pronoun or adverb (What('s), Who('s), Where('s), When('s), Why('s), How('s)))
		
	**Examples**:
	- 'Who's Harry Potter?'
	- 'What's Harry Potter known as?'
	- 'What's a house elf?'
	- 'Who's Cedric?'
	- 'Who was Cho Chang?'
	- 'Who's pet was Fang?'
	- 'How many horcruxes has Voldemort created?'
	- 'Who founded the Order of the Phoenix?'
	- 'When did Bellatrix escape from Azkaban?'
	- 'What was Rita Skeeter known to carry in her handbag?'
	- 'What was it that happened to Harry and Cedric Diggory at the end of the Triwizard Tournament?'
	- 'Who is Parvati?'
	- 'What is the Yule Ball?'
	- 'Who is Moaning Myrtle?'
	- 'Where is Gringotts located?'
	- 'What are the four houses of Hogwarts?'
	- 'Where is Hogwarts located?'
	- 'What is the Tale of Three Brothers?'
	- 'Who are Death Eaters?'
	- 'Who transformed into Scabbers?'
	- 'What did Harry do after the war?'
	- 'What is Grawp?'
	- 'What does creating a horcrux do?'
	- 'What's Divination?'
	
	**III.** Any phrase ending in a WH-pronoun:
	
	**Examples**:
	- 'To be a seeker in Quidditch means what?'
	- 'The half blood prince is who?'
	- 'The study of magical creatures is called what?'
	
	**IV.** Any phrase starting with a singular present verb or modal (Is, Does, Are, Can, Could, Should, Would, Were, Was, etc...)

	**Examples**:
	- 'Was Mr. Ollivander a wand maker?'
	- 'Is Gryffindor the bravest house?'
	- 'Are you friends with Harry Potter?' 
	- 'Does every spell require a wand?'
	- 'Can you tell me about the Marauders Map?'

	**V.** Questions directed at Hermione in 2nd person

	**Examples**:
	- 'Who are you?'
	- 'Who was the love of your life?'
	- 'When did you, Harry and Ron become best friends?'

3. Type in nonsensical phrase or a statement-like sentence to receive Hermione-like remark

	**Example**: (enter multiple times for different retorts)
	- 'I like Harry Potter.' 

4. Type in a question or statement with an incorrectly spelled HP-specific spell or character name:
	
	**Examples**:	
	- 'What is quiddich?' -> 'It's Quidditch, not quiddich!
	- 'Who is Professor Quirel?' -> 'It's Quirrel, not Quirel!' 
	- 'What is Wingardium Leviosar?' -> 'It's Leviosa, not Leviosar!'
	- 'Who is Minerva McGonogall?' -? 'It's McGonagall not McGonogall!'
	- 'Who is Luny Lovegood?' -> 'It's Luna not Luny!'

### Remarks
This is a largely probabilistic model which doesn't always obtain optimal results, for many queries, where there exists a wikia article containing a high occurence of relevant information/keywords based on that query, it will return the answer or related information.  However, this does not always happen.  The problem space is very large and there are many more optimizations and refinements that could be made to improve the system. Although, given the time and resource constraint I am satisfied with what I've been able to achieve and learn from this project thus far.
