from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import uuid
from config.settings import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME

class VectorDB:
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self._setup_collection()
    
    def _setup_collection(self):
        try:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
        except:
            pass  
    
    def insert(self, documents: List[Dict[str, Any]]) -> List[str]:
        points = []
        ids = []
        for doc in documents:
            doc_id = str(uuid.uuid4())
            vector = self.encoder.encode(doc['text']).tolist()
            points.append(PointStruct(id=doc_id, vector=vector, payload=doc))
            ids.append(doc_id)
        
        self.client.upsert(collection_name=COLLECTION_NAME, points=points)
        return ids
    
    def search(self, query: str, limit: int = 5) -> List[Dict]:
        vector = self.encoder.encode(query).tolist()
        results = self.client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=limit
        )
        return [{"id": r.id, "score": r.score, "data": r.payload} for r in results]
    
    def get(self, doc_id: str) -> Dict:
        result = self.client.retrieve(collection_name=COLLECTION_NAME, ids=[doc_id])
        return {"id": result[0].id, "data": result[0].payload} if result else None
    
    def update(self, doc_id: str, data: Dict[str, Any]) -> bool:
        vector = self.encoder.encode(data['text']).tolist()
        point = PointStruct(id=doc_id, vector=vector, payload=data)
        self.client.upsert(collection_name=COLLECTION_NAME, points=[point])
        return True
    
    def delete(self, doc_ids: List[str]) -> bool:
        self.client.delete(collection_name=COLLECTION_NAME, points_selector=doc_ids)
        return True