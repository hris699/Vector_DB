# Qdrant Cloud Vector Database Project

## Structure
```
Vector_DB/
├── src/
│   ├── database/
│   │   └── qdrant_client.py    # Vector DB operations
│   ├── models/
│   │   └── document.py         # Document model
│   └── data_loader.py          # Data loading utilities
├── config/
│   └── settings.py             # Configuration
├── data/
│   └── sample_data.json        # Sample data
├── .env                        # Environment variables
├── requirements.txt            # Dependencies
└── main.py                     # Demo script
```

## Setup
1. Install: `pip install -r requirements.txt`
2. Update `.env` with your Qdrant Cloud credentials
3. Run: `python main.py`

## Operations
- **Insert**: `db.insert(documents)`
- **Search**: `db.search(query, limit)`
- **Get**: `db.get(doc_id)`
- **Update**: `db.update(doc_id, data)`
- **Delete**: `db.delete(doc_ids)`