from sentence_transformers import util, SentenceTransformer
import torch
import numpy as np

def embed_n_retrieve(LST_OF_CHUNKS: list[str],
                     QUERY: str,
                     NUMBER_OF_RESULTS = 5,
                     MODEL_NAME_OR_PATH = "all-mpnet-base-v2",
                     DEVICE = "cpu") -> list: #returns list of len 2

    embedding_model = SentenceTransformer(model_name_or_path=MODEL_NAME_OR_PATH, device=DEVICE)

    lst_of_embeddings = []
    for chunk in LST_OF_CHUNKS:
        lst_of_embeddings.append(embedding_model.encode(chunk))
    print("Ensure number of embeddings = number of chunks")
    print(len(lst_of_embeddings))
    print("\n")
    print("\n")

    embeddings = torch.tensor(np.array(lst_of_embeddings), dtype=torch.float32).to(DEVICE)
    print("embeddings of tensor type has this shape (the 2nd dimension depends on the embedding model you choose): ")
    print(embeddings.shape)
    print("\n")
    print("\n")

    query_embedding = embedding_model.encode(QUERY, convert_to_tensor=True)

    dot_scores = util.dot_score(a=query_embedding, b=embeddings)[0]

    return torch.topk(dot_scores, k=NUMBER_OF_RESULTS) #get top k results

    