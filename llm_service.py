import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from openai import OpenAIError
import time

def load_api_key():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE")

    if not api_key:
        print("\n❌ Error: OPENAI_API_KEY not found. Please create a .env file with your key.")
        print("Exiting the program. Ensure the .env file is properly configured.")
        exit(1)  # Exit the program gracefully

    if not api_base:
        print("\n❌ Error: OPENAI_API_BASE not found. Please create a .env file with your base URL.")
        print("Exiting the program. Ensure the .env file is properly configured.")
        exit(1)  # Exit the program gracefully

    print("\n✅ OpenAI API key and base URL successfully loaded.")

def load_prompt(file_path: str) -> str:
    """Loads the prompt text from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"\n❌ Error: Prompt file not found at {file_path}")
        raise

def retry_on_failure(func, retries=3, delay=2):
    """Retries a function on failure up to a specified number of retries."""
    for attempt in range(retries):
        try:
            return func()
        except OpenAIError as e:
            print(f"\n⚠️ Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print("\n❌ All retry attempts failed.")
                raise

def validate_llm_response(response: str) -> bool:
    """Validates the LLM response to ensure it meets the expected format."""
    if not response:
        print("\n❌ Error: LLM response is empty.")
        return False

    # Example validation: Ensure the response contains at least one sentence
    if len(response.split('.')) < 2:
        print("\n⚠️ Warning: LLM response does not contain enough content.")
        return False

    return True

def get_llm_response(prompt_text: str, model: str) -> str:
    """Invokes the LLM and returns the raw text response, handling errors with retries."""
    print(f"Initializing model: {model}...")

    def invoke():
        llm = ChatOpenAI(model=model, temperature=0.3)
        print("Sending prompt to OpenAI... (This may take a moment)...")
        response = llm.invoke(prompt_text)
        if validate_llm_response(response.content):
            return response.content
        else:
            raise ValueError("Invalid LLM response format.")

    try:
        return retry_on_failure(invoke)
    except Exception as e:
        print(f"\n❌ Unexpected error during LLM invocation: {e}")
        return ""