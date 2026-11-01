
from google import genai
import os

def get_ai_response(question, df):

    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    dataset_info = f"""
    Dataset Shape: {df.shape}

    Columns:
    {df.dtypes.to_string()}

    Dataset Preview:
    {df.head(10).to_string()}

    Statistical Summary:
    {df.describe(include='all').to_string()}
    """

    prompt = f"""
    You are an expert Business Data Analyst.

    Analyze the following dataset:

    {dataset_info}

    User Question: {question}

    Instructions:
    1. Provide clear and structured answers.
    2. Never invent numerical values.
    3. Use the provided statistics and dataset preview.
    4. Identify business trends and patterns.
    5. Provide actionable recommendations.
    6. Mention limitations when data is insufficient.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"AI Analysis Error: {str(e)}"
