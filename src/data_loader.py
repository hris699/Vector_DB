from typing import List, Dict, Any
import json
import os
import random

class DataLoader:
    @staticmethod
    def load_all_reviews(limit: int = 100) -> List[Dict[str, Any]]:
        """Load reviews from both archive folders"""
        reviews = []
        
        imdb_reviews = DataLoader.load_imdb_reviews(limit//2)
        reviews.extend(imdb_reviews)
        
        sentiment_reviews = DataLoader.load_sentiment_reviews(limit//2)
        reviews.extend(sentiment_reviews)
        
        return reviews
    
    @staticmethod
    def load_imdb_reviews(limit: int = 100) -> List[Dict[str, Any]]:
        """Load IMDB movie reviews from archive folder"""
        reviews = []
        base_path = "archive/aclImdb/train"
        
        # Load positive reviews
        pos_path = os.path.join(base_path, "pos")
        if os.path.exists(pos_path):
            files = os.listdir(pos_path)[:limit//2]
            for file in files:
                try:
                    with open(os.path.join(pos_path, file), 'r', encoding='utf-8') as f:
                        text = f.read().strip()
                        rating = int(file.split('_')[1].split('.')[0]) if '_' in file else 5
                        reviews.append({
                            "text": text,
                            "sentiment": "positive",
                            "rating": rating,
                            "word_count": len(text.split()),
                            "char_count": len(text),
                            "source": "imdb",
                            "category": "movie_review",
                            "language": "english",
                            "file": file
                        })
                except:
                    continue
        
        # Load negative reviews
        neg_path = os.path.join(base_path, "neg")
        if os.path.exists(neg_path):
            files = os.listdir(neg_path)[:limit//2]
            for file in files:
                try:
                    with open(os.path.join(neg_path, file), 'r', encoding='utf-8') as f:
                        text = f.read().strip()
                        rating = int(file.split('_')[1].split('.')[0]) if '_' in file else 5
                        reviews.append({
                            "text": text,
                            "sentiment": "negative",
                            "rating": rating,
                            "word_count": len(text.split()),
                            "char_count": len(text),
                            "source": "imdb",
                            "category": "movie_review",
                            "language": "english",
                            "file": file
                        })
                except:
                    continue
        
        return reviews
    
    @staticmethod
    def load_sentiment_reviews(limit: int = 100) -> List[Dict[str, Any]]:
        """Load sentiment reviews from archive (1) folder"""
        reviews = []
        base_path = "archive (1)/txt_sentoken"
        
        # Load positive reviews
        pos_path = os.path.join(base_path, "pos")
        if os.path.exists(pos_path):
            files = os.listdir(pos_path)[:limit//2]
            for file in files:
                try:
                    with open(os.path.join(pos_path, file), 'r', encoding='utf-8') as f:
                        text = f.read().strip()
                        reviews.append({
                            "text": text,
                            "sentiment": "positive",
                            "word_count": len(text.split()),
                            "char_count": len(text),
                            "source": "sentiment_corpus",
                            "category": "sentiment_review",
                            "language": "english",
                            "file": file
                        })
                except:
                    continue
        
        # Load negative reviews
        neg_path = os.path.join(base_path, "neg")
        if os.path.exists(neg_path):
            files = os.listdir(neg_path)[:limit//2]
            for file in files:
                try:
                    with open(os.path.join(neg_path, file), 'r', encoding='utf-8') as f:
                        text = f.read().strip()
                        reviews.append({
                            "text": text,
                            "sentiment": "negative",
                            "word_count": len(text.split()),
                            "char_count": len(text),
                            "source": "sentiment_corpus",
                            "category": "sentiment_review",
                            "language": "english",
                            "file": file
                        })
                except:
                    continue
        
        return reviews
    
    @staticmethod
    def load_single_text_file(filepath: str) -> Dict[str, Any]:
        """Load single text file with metadata"""
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        filename = os.path.basename(filepath)
        return {
            "text": text,
            "filename": filename,
            "word_count": len(text.split()),
            "char_count": len(text),
            "source": "text_file",
            "category": "document",
            "file_path": filepath
        }
    
    @staticmethod
    def load_sample_data() -> List[Dict[str, Any]]:
        return [
            {"text": "Machine learning algorithms learn patterns from data", "category": "AI"},
            {"text": "Vector databases store embeddings for similarity search", "category": "Database"},
            {"text": "Python is widely used in data science projects", "category": "Programming"}
        ]
    
    @staticmethod
    def load_csv_reviews(filepath: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Load TV show data from CSV file (archive 2)"""
        import pandas as pd
        try:
            df = pd.read_csv(filepath, encoding='utf-8')
            reviews = []
            for _, row in df.head(limit).iterrows():
                # Combine name and description for text content
                name = str(row.get('Name', '')).strip()
                description = str(row.get('Description', '')).strip()
                text_content = f"{name}: {description}"
                
                # Determine sentiment based on rating
                rating = float(row.get('Rating', 0))
                sentiment = "positive" if rating >= 8.0 else "negative" if rating < 6.0 else "neutral"
                
                reviews.append({
                    "text": text_content,
                    "sentiment": sentiment,
                    "rating": rating,
                    "word_count": len(text_content.split()),
                    "char_count": len(text_content),
                    "source": "csv_dataset",
                    "category": "csv_review",
                    "language": "english",
                    "show_name": name,
                    "year": str(row.get('Year', '')),
                    "type": str(row.get('Type', ''))
                })
            return reviews
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return []
    
    @staticmethod
    def load_from_json(filepath: str) -> List[Dict[str, Any]]:
        with open(filepath, 'r') as f:
            return json.load(f)