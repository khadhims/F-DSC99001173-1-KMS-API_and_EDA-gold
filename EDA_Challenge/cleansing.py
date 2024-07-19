import pandas as pd
import re, unicodedata
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import nltk

def clean_text(text):
  processed_text = preprocess_text(text)
  # Buat variabel sementara untuk diproses
  cleaned_words = clean_text_with_sastrawi(processed_text)
  cleaned_text = ''.join(cleaned_words)

  processed_text = preprocess_text(cleaned_text)

  return processed_text

def preprocess_text(text):
    # Lowercase
    text = text.lower()
    # Hapus karakter non-ASCII
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    # Normalisasi Unicode ke ASCII
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    # Hapus karakter non-word
    text = re.sub(r'\W+', ' ', text)
    # Hapus kata yang hanya berisi angka atau karakter aneh
    text = re.sub(r'\b[\d\\]+\b', ' ', text)

    text = re.sub(r'[^a-zA-Z\s]', ' ', text)


    return text

def clean_text_with_sastrawi(text):
    text = preprocess_text(text)
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    stemmed_text = stemmer.stem(text)

    return stemmed_text

def clean_csv(file_path):
  df = pd.read_csv(file_path)
  df.drop_duplicates(subset=['Tweet'], inplace=True)
  df.dropna(subset=['Tweet'], inplace=True)

  if 'Tweet' not in df.columns:
    raise KeyError("Kolom 'Tweet' tidak ditemukan di file CSV.")
  
  df['Tweet'] = df['Tweet'].apply(lambda text: clean_text(text))
    
  return df