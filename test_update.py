from src.database.qdrant_client import VectorDB
from src.data_loader import DataLoader

def test_update():
    # Test update operations across the three collections
    collections = {
        "imdb_reviews": VectorDB("imdb_reviews"),
        "sentiment_reviews": VectorDB("sentiment_reviews"),
        "tv_reviews": VectorDB("tv_reviews")
    }
    
    all_doc_ids = {}
    

    for collection_name, doc_ids in all_doc_ids.items():
        print(f"\n=== UPDATING {collection_name.upper()} ===")
        
        doc_id = doc_ids[0]  # Update first document
        db = collections[collection_name]
        
        # Get original
        original = db.get(doc_id)
        print(f"Original text: {original['data']['text'][:50]}...")
        
        # Prepare update data based on collection type
        if collection_name == "imdb_reviews":
            updated_data = {
                "text": "Updated IMDB review: This movie has incredible acting and amazing storyline",
                "sentiment": "positive",
                "rating": 9,
                "word_count": 12,
                "char_count": 75,
                "source": "imdb",
                "category": "movie_review",
                "language": "english",
                "updated": True
            }
        elif collection_name == "sentiment_reviews":
            updated_data = {
                "text": "Updated sentiment review: Excellent film with outstanding performances",
                "sentiment": "positive",
                "word_count": 9,
                "char_count": 70,
                "source": "sentiment_corpus",
                "category": "sentiment_review",
                "language": "english",
                "updated": True
            }
        else:  # csv_reviews
            updated_data = {
                "text": "Updated CSV Show: Revolutionary series with groundbreaking storytelling",
                "sentiment": "positive",
                "rating": 9.8,
                "word_count": 9,
                "char_count": 70,
                "source": "csv_dataset",
                "category": "csv_review",
                "language": "english",
                "show_name": "Updated Masterpiece",
                "year": "2024",
                "type": "Updated Series",
                "updated": True
            }
        
        # Perform update
        success = db.update(doc_id, updated_data)
        print(f"Update successful: {success}")
        
        # Verify update
        updated = db.get(doc_id)
        print(f"Updated text: {updated['data']['text'][:50]}...")
        print(f"Updated field: {updated['data'].get('updated', False)}")
        
        # Search for updated content
        results = db.search("updated incredible", limit=1)
        if results:
            print(f"Found updated document with score: {results[0]['score']:.3f}")

if __name__ == "__main__":
    test_update()