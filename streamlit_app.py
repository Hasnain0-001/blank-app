import streamlit as st
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter

# Ensure the 'punkt' tokenizer is downloaded
nltk.download('punkt')

# Function to fetch page content
def fetch_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Function to clean and tokenize text
def clean_and_tokenize(text):
    tokens = nltk.word_tokenize(text)
    tokens = [token.lower() for token in tokens if token.isalnum()]  # Remove punctuation and lowercase
    return tokens

# Function to extract n-grams from tokens
def extract_ngrams(tokens, n):
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [' '.join(ngram) for ngram in ngrams]

# Streamlit app
st.title('N-gram Extractor from Top Ranking URLs')

# Input: URLs
url1 = st.text_input("Enter URL 1:")
url2 = st.text_input("Enter URL 2:")
url3 = st.text_input("Enter URL 3:")

# Input: Query
query = st.text_input("Enter Target Query:")

# Select n-gram size
n = st.slider("Select n-gram size:", 1, 5, 2)

# Button to run the extraction
if st.button('Extract N-grams'):
    urls = [url1, url2, url3]
    all_tokens = []

    for url in urls:
        if url:
            content = fetch_page_content(url)
            if content:
                soup = BeautifulSoup(content, 'html.parser')
                text = soup.get_text()
                tokens = clean_and_tokenize(text)
                all_tokens.extend(tokens)

    # Extract n-grams and display the most common ones
    if all_tokens:
        ngrams = extract_ngrams(all_tokens, n)
        ngram_freq = Counter(ngrams)
        st.write(f"Top {n}-grams for the query '{query}':")
        st.write(ngram_freq.most_common(10))
    else:
        st.write("Could not fetch content from the URLs.")


