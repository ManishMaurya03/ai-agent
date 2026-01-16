import os
from openai import OpenAI
from config import OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)

def main():
    

    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input="The food was delicious and the waiter...",
        encoding_format="float"
    )

    # 🔹 Print full response object (metadata + embedding)
    print(response)

    # 🔹 Print only the embedding vector
    embedding_vector = response.data[0].embedding
    print("\nEmbedding vector:")
    print(embedding_vector)

    # 🔹 Optional: print embedding size
    print("\nEmbedding dimension:", len(embedding_vector))

if __name__ == "__main__":
    main()