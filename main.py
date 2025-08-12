from src.database.qdrant_client import VectorDB
from src.data_loader import DataLoader

def main():
    # Initialize
    db = VectorDB()
    
    # Load IMDB movie reviews
    print("Loading IMDB movie reviews...")
    reviews = DataLoader.load_imdb_reviews(limit=20)
    print(f"Loaded {len(reviews)} reviews")
    
    # Insert reviews
    ids = db.insert(reviews)
    print(f"Inserted: {len(ids)} movie reviews")
    
    # Search for movie-related content
    queries = ["great movie acting", "terrible film boring", "amazing story plot"]
    
    for query in queries:
        print(f"\nSearching: '{query}'")
        results = db.search(query, limit=3)
        for r in results:
            sentiment = r['data']['sentiment']
            text_preview = r['data']['text'][:100].replace('\n', ' ')
            print(f"  {r['score']:.3f} ({sentiment}): {text_preview}...")
    
    # Get by ID
    doc = db.get(ids[0])
    print(f"\nRetrieved review: {doc['data']['sentiment']} - {doc['data']['text'][:50]}...")
    
    # Update a review
    updated_review = {
        "text": "This movie was absolutely fantastic with great acting!",
        "sentiment": "positive",
        "source": "imdb_updated"
    }
    db.update(ids[0], updated_review)
    print("Review updated")
    
    # Delete last review
    db.delete([ids[-1]])
    print("Review deleted")

if __name__ == "__main__":
    main()