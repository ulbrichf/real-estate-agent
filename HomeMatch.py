from langchain_community.document_loaders.csv_loader import CSVLoader


from config import PROMPT_FILE, OUTPUT_FILE, LLM_MODEL
from db_service import DBService
from llm_service import load_api_key,load_prompt, get_llm_response
from csv_service import save_csv_data

def generate_listings():
    """Generates the CSV data using the LLM and saves it to a file."""

    if OUTPUT_FILE.exists():
        if OUTPUT_FILE.stat().st_size > 0:  # Check if the file has records
            print("Output file already exists and contains data. Skipping generation.")
            return
        else:
            print("Output file exists but is empty. Proceeding with generation.")

    prompt = load_prompt(PROMPT_FILE)

    csv_data = get_llm_response(prompt, LLM_MODEL)
    
    if not csv_data.startswith("ID,Type,Price,Bedrooms,Bathrooms,Size_m2,Location,Lifestyle,Amenities,NearbyPOI,Description"):
        print("Warning: LLM response did not start with the expected CSV header.")
        print("The file will be saved, but may be invalid.")
    
    save_csv_data(csv_data, OUTPUT_FILE)

def store_listings(db_service: DBService):
    """Loads the CSV data, creates embeddings, and stores them in a vector database."""

    loader = CSVLoader("docs/listing_data.csv")
    docs = loader.load()

    if not docs:
        print("\n❌ Error: The CSV file is empty. Please ensure the file contains valid data.")
        exit(1)  # Exit the program gracefully

    db_service.store_documents(docs)


load_api_key()

generate_listings()

db_service = DBService()
store_listings(db_service)

questions = [   
                "How big do you want your house to be?",
                "What are 3 most important things for you in choosing this property?",
                "Which amenities would you like?",
                "Which transportation options are important to you?",
                "How urban do you want your neighborhood to be?",   
            ]
answers = [
    "A comfortable three-bedroom house with a spacious kitchen and a cozy living room.",
    "A quiet neighborhood, good local schools, and convenient shopping options.",
    "A backyard for gardening, a two-car garage, and a modern, energy-efficient heating system.",
    "Easy access to a reliable bus line, proximity to a major highway, and bike-friendly roads.",
    "A balance between suburban tranquility and access to urban amenities like restaurants and theaters."
]

query = " ".join(answers)

context = db_service.retrieve_similar(query, k=5)

print("Top 5 similar property listings based on user preferences:")
for i, doc in enumerate(context):
    # Use the LLM to augment the listing description
    prompt = (
        f"You are a real estate agent. "
        f"Given the following property listing:\n\n{doc.page_content}\n\n"
        f"And the buyer's preferences:\n{query}\n\n"
        "Rewrite the listing description to subtly emphasize features that match the buyer's preferences. "
        "Do not add or change any factual information—only highlight relevant aspects."
    )
    response = get_llm_response(prompt, LLM_MODEL)
    print(f"{i + 1}. {response}")
