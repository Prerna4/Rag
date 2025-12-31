Mini RAG System - Setup and Run Instructions:

Step 1: Create Project Structure:
    ->mkdir rag-project->
    cd rag-project

Step 2: Generate Sample Documents:
    ->run create_docs.py
    ->python create_documents.py
    (This will create a docs/ directory with sample documents)

step 3: Requirements:
    ->run requirement.txt file
    ->pip install -r requirement.txt

Step 4: Generate Sample Documents:
    ->run rag_pipeline.py
    ->python rag_pipeline.py

step 5: Testing
Sample testing queries:
    1.What is the warranty for UltraBlend 3000?
    2.How do I schedule maintenance for UltraBlend 3000?
    3.How many paid leaves do employees get?
    4.How long do returns take to process refunds?
    5.Does SafeGrill have auto-shutoff?

step 6: Debugging:
    python rag_pipeline.py --debug -k 3




