from src.database.qdrant_client import VectorDB
from src.data_loader import DataLoader

def search_all_collections(query, limit=3):
    """Search across all three collections and return combined results"""
    collections = {
        "imdb_reviews": VectorDB("imdb_reviews"),
        "sentiment_reviews": VectorDB("sentiment_reviews"),
        "csv_reviews": VectorDB("csv_reviews")
    }
    
    all_results = []
    
    for collection_name, db in collections.items():
        try:
            results = db.search(query, limit=limit)
            for result in results:
                result['collection'] = collection_name
                all_results.append(result)
        except Exception as e:
            print(f"Error searching {collection_name}: {e}")
    
    # Sort by score descending
    all_results.sort(key=lambda x: x['score'], reverse=True)
    return all_results[:limit]

def test_search():
    # Setup data in all collections
    imdb_db = VectorDB("imdb_reviews")
    sentiment_db = VectorDB("sentiment_reviews")
    csv_db = VectorDB("csv_reviews")
    
    # Insert data
    imdb_data = DataLoader.load_imdb_reviews(limit=10)
    if imdb_data:
        imdb_db.insert(imdb_data)
    
    sentiment_data = DataLoader.load_sentiment_reviews(limit=10)
    if sentiment_data:
        sentiment_db.insert(sentiment_data)
    
    csv_data = DataLoader.load_csv_reviews("archive (2)/IMDB.csv", limit=10)
    if csv_data:
        csv_db.insert(csv_data)
    
    queries = ["great movie", "terrible film", "avatar"]
    
    for query in queries:
        print(f"\n=== SEARCHING ALL COLLECTIONS: '{query}' ===")
        results = search_all_collections(query, limit=5)
        
        for r in results:
            collection = r['collection']
            score = r['score']
            
            if collection == "imdb_reviews":
                sentiment = r['data']['sentiment']
                rating = r['data'].get('rating', 'N/A')
                text = r['data']['text'][:50]
                print(f"  {score:.3f} [IMDB]: {text}... ({sentiment}, Rating: {rating})")
            elif collection == "sentiment_reviews":
                sentiment = r['data']['sentiment']
                text = r['data']['text'][:50]
                print(f"  {score:.3f} [SENTIMENT]: {text}... ({sentiment})")
            else:  # csv_reviews
                show_name = r['data'].get('show_name', 'Unknown')
                rating = r['data'].get('rating', 'N/A')
                print(f"  {score:.3f} [CSV]: {show_name} (Rating: {rating})")

if __name__ == "__main__":
    test_search()