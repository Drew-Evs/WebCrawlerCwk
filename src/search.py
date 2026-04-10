import json

'''
@class use the inverted index to search and return positions
    of the given word or show the index
@func __init__: takes in an index
    print_word: takes in a word and outputs the inverted index for the word
    find_phrase: takes in word or phrase and returns list of all pages with the words in it
'''   
class Searcher:
    #takes in the indexer
    def __init__(self, indexer):
        self.indexer = indexer

    #print command implenetation - prints statistics
    def print_word(self, word):
        #use tokeniser logic to clean word
        clean_words = self.indexer.tokenize(word)
        if not clean_words:
            print(f"{word} is invalid. Try again")
            return
        
        #get the first word (in case using word like it's)
        target_word = clean_words[0]

        #check for word in index and print the dictionary to CLI
        if target_word in self.indexer.index:
            print(f"\n--- Index Data Found for '{target_word}' ---")
            print(json.dumps(self.indexer.index[target_word], indent=4))
        else:
            print(f"\nWord '{target_word}' not found in index")

    #find implementation - returning all URLs with all words in query phrase
    def find_phrase(self, phrase):
        #tokenise the words and check exists
        query_words = self.indexer.tokenize(phrase)
        if not query_words:
            print(f"{phrase} is invalid. Try again")
            return []

        #test first word if its not valid then failed query
        first_word = query_words[0]
        if first_word not in self.indexer.index:
            print(f"\nNo pages found with search phrase")
            return []

        #get a set of urls to find overlap rapidly
        matching_urls = set(self.indexer.index[first_word].keys())

        #loop through rest of words
        for word in query_words[1:]:
            #if each word not in set then fail
            if word not in self.indexer.index:
                print(f"\nNo pages found with search phrase")
                return []
            
            #get URLs for each sord and find intersection between sets
            word_urls = set(self.indexer.index[word].keys())
            matching_urls = matching_urls.intersection(word_urls)

        #output the results if there are any
        if matching_urls:
            print(f"\nFound {len(matching_urls)} page(s) with the search phrase:")
            for url in sorted(matching_urls):
                print(f" - {url}")
            return list(matching_urls)
        else:
            print(f"\nNo pages found with search phrase")
            return []