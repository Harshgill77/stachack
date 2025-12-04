import sys
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_chatbot_loading():
    print("Testing Chatbot Data Loading...")
    try:
        # Mimic the path logic in main.py
        csv_path = os.path.join(os.path.dirname(__file__), 'data', 'chatbot_data.csv')
        print(f"Looking for CSV at: {csv_path}")
        
        if not os.path.exists(csv_path):
            print("❌ File not found!")
            return

        df = pd.read_csv(csv_path)
        print(f"✅ CSV loaded. Rows: {len(df)}")
        
        questions = df['question'].tolist()
        
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(questions)
        print("✅ Vectorization successful.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_chatbot_loading()
