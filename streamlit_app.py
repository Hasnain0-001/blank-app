import streamlit as st
import requests
from bs4 import BeautifulSoup
import nltk
from nltk import ngrams
from collections import Counter
import string

# Download the NLTK punkt tokenizer if needed
nltk.download('punkt')

# Streamlit app title
st.title("N-Gram Analyzer for Top-Ranking URLs")

# Function to fetch webpage content
def get_webpage_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.get_text()
        else:
            st.error(f"Failed to fetch {url}. Status code: {response.status_code}")
            return ""
    except Exception as e:
        st.error(f"Error fetching {url}: {e}")
        return ""

# Function to clean and tokenize text
def clean_and_tokenize(text):
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    tokens = nltk.word_tokenize(text)
    return tokens

# Function to extract n-grams
def extract_ngrams(tokens, n):
    return ngrams(tokens, n)

# Function to count n-grams
def get_ngram_counts(tokens, n, top_n=10):
    n_grams = extract_ngrams(tokens, n)
    return Counter(n_grams).most_common(top_n)

# Input fields for URLs
st.write("Enter the top 3 URLs you want to analyze:")
url_1 = st.text_input("Enter URL 1")
url_2 = st.text_input("Enter URL 2")
url_3 = st.text_input("Enter URL 3")

# Input for the targeted query
query = st.text_input("Enter the targeted query:")

# Button to analyze n-grams
if st.button("Analyze N-Grams"):
    if url_1 and url_2 and url_3 and query:
        urls = [url_1, url_2, url_3]
        combined_tokens = []

        # Fetch and combine tokens from all 3 URLs
        for url in urls:
            content = get_webpage_content(url)
            tokens = clean_and_tokenize(content)
            combined_tokens.extend(tokens)

        # Display the n-grams for unigrams, bigrams, trigrams
        st.write(f"\nAnalyzing n-grams for the query: {query}")

        # Loop through unigrams, bigrams, trigrams
        for n in range(1, 4):
            st.write(f"\nTop {n}-grams:")
            ngram_counts = get_ngram_counts(combined_tokens, n)
            for ngram, count in ngram_counts:
                st.write(f"{' '.join(ngram)}: {count}")
    else:
        st.error("Please fill in all URLs and the query before analyzing.")

