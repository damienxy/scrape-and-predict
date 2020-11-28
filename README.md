# Lyrics scraper and NLP classifier

Command-line tool where:

1. You provide as many artist/band names as you want
2. Their respective song lyrics are scraped to create a corpus (you can interrupt at any time and pick up the download at a later point)
3. The corpus is preprocessed (stop-word removal, tokenization, vectorization, tf-idf) and then used to train a Naive Bayes classifier
4. Once the model is trained, you can provide any word or song line from an artist
5. The tool predicts which artist the line is from

**Technologies:**<br>
Python | mypy | scikit-learn | pandas | BeautifulSoup
