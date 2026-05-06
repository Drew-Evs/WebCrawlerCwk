import sys
from crawler import build_crawler
from indexer import InvertedIndex
from search import Searcher

def main():
    #initial start + create core components
    print("Search Engine Tool")
    print("'help' for commands and 'exit' to quit")
    indexer = InvertedIndex()
    searcher = Searcher(indexer)

    #alter this to take in other urls but start with target website
    target_url = "https://quotes.toscrape.com/"

    #cli loop
    while True:
        try:
            #command prompt
            user_input = input("\n> ").strip()

            #test for empty input before splitting into command and args
            if not user_input:
                continue
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            #test for quit commands
            if command in ["exit", "quit"]:
                print("Exiting Search Engine")
                break

            #list available commands
            elif command == "help":
                print("Available commands:")
                print("  build         - crawl site and build/save index")
                print("  load          - load pre existing index")
                print("  print <word>  - inverted index stats for <word>")
                print("  find <phrase> - find all pages with words in <phrase>")
                print("  exit          - close")

            elif command == "build":
                print(f'Crawling {target_url}')
                indexer = build_crawler(target_url)
                searcher.indexer = indexer
                print("Crawler built")

            #already handles missing files
            elif command == "load":
                indexer.load(filepath='data/index.json')
                searcher.indexer = indexer

            #need to test for missing args
            elif command == "print":
                if not args:
                    print("Missing word to print e.g. print nonsense")
                elif indexer.index == {}:
                    print("Indexer missing - run 'build' or 'load' first")
                else:
                    searcher.print_word(args)

            #need to test for phrase
            elif command == "find":
                if not args:
                    print("Missing phrase to search e.g. find good friends")
                elif indexer.index == {}:
                    print("Indexer missing - run 'build' or 'load' first")
                else:
                    searcher.find_phrase(args)

            else:
                print(f"Unknown command: '{command}'. Type 'help' command list")

        except KeyboardInterrupt:
            print("\nExiting Search Engine")
            break
        
        #handle exceptions to keep shell open
        except Exception as e:
            print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()