from src.database.qdrant_client import VectorDB
from src.data_loader import DataLoader

def test_insert():
    # Create the three specified collections
    imdb_db = VectorDB("imdb_reviews")
    sentiment_db = VectorDB("sentiment_reviews") 
    tv_db = VectorDB("tv_reviews")
    
    total_inserted = 0
    
    # Insert IMDB data
    imdb_data = DataLoader.load_imdb_reviews(limit=70)
    if imdb_data:
        imdb_ids = imdb_db.insert(imdb_data)
        print(f"[OK] IMDB Reviews: {len(imdb_ids)} documents")
        total_inserted += len(imdb_ids)
    else:
        print("[ERROR] No IMDB data loaded")
    
    # Insert sentiment data
    sentiment_data = DataLoader.load_sentiment_reviews(limit=50)
    if sentiment_data:
        sentiment_ids = sentiment_db.insert(sentiment_data)
        print(f"[OK] Sentiment Reviews: {len(sentiment_ids)} documents")
        total_inserted += len(sentiment_ids)
    else:
        print("[ERROR] No sentiment data loaded")
    
    # Insert CSV data
    csv_data = DataLoader.load_csv_reviews("archive (2)/IMDB.csv", limit=50)
    if csv_data:
        csv_ids = tv_db.insert(csv_data)
        print(f"[OK] TV Reviews: {len(csv_ids)} documents")
        total_inserted += len(csv_ids)
    else:
        print("[ERROR] No TV data loaded")
    
    print(f"\nTotal inserted across all collections: {total_inserted}")

if __name__ == "__main__":
    test_insert()