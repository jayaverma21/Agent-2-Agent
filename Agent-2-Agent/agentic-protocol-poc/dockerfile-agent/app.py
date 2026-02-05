import os
from pathlib import Path
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version="2024-02-15-preview"  # IMPORTANT for Azure chat
)

def generate_dockerfile():
    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        messages=[
            {
                "role": "system",
                "content": "You are a DevOps expert who only outputs valid Dockerfile content."
            },
            {
                "role": "user",
                "content": """
Create a Dockerfile for a simple Python application.

Requirements:
- Base image: python:3.11-slim
- Workdir: /app
- Copy all files
- Install requirements.txt
- Expose port 8000
- Run app.py

Return ONLY the Dockerfile. No explanation.
"""
            }
        ]
    )

    return response.choices[0].message.content.strip()

def main():
    dockerfile_content = generate_dockerfile()

    dockerfile_path = Path("../shared/Dockerfile")
    dockerfile_path.write_text(dockerfile_content)

    print("[Agent-1] Dockerfile generated using Azure OpenAI")
    print("[Agent-1] Saved to ../shared/Dockerfile")
    print("[Agent-1] Delegating build & push to Agent-2")

if __name__ == "__main__":
    main()