# HomeMatch Project

## Getting Started

Follow these steps to set up and run the HomeMatch project from scratch:

1. **Clone the repository** (if not already done):
    ```
    git clone <repository-url>
    cd HomeMatch
    ```

2. **Create and activate a virtual environment**:
    - On Windows:
      ```
      python -m venv venv
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```
      python3 -m venv venv
      source venv/bin/activate
      ```

3. **Install the required dependencies**:
    ```
    pip install -r requirements.txt
    ```

4. **Run the project**:
    ```
    python HomeMatch.py
    ```
## Configuration

Before running the project, ensure you have set up the following environment variables in the `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key.
- `OPENAI_API_BASE`: The base URL for the OpenAI API.

These are required for the application to interact with the OpenAI services.

## Dependencies

The following dependencies are used in this project (see `requirements.txt` for exact versions):

- langchain-community (for LLM and agent utilities)
- langchain-chroma (for Chroma vector database integration)
- langchain-openai (for OpenAI LLM integration)
- python-dotenv (for environment variable management)


## Detailed Functionality

### 1. Entry Point: `HomeMatch.py`
This is the main script that orchestrates the application's functionality. It includes the following steps:
- **Initialization:** Loads configurations and initializes services like the LLM, vector database, and other utilities.
- **Data Generation:** Uses an LLM to generate synthetic real estate listings, which are stored in a CSV file.
- **Database Setup:** Embeds the generated listings and stores them in a vector database for semantic search.
- **User Interaction:** Provides an interface (CLI, API, or GUI) for users to input their preferences and retrieve personalized results.

### 2. Core Functionalities

#### a. Synthetic Data Generation
- **Purpose:** Generate diverse and realistic real estate listings.
- **How It Works:**
  - A prompt is sent to the LLM (via `llm_service.py`) to create listings with details like location, price, size, and amenities.
  - The generated listings are saved in a CSV file (`docs/listing_data.csv`).

#### b. Vector Database Creation
- **Purpose:** Store and organize the embeddings of real estate listings for efficient semantic search.
- **How It Works:**
  - The `db_service.py` module creates a Chroma vector database.
  - Each listing is converted into an embedding (numerical representation) using the LLM.
  - These embeddings are stored in the database for future searches.

#### c. Semantic Search
- **Purpose:** Match real estate listings to user preferences.
- **How It Works:**
  - User preferences (e.g., "3-bedroom house near a park") are converted into an embedding.
  - The vector database is queried to find listings with similar embeddings.
  - The most relevant listings are returned to the user.

#### d. Augmented Response Generation
- **Purpose:** Personalize the descriptions of the matched listings based on user preferences.
- **How It Works:**
  - The LLM is used to rewrite the descriptions of the top-matched listings.
  - The rewritten descriptions emphasize features that align with the user's preferences, making them more appealing.

### 3. Supporting Modules

#### a. `llm_service.py`
- Handles interactions with the Large Language Model (LLM).
- Functions include generating listings and rewriting descriptions.

#### b. `db_service.py`
- Manages the Chroma vector database.
- Functions include storing embeddings and performing semantic searches.

#### c. `csv_service.py`
- Handles reading and writing of CSV files.
- Used for saving generated listings and loading them into the database.

### 4. User Workflow
1. **Data Generation:**
   - The application generates synthetic real estate listings using the LLM.
2. **Database Setup:**
   - The listings are embedded and stored in the vector database.
3. **Input Preferences:**
   - The user provides their preferences (e.g., "2-bedroom apartment in the city center").
4. **Semantic Search:**
   - The application searches the database for listings that match the preferences.
5. **Personalized Results:**
   - The top-matched listings are presented with personalized descriptions.

### 5. Key Features
- **Realistic Listings:** Generated using an LLM to ensure diversity and realism.
- **Efficient Search:** Uses a vector database for fast and accurate semantic search.
- **Personalized Descriptions:** Tailored to user preferences for a better experience.
- **Scalability:** Can handle large datasets and complex queries.

