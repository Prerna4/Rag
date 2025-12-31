import os
import re
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import argparse

class Document:
    """Represents a document with metadata"""
    def __init__(self, filename, content):
        self.filename = filename
        self.content = content

class Passage:
    """Represents a passage/chunk with metadata"""
    def __init__(self, text, source, passage_id):
        self.text = text
        self.source = source
        self.passage_id = passage_id

class RAGSystem:
    def __init__(self, docs_dir='docs', max_words_per_passage=120):
        self.docs_dir = docs_dir
        self.max_words_per_passage = max_words_per_passage
        self.documents = []
        self.passages = []
        self.vectorizer = TfidfVectorizer()
        self.passage_vectors = None
        
    def preprocess_text(self, text):
        """Preprocess text: lowercase, remove punctuation, normalize whitespace"""
        # Lowercase
        text = text.lower()
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Normalize whitespace
        text = ' '.join(text.split())
        return text
    
    def split_into_sentences(self, text):
        """Split text into sentences with better handling"""
        # Split on sentence boundaries
        sentences = re.split(r'(?<=[.!?])\s+', text)
        # Clean up and filter
        cleaned_sentences = []
        for s in sentences:
            s = s.strip()
            # Keep sentences that end with punctuation or are substantial
            if s and (s[-1] in '.!?' or len(s.split()) > 5):
                if s[-1] not in '.!?':
                    s += '.'
                cleaned_sentences.append(s)
        return cleaned_sentences
    
    def create_passages(self, text, filename):
        """Split document into passages of ~120 words"""
        sentences = self.split_into_sentences(text)
        passages = []
        current_passage = []
        current_word_count = 0
        
        for sentence in sentences:
            words = sentence.split()
            word_count = len(words)
            
            # If adding this sentence exceeds limit, save current passage
            if current_word_count + word_count > self.max_words_per_passage and current_passage:
                passages.append(' '.join(current_passage))
                current_passage = [sentence]
                current_word_count = word_count
            else:
                current_passage.append(sentence)
                current_word_count += word_count
        
        # Add remaining passage
        if current_passage:
            passages.append(' '.join(current_passage))
        
        return passages
    
    def ingest_documents(self):
        """Read all .txt files from docs directory"""
        if not os.path.exists(self.docs_dir):
            print(f"Error: Directory '{self.docs_dir}' not found!")
            return
        
        txt_files = [f for f in os.listdir(self.docs_dir) if f.endswith('.txt')]
        
        if not txt_files:
            print(f"No .txt files found in '{self.docs_dir}'")
            return
        
        print(f"Found {len(txt_files)} documents")
        
        for filename in txt_files:
            filepath = os.path.join(self.docs_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                self.documents.append(Document(filename, content))
                
                # Create passages from this document
                passages = self.create_passages(content, filename)
                for i, passage_text in enumerate(passages):
                    passage_id = f"{filename}_passage_{i}"
                    self.passages.append(Passage(passage_text, filename, passage_id))
        
        print(f"Created {len(self.passages)} passages from {len(self.documents)} documents")
    
    def index_passages(self):
        """Index passages using TF-IDF"""
        if not self.passages:
            print("No passages to index!")
            return
        
        # Preprocess all passages
        preprocessed_passages = [self.preprocess_text(p.text) for p in self.passages]
        
        # Create TF-IDF vectors
        self.passage_vectors = self.vectorizer.fit_transform(preprocessed_passages)
        print(f"Indexed {len(self.passages)} passages")
    
    def retrieve(self, query, k=3, debug=False):
        """Retrieve top-k relevant passages"""
        # Preprocess query
        preprocessed_query = self.preprocess_text(query)
        
        if debug:
            print(f"\n--- DEBUG: Preprocessed Query ---")
            print(f"Original: {query}")
            print(f"Preprocessed: {preprocessed_query}")
        
        # Vectorize query
        query_vector = self.vectorizer.transform([preprocessed_query])
        
        # Compute cosine similarities
        similarities = cosine_similarity(query_vector, self.passage_vectors)[0]
        
        # Get top-k indices
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        
        results = []
        for idx in top_k_indices:
            results.append({
                'passage': self.passages[idx],
                'score': similarities[idx]
            })
        
        if debug:
            print(f"\n--- DEBUG: Top {k} Retrieved Passages ---")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. Score: {result['score']:.4f}")
                print(f"   Source: {result['passage'].source}")
                print(f"   ID: {result['passage'].passage_id}")
                print(f"   Text: {result['passage'].text[:200]}...")
        
        return results
    
    def extract_keywords(self, query):
        """Extract potential keywords from query"""
        # Common question words to ignore
        stop_words = {'what', 'is', 'the', 'how', 'do', 'i', 'does', 'have', 'for', 
                      'many', 'long', 'to', 'a', 'an', 'are', 'get', 'can', 'my',
                      'schedule', 'take'}
        
        words = query.lower().split()
        keywords = [w.strip(string.punctuation) for w in words if w.lower() not in stop_words]
        return keywords
    
    def score_sentence_relevance(self, sentence, keywords, query_lower):
        """Score how relevant a sentence is to the query"""
        sentence_lower = sentence.lower()
        score = 0
        
        # Count exact keyword matches
        for keyword in keywords:
            if keyword in sentence_lower:
                score += 2
        
        # Bonus for containing question-related words
        query_words = query_lower.split()
        for word in query_words:
            if len(word) > 3 and word in sentence_lower:
                score += 1
        
        # Penalize very long sentences (likely paragraphs)
        word_count = len(sentence.split())
        if word_count > 50:
            score -= 2
        
        # Bonus for sentences with numbers (often contain specific facts)
        if re.search(r'\d+', sentence):
            score += 1
            
        return score
    
    def generate_answer(self, query, retrieved_results, debug=False):
        """Generate concise answer from retrieved passages"""
        if not retrieved_results or retrieved_results[0]['score'] < 0.01:
            return "I couldn't find relevant information to answer this question.", []
        
        # Extract keywords from query
        keywords = self.extract_keywords(query)
        query_lower = query.lower()
        
        if debug:
            print(f"\n--- DEBUG: Answer Generation ---")
            print(f"Keywords extracted: {keywords}")
        
        # Collect all candidate sentences with scores
        candidate_sentences = []
        
        for result in retrieved_results:
            passage = result['passage']
            sentences = self.split_into_sentences(passage.text)
            
            for sentence in sentences:
                # Skip very short sentences (headers, labels, etc.)
                if len(sentence.split()) < 5:
                    continue
                
                # Score this sentence
                relevance_score = self.score_sentence_relevance(sentence, keywords, query_lower)
                
                if relevance_score > 0:
                    candidate_sentences.append({
                        'sentence': sentence,
                        'score': relevance_score,
                        'source': passage.source,
                        'passage_score': result['score']
                    })
        
        if debug:
            print(f"\nFound {len(candidate_sentences)} candidate sentences")
            for i, cand in enumerate(sorted(candidate_sentences, key=lambda x: x['score'], reverse=True)[:5], 1):
                print(f"\n{i}. Relevance Score: {cand['score']}, Passage Score: {cand['passage_score']:.4f}")
                print(f"   Source: {cand['source']}")
                print(f"   Sentence: {cand['sentence'][:150]}...")
        
        if not candidate_sentences:
            # Fallback: use first sentence from top passage
            top_passage = retrieved_results[0]['passage']
            sentences = self.split_into_sentences(top_passage.text)
            best_sentence = sentences[0] if sentences else top_passage.text
            best_source = top_passage.source
        else:
            # Sort by relevance score, then by passage score
            candidate_sentences.sort(key=lambda x: (x['score'], x['passage_score']), reverse=True)
            best = candidate_sentences[0]
            best_sentence = best['sentence']
            best_source = best['source']
        
        # Clean up the sentence
        best_sentence = best_sentence.strip()
        if not best_sentence.endswith(('.', '!', '?')):
            best_sentence += '.'
        
        return best_sentence, [best_source]
    
    def answer_query(self, query, k=3, debug=False):
        """Main method to answer a query"""
        print(f"\nQuery: {query}")
        
        # Retrieve relevant passages
        retrieved_results = self.retrieve(query, k=k, debug=debug)
        
        # Generate answer
        answer, sources = self.generate_answer(query, retrieved_results, debug=debug)
        
        print(f"\nAnswer (based on retrieved documents):")
        print(answer)
        print(f"\nSources: {', '.join(set(sources))}")
        print("-" * 80)
        
        return answer, sources


def run_tests(rag):
    """Run test queries"""
    print("\n" + "="*80)
    print("RUNNING TEST QUERIES")
    print("="*80)
    
    test_queries = [
        "What is the warranty for UltraBlend 3000?",
        "How do I schedule maintenance for UltraBlend 3000?",
        "How many paid leaves do employees get?",
        "How long do returns take to process refunds?",
        "Does SafeGrill have auto-shutoff?"
    ]
    
    for query in test_queries:
        rag.answer_query(query, k=3, debug=False)


def main():
    parser = argparse.ArgumentParser(description='Mini RAG System')
    parser.add_argument('--query', type=str, help='Query to answer')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--test', action='store_true', help='Run test queries')
    parser.add_argument('--docs-dir', type=str, default='docs', help='Documents directory')
    parser.add_argument('-k', type=int, default=3, help='Number of passages to retrieve')
    
    args = parser.parse_args()
    
    # Initialize RAG system
    rag = RAGSystem(docs_dir=args.docs_dir)
    
    # Ingest and index documents
    print("="*80)
    print("INITIALIZING RAG SYSTEM")
    print("="*80)
    rag.ingest_documents()
    rag.index_passages()
    
    if args.test:
        run_tests(rag)
    elif args.query:
        rag.answer_query(args.query, k=args.k, debug=args.debug)
    else:
        # Interactive mode
        print("\n" + "="*80)
        print("INTERACTIVE MODE (type 'exit' to quit, 'test' to run tests)")
        print("="*80)
        
        while True:
            query = input("\nEnter your question: ").strip()
            
            if query.lower() == 'exit':
                print("Goodbye!")
                break
            elif query.lower() == 'test':
                run_tests(rag)
            elif query:
                rag.answer_query(query, k=args.k, debug=args.debug)


if __name__ == "__main__":
    main()