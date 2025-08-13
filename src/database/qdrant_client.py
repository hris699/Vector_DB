from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue, PayloadSchemaType
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
import uuid
from config.settings import QDRANT_URL, QDRANT_API_KEY

class VectorDB:
    def __init__(self, collection_name: str = "documents"):
        self.client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection_name = collection_name
        self._setup_collection()
    
    def _setup_collection(self):
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
        except:
            pass
        
        # Create indexes
        indexes = [
            ("sentiment", PayloadSchemaType.KEYWORD),
            ("rating", PayloadSchemaType.INTEGER),
            ("category", PayloadSchemaType.KEYWORD),
            ("source", PayloadSchemaType.KEYWORD)
        ]
        
        for field_name, schema_type in indexes:
            try:
                self.client.create_payload_index(
                    collection_name=self.collection_name,
                    field_name=field_name,
                    field_schema=schema_type
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
        
        self.client.upsert(collection_name=self.collection_name, points=points)
        return ids
    
    def search(self, query: str, limit: int = 5, filters: Optional[Dict[str, Any]] = None) -> List[Dict]:
        vector = self.encoder.encode(query).tolist()
        
        query_filter = None
        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(FieldCondition(key=key, match=MatchValue(value=value)))
            query_filter = Filter(must=conditions)
        
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            query_filter=query_filter,
            limit=limit
        )
        return [{"id": r.id, "score": r.score, "data": r.payload} for r in results]
    
    def get(self, doc_id: str) -> Dict:
        result = self.client.retrieve(collection_name=self.collection_name, ids=[doc_id])
        return {"id": result[0].id, "data": result[0].payload} if result else None
    
    def update(self, doc_id: str, data: Dict[str, Any]) -> bool:
        vector = self.encoder.encode(data['text']).tolist()
        point = PointStruct(id=doc_id, vector=vector, payload=data)
        self.client.upsert(collection_name=self.collection_name, points=[point])
        return True
    
    def delete(self, doc_ids: List[str]) -> bool:
        self.client.delete(collection_name=self.collection_name, points_selector=doc_ids)
        return True