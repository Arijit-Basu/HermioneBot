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
python 
nltk
nltk.data - Treebank Part of Speech Tagger (Maximum entropy) 
	  - Punkt Tokenizer Models

to download: run python
>> import nltk
>> nltk.download()

- this will open a gui application where you will be able to select the packages to install, they will download to the directory: /Users/<your_user>/nltk_data 
