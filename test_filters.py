from src.database.qdrant_client import VectorDB
from src.data_loader import DataLoader

def filter_all_collections(query, filters, limit=3):
    """Filter across all three collections and return combined results"""
    collections = {
        "imdb_reviews": VectorDB("imdb_reviews"),
        "sentiment_reviews": VectorDB("sentiment_reviews"), 
        "tv_reviews": VectorDB("tv_reviews")
    }
    
    all_results = []
    
    for collection_name, db in collections.items():
        try:
            results = db.search(query, limit=limit, filters=filters)
            for result in results:
                result['collection'] = collection_name
                all_results.append(result)
        except Exception as e:
            print(f"No results in {collection_name} with filters {filters}")
    
    # Sort by score descending
    all_results.sort(key=lambda x: x['score'], reverse=True)
    return all_results[:limit]

def test_filters():
    # # Setup data in all collections
    # imdb_db = VectorDB("imdb_reviews")
    # sentiment_db = VectorDB("sentiment_reviews")
    # tv_db = VectorDB("tv_reviews")
    
    # # Insert data
    # imdb_data = DataLoader.load_imdb_reviews(limit=15)
    # if imdb_data:
    #     imdb_db.insert(imdb_data)
    
    # sentiment_data = DataLoader.load_sentiment_reviews(limit=15)
    # if sentiment_data:
    #     sentiment_db.insert(sentiment_data)
    
    # csv_data = DataLoader.load_csv_reviews("archive (2)/IMDB.csv", limit=15)
    # if csv_data:
    #     tv_db.insert(csv_data)
    
    print("=== FILTER TESTS ACROSS ALL COLLECTIONS ===")
    
    # Filter by sentiment
    print("\n1. Positive sentiment across all collections:")
    results = filter_all_collections("great amazing", {"sentiment": "positive"}, limit=5)
    for r in results:
        collection = r['collection']
        if collection == "imdb_reviews":
            rating = r['data'].get('rating', 'N/A')
            text = r['data']['text'][:40]
            print(f"  {r['score']:.3f} [IMDB]: {text}... (Rating: {rating})")
        elif collection == "sentiment_reviews":
            text = r['data']['text'][:40]
            print(f"  {r['score']:.3f} [SENTIMENT]: {text}...")
        else:  # csv_reviews
            show_name = r['data'].get('show_name', 'Unknown')
            rating = r['data'].get('rating', 'N/A')
            print(f"  {r['score']:.3f} [CSV]: {show_name} (Rating: {rating})")
    
    # Filter by source
    print("\n2. IMDB source:")
    results = filter_all_collections("movie film", {"source": "imdb"}, limit=3)
    for r in results:
        sentiment = r['data']['sentiment']
        rating = r['data'].get('rating', 'N/A')
        text = r['data']['text'][:40]
        print(f"  {r['score']:.3f} [IMDB]: {text}... ({sentiment}, Rating: {rating})")
    
    # Filter by category
    print("\n3. Movie reviews:")
    results = filter_all_collections("story plot", {"category": "movie_review"}, limit=3)
    for r in results:
        sentiment = r['data']['sentiment']
        text = r['data']['text'][:40]
        print(f"  {r['score']:.3f} [IMDB]: {text}... ({sentiment})")

if __name__ == "__main__":
    test_filters()