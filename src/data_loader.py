from typing import List, Dict, Any
import json
import os
import random

class DataLoader:
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
                        reviews.append({
                            "text": text,
                            "sentiment": "positive",
                            "source": "imdb",
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
                            "source": "imdb",
                            "file": file
                        })
                except:
                    continue
        
        return reviews
    
    @staticmethod
    def load_sample_data() -> List[Dict[str, Any]]:
        return [
            {"text": "Machine learning algorithms learn patterns from data", "category": "AI"},
            {"text": "Vector databases store embeddings for similarity search", "category": "Database"},
            {"text": "Python is widely used in data science projects", "category": "Programming"}
        ]