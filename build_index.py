from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Load the FAQ file
with open('knowledge_base.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Split into Q&A chunks (each block separated by blank line)
chunks = [chunk.strip() for chunk in content.split('\n\n') if chunk.strip()]

print(f"Total chunks: {len(chunks)}")

# Load embedding model (same one you used in HFI project)
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')

# Create embeddings
embeddings = model.encode(chunks, show_progress_bar=True)
embeddings = np.array(embeddings).astype('float32')

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save index and chunks
faiss.write_index(index, 'faiss_index/loan_faq.index')
with open('faiss_index/chunks.pkl', 'wb') as f:
    pickle.dump(chunks, f)

print("Index built and saved successfully!")