from src.database.qdrant_client import VectorDB
from src.data_loader import DataLoader

def test_get():
    # Test get operations across the three collections
    collections = {
        "imdb_reviews": VectorDB("imdb_reviews"),
        "sentiment_reviews": VectorDB("sentiment_reviews"),
        "csv_reviews": VectorDB("csv_reviews")
    }
    
    all_doc_ids = {}
    
    # Insert data into all collections
    imdb_data = DataLoader.load_imdb_reviews(limit=2)
    if imdb_data:
        all_doc_ids["imdb_reviews"] = collections["imdb_reviews"].insert(imdb_data)
    
    sentiment_data = DataLoader.load_sentiment_reviews(limit=2)
    if sentiment_data:
        all_doc_ids["sentiment_reviews"] = collections["sentiment_reviews"].insert(sentiment_data)
    
    csv_data = DataLoader.load_csv_reviews("archive (2)/IMDB.csv", limit=2)
    if csv_data:
        all_doc_ids["csv_reviews"] = collections["csv_reviews"].insert(csv_data)
    
    # Test get by ID for each collection
    for collection_name, doc_ids in all_doc_ids.items():
        print(f"\n=== {collection_name.upper()} COLLECTION ===")
        
        for i, doc_id in enumerate(doc_ids):
            print(f"\n--- Document {i+1} ---")
            doc = collections[collection_name].get(doc_id)
            
            if doc:
                print(f"ID: {doc['id']}")
                
                if collection_name == "imdb_reviews":
                    print(f"Sentiment: {doc['data']['sentiment']}")
                    print(f"Rating: {doc['data'].get('rating', 'N/A')}")
                    print(f"Text: {doc['data']['text'][:50]}...")
                elif collection_name == "sentiment_reviews":
                    print(f"Sentiment: {doc['data']['sentiment']}")
                    print(f"Text: {doc['data']['text'][:50]}...")
                else:  # csv_reviews
                    print(f"Show: {doc['data'].get('show_name', 'N/A')}")
                    print(f"Rating: {doc['data'].get('rating', 'N/A')}")
                    print(f"Year: {doc['data'].get('year', 'N/A')}")
                
                print(f"Source: {doc['data'].get('source', 'N/A')}")
            else:
                print(f"Document {doc_id} not found")
    
    # Test get with non-existent ID across all collections
    print(f"\n=== NON-EXISTENT ID TEST ===")
    fake_id = "non-existent-id"
    for collection_name, db in collections.items():
        result = db.get(fake_id)
        print(f"{collection_name}: {result}")

if __name__ == "__main__":
    test_get()