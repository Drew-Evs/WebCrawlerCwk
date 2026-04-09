import json 
import re
import os

'''
@class the inverted index containing all of the words in the site
    uses a nested dictionary containing the number of entreis and pages
@func __init__: creates the empty dictionary
    tokenize: converts all text to lowercase and extracts words
    add_document: processes document and adds word statistics to index
    save: save the index as a JSON file in data file
    load: loads the index from the JSON file 
'''
class InvertedIndex:
    '''initiate the empty dictionary'''
    def __init__(self):
        self.index = {}

    '''converts to lowercase and extracts words using regex'''
    def tokenize(self, text):
        text = text.lower()

        #\b for word boundary \w+ = 1+ word characters
        words = re.findall(r'\b\w+\b', text)
        return words
    
    '''processes the text and adds to stats in index'''
    def add_document(self, url, text):
        #get the list of words
        words = self.tokenize(text)

        #iterate each word and position in list
        for position, word in enumerate(words):
            #if new add to index
            if word not in self.index:
                self.index[word] = {}

            #if not new but new to url
            if url not in self.index[word]:
                self.index[word][url] = {"frequency": 0, "positions": []}

            #then update statistics
            self.index[word][url]["frequency"] += 1
            self.index[word][url]["positions"].append(position)

    '''saves to the JSON file'''
    def save(self, filepath="data/index.json"):
        #make file path if it doesnt exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        #then use json dumps to save
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=4)
        print(f"Index saved to {filepath}")

    '''and load from the JSON file'''
    def save(self, filepath="data/index.json"):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.index = json.load(f)
            print(f"Index loaded from {filepath}")
        except FileNotFoundError:
            print(f"Error: Didn't find index file at {filepath} - run crawler first")
            