# COMP3011 Web Crawler and Search Engine

## Project Overview
This project is a Command-Line Interface (CLI) based web crawler and search engine built for the COMP3011 module. The tool is designed to systematically crawl `https://quotes.toscrape.com/`, parse the HTML content, extract text, and build an **Inverted Index** to facilitate search queries. 

### Key Architectural Features:
* **Optimized Search Logic:** Utilizes Python `Sets` and mathematical intersections to process multi-word "AND" queries efficiently.
* **Politeness Compliance:** Strictly adheres to a 6-second delay between HTTP requests to prevent server overload.
* **Queue Based Crawling** To ensure all available links on the site are parsed and visited. 
* **JSON index saving and loading** To reduce amount of `build` commands required.
---

## Dependencies & Installation

This project requires **Python 3.8+**. 
It relies on the following third-party libraries:
* `requests`: For handling HTTP requests.
* `beautifulsoup4`: For parsing HTML and extracting tag elements.

### Setup Instructions
1. **Clone or unzip the repository** to your local machine.
2. **Navigate to the root directory** of the project in your terminal.
3. **Install the dependencies** using the provided `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```
---

## Demonstration of Commands

Once you launch the interactive shell using `python src/main.py`, you can use the following commands at the `>` prompt:

### 1. `build`
Crawls the target website (`quotes.toscrape.com`), processes the text, and saves the resulting inverted index to `data/index.json`. 
```text
> build
```

### 2. `load`
Loads a pre-crawled index from the local `data/index.json` file to avoid needing to recrawl. 
```text
> load
```

### 3. `print <word>`
Displays inverted index statistics, including frequency and exact positions, for a specific word from all crawled pages. 
```text
> print einstein
```

### 4. `find <phrase>`
Searches the index for a given phrase and outputs Urls that have said phrase. Use AND logic for multi word phrases, only returning URLs containing every word.
```text
> find good friends
```

Use `exit` or `quit` to close the CLI loop.
---

## Testing

This project uses Python's `unittest` framework to ensure that the crawler and search logic work.

To run the full test suite, execute this command from the root directory:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

A successful run will show ```Ran 9 tests``