"""
Script to regenerate tokenizer.pkl with TensorFlow 2.15.0 compatibility
Run this script to fix pickle compatibility issues
"""
import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer

print(f"TensorFlow version: {tf.__version__}")

# Load the old tokenizer
print("Loading old tokenizer...")
with open('../backend/tokenizer.pkl', 'rb') as f:
    try:
        old_tokenizer = pickle.load(f)
        print("Old tokenizer loaded successfully")
    except Exception as e:
        print(f"Error loading old tokenizer: {e}")
        exit(1)

# Create a new tokenizer with the same configuration
print("Creating new tokenizer with same configuration...")
new_tokenizer = Tokenizer(
    num_words=old_tokenizer.num_words if hasattr(old_tokenizer, 'num_words') else 10000,
    oov_token="<unk>"
)

# Copy the word_index and other attributes
new_tokenizer.word_index = old_tokenizer.word_index
new_tokenizer.word_counts = old_tokenizer.word_counts
new_tokenizer.word_docs = old_tokenizer.word_docs
new_tokenizer.index_word = old_tokenizer.index_word
new_tokenizer.index_docs = old_tokenizer.index_docs
new_tokenizer.document_count = old_tokenizer.document_count

print(f"Tokenizer configuration:")
print(f"  - Vocabulary size: {len(new_tokenizer.word_index)}")
print(f"  - num_words: {new_tokenizer.num_words}")
print(f"  - Document count: {new_tokenizer.document_count}")

# Save the new tokenizer
print("Saving new tokenizer...")
with open('../backend/tokenizer.pkl', 'wb') as f:
    pickle.dump(new_tokenizer, f)

print("✓ Tokenizer regenerated successfully!")
print("You can now deploy to Render.")
