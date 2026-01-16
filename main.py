from openai import OpenAI
from config import OPENAI_API_KEY

def main():
    """
    Entry point for the first OpenAI API call.
    """

    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = "Explain what RAG is in one sentence."

    response = client.responses.create(
        model="gpt-4o-mini",          # cost-effective model
        input=prompt,
        max_output_tokens=100,         # HARD safety limit
        temperature=0.2               # focused output
    )

    # Extract output text safely
    output_text = response.output_text

    print("Model Response:")
    print(output_text)

    # Optional: print token usage (good habit)
    print("\nToken Usage:")
    print(response.usage)

if __name__ == "__main__":
    main()