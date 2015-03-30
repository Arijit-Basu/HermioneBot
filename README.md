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

to download: 
1. run python
2. import nltk
3. nltk.download()

This will open a gui application where you will be able to select the packages to install, they will download to the directory: /Users/<your_user>/nltk_data

## Submission #1 
The bot currently handles only simple question queries such as Who/What is/are <NP>.
The application remembers the username and uses it when replying in certain scenarios.
If the question does not either start with WH-word or end with a ? then the application will assume the input as nonsensical.
Statements will be handled for the final submission.

### Happy Path: 
1. Enter name > Click "Reply"
2. Ask one of the following questions (on loop):
- "Who is Hermione Granger?" 
- "Who is Harry?"
- "What is Hogwarts?"
- "What is herbology?"
- "What are the houses at Hogwarts?" 
- "What was the battle of Hogwarts?"
- "What's a muggle?"

