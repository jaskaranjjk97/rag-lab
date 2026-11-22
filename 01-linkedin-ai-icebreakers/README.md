# LinkedIn AI Icebreakers

An AI-powered application that extracts publicly available LinkedIn profile information, generates interesting professional facts, and answers questions about a person's professional background using Retrieval-Augmented Generation (RAG).

Built with **Python, Gradio, LlamaIndex, OpenAI, and HarvestAPI (Apify)**.

## Features

- **LinkedIn Profile Extraction:** Retrieve profile information using HarvestAPI through Apify.
- **Profile Data Normalization:** Convert extracted profile data into a consistent application schema.
- **Document Processing:** Transform profile information into structured LlamaIndex nodes.
- **Vector Search:** Generate embeddings and retrieve relevant profile information.
- **AI-Generated Facts:** Generate three interesting, profile-grounded facts.
- **Profile Q&A:** Ask questions about professional experience, education, skills, and certifications.
- **Mock Mode:** Test the application using a local sample profile without consuming a HarvestAPI extraction credit.

## Architecture

```text
LinkedIn Profile URL
        |
        v
   Gradio Interface
        |
        v
   Data Extraction
   (HarvestAPI / Mock)
        |
        v
  Data Normalization
        |
        v
 Profile Preprocessing
        |
        v
  LlamaIndex Nodes
        |
        v
 OpenAI Embeddings
        |
        v
   Vector Index
        |
        +-------------------+
        |                   |
        v                   v
 Interesting Facts      User Questions
        |                   |
        v                   v
   OpenAI LLM          RAG Retrieval
                            |
                            v
                         OpenAI LLM
                            |
                            v
                       Final Answer
```

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| User interface | Gradio |
| Profile extraction | HarvestAPI via Apify |
| RAG framework | LlamaIndex |
| LLM | OpenAI GPT-4o-mini |
| Embedding model | OpenAI text-embedding-3-small |
| Vector indexing | LlamaIndex VectorStoreIndex |
| Environment management | python-dotenv |

## Project Structure

```text
linkedin-ai-icebreakers/
│
├── app.py
├── config.py
├── mock_profile.json
├── requirements.txt
├── .env.example
├── .gitignore
│
└── modules/
    ├── data_extraction.py
    ├── data_preprocessing.py
    ├── llm_interface.py
    └── query_engine.py
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/jaskaranjjk97/linkedin-ai-icebreakers.git
cd linkedin-ai-icebreakers
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create your `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Add your API credentials:

```env
OPENAI_API_KEY=your_openai_api_key
APIFY_API_TOKEN=your_apify_api_token
```

### 5. Run the application

```bash
python app.py
```

Open the local Gradio interface:

```text
http://localhost:7860
```

## Application Usage

### Mock Mode

1. Open the application.
2. Enable **Use mock profile data**.
3. Click **Process Profile**.
4. Review the generated interesting facts.
5. Open the Chat tab and ask questions.

Mock mode uses the local `mock_profile.json` fixture. OpenAI credentials are still required for embeddings and LLM generation.

### Live Mode

1. Keep **Use mock profile data** disabled.
2. Enter a publicly accessible LinkedIn profile URL.
3. Click **Process Profile**.
4. The application sends the URL to HarvestAPI through Apify.
5. The extracted profile is normalized and indexed.
6. Review the generated facts and ask questions through the Chat tab.

Live extraction may incur Apify usage charges. OpenAI API usage may also incur charges.

## Example Questions

- What are this person's main professional achievements?
- What companies has this person worked for?
- What is their educational background?
- What GenAI initiatives have they contributed to?
- Which skills or certifications are listed?
- What information is not available on the profile?

## Configuration

The application uses the following models:

- **LLM:** `gpt-4o-mini`
- **Embedding:** `text-embedding-3-small`

Model configuration and application settings are maintained in `config.py`.

## Privacy and Responsible Use

- Use profile information only where you have an appropriate reason and permission to process it.
- Respect LinkedIn's terms and applicable privacy requirements.
- Do not commit API credentials or extracted personal profile data to GitHub.
- The application is designed to answer questions using extracted profile information and should not be treated as an authoritative source of personal information.

## Current Status

The application has been tested with both mock and live profile extraction workflows, including profile normalization, vector indexing, interesting-fact generation, and profile-based question answering.

## Future Improvements

- Improve fact generation and conversation starter quality.
- Add source references to generated answers.
- Add profile session cleanup.
- Deploy the application for public demonstration.

## Author

**Jaskaran Singh**

GenAI | RAG | Agentic AI | Python

