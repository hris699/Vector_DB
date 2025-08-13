from src.database.qdrant_client import VectorDB
from src.data_loader import DataLoader

def test_delete():
    # Test delete operations across the three collections
    collections = {
        "imdb_reviews": VectorDB("imdb_reviews"),
        "sentiment_reviews": VectorDB("sentiment_reviews"),
        "tv_reviews": VectorDB("tv_reviews")
    }
    
    all_doc_ids = {}
    
    # # Insert data into all collections
    # imdb_data = DataLoader.load_imdb_reviews(limit=4)
    # if imdb_data:
    #     all_doc_ids["imdb_reviews"] = collections["imdb_reviews"].insert(imdb_data)
    
    # sentiment_data = DataLoader.load_sentiment_reviews(limit=4)
    # if sentiment_data:
    #     all_doc_ids["sentiment_reviews"] = collections["sentiment_reviews"].insert(sentiment_data)
    
    # csv_data = DataLoader.load_csv_reviews("archive (2)/IMDB.csv", limit=4)
    # if csv_data:
    #     all_doc_ids["csv_reviews"] = collections["csv_reviews"].insert(csv_data)
    
    # Test deletion in each collection
    for collection_name, doc_ids in all_doc_ids.items():
        print(f"\n=== DELETING FROM {collection_name.upper()} ===")
        
        db = collections[collection_name]
        
        # Show documents before deletion
        print("Before deletion:")
        for i, doc_id in enumerate(doc_ids):
            doc = db.get(doc_id)
            if doc:
                if collection_name == "imdb_reviews":
                    sentiment = doc['data']['sentiment']
                    rating = doc['data'].get('rating', 'N/A')
                    text = doc['data']['text'][:30]
                    print(f"  {i+1}. {text}... ({sentiment}, Rating: {rating})")
                elif collection_name == "sentiment_reviews":
                    sentiment = doc['data']['sentiment']
                    text = doc['data']['text'][:30]
                    print(f"  {i+1}. {text}... ({sentiment})")
                else:  # csv_reviews
                    show_name = doc['data'].get('show_name', 'Unknown')
                    rating = doc['data'].get('rating', 'N/A')
                    print(f"  {i+1}. {show_name} (Rating: {rating})")
        
        # Delete last half of documents
        delete_count = len(doc_ids) // 2
        delete_ids = doc_ids[-delete_count:] if delete_count > 0 else [doc_ids[-1]]
        
        success = db.delete(delete_ids)
        print(f"\nDeleted {len(delete_ids)} documents: {success}")
        
        # Verify deletion
        print("After deletion:")
        remaining_count = 0
        for i, doc_id in enumerate(doc_ids):
            doc = db.get(doc_id)
            if doc:
                if collection_name == "imdb_reviews":
                    sentiment = doc['data']['sentiment']
                    print(f"  Still exists: {sentiment} review")
                elif collection_name == "sentiment_reviews":
                    sentiment = doc['data']['sentiment']
                    print(f"  Still exists: {sentiment} sentiment")
                else:
                    show_name = doc['data'].get('show_name', 'Unknown')
                    print(f"  Still exists: {show_name}")
                remaining_count += 1
            else:
                print(f"  Deleted: {doc_id[:8]}...")
        
        # Search verification
        results = db.search("movie film", limit=10)
        print(f"Search results: {len(results)} found (remaining: {remaining_count})")

if __name__ == "__main__":
    test_delete()