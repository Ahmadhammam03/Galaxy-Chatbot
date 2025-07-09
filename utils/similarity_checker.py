
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
import torch

class SimilarityChecker:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.embeddings_cache = {}
        
    def encode_questions(self, questions: List[str]) -> np.ndarray:
        """Encode questions to embeddings"""
        # Use cache for efficiency
        uncached = [q for q in questions if q not in self.embeddings_cache]
        if uncached:
            new_embeddings = self.model.encode(uncached, convert_to_tensor=True)
            for q, emb in zip(uncached, new_embeddings):
                self.embeddings_cache[q] = emb
        
        embeddings = [self.embeddings_cache[q] for q in questions]
        return torch.stack(embeddings) if embeddings else torch.tensor([])
    
    def find_similar_qa(self, user_question: str, qa_database: List[dict], 
                       top_k: int = 3, threshold: float = 0.75) -> List[Tuple[dict, float]]:
        """Find most similar Q&A pairs"""
        if not qa_database:
            return []
        
        # Encode user question
        user_embedding = self.model.encode(user_question, convert_to_tensor=True)
        
        # Encode all database questions
        db_questions = [item['prompt'] for item in qa_database]
        db_embeddings = self.encode_questions(db_questions)
        
        # Calculate similarities
        similarities = torch.nn.functional.cosine_similarity(
            user_embedding.unsqueeze(0), db_embeddings
        )
        
        # Get top matches above threshold
        top_indices = torch.argsort(similarities, descending=True)[:top_k]
        results = []
        
        for idx in top_indices:
            score = similarities[idx].item()
            if score >= threshold:
                results.append((qa_database[idx], score))
        
        return results
    
    def is_relevant_question(self, question: str, keywords: List[str]) -> bool:
        """Check if question is relevant to our domains"""
        question_lower = question.lower()
        
        # Direct keyword matching
        if any(keyword in question_lower for keyword in keywords):
            return True
        
        # Check for related terms
        galaxy_related = ['jordan', 'amman', 'nonprofit', 'recycling', 'empowerment']
        alibaba_related = ['cloud', 'computing', 'certification', 'training', 'china']
        
        all_related = galaxy_related + alibaba_related
        return any(term in question_lower for term in all_related)
