from src.database.qdrant_client import VectorDB
from src.data_loader import DataLoader

def main():
    
    db = VectorDB()
    print("Vector Database initialized successfully")
    print("Available operations: insert, search, get, update, delete, filter")

if __name__ == "__main__":
    main()