# Hall Reservation Chatbot

A Streamlit-based chatbot application developed for IDA (Istrian Development Agency) to automate space reservations in Coworking Pula. The chatbot uses OpenAI's language models to handle natural language conversations in Croatian and helps users reserve different types of spaces including halls, meeting rooms, and coworking spaces.

## Features

- Natural language interaction in Croatian
- Real-time availability checking
- Reservation management for:
  - Conference halls
  - Meeting rooms
  - Coworking spaces
- User-friendly Streamlit interface
- Integration with OpenAI's models

## Prerequisites

- Python 3.8+
- OpenAI API key
- uv package manager (`pip install uv`)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/EDIH-Adria-UNIPU/hall-reservation-chatbot.git
```

2. Create and activate a virtual environment using uv:

```bash
uv sync
```

3. Set up your OpenAI API key in Streamlit's secrets.toml file:

```toml
OPENAI_API_KEY = "your-api-key-here"
```

## Usage

1. Generate initial dummy data:

```bash
uv run src/generate_dummy_data.py
```

2. Run the Streamlit application:

```bash
streamlit run src/app.py
```

3. Access the application through your web browser at `http://localhost:8501`

## Project Structure

- `src/`
  - `app.py` - Main Streamlit application
  - `data_manager.py` - Handles data operations and reservations
  - `functions.py` - Defines available chatbot functions
  - `utils.py` - Utility functions
  - `prompts/` - Contains system messages and prompts
  - `assets/` - Static assets like logos
- `pyproject.toml` - Project metadata and dependencies
- `.streamlit/` - Streamlit configuration files

## Development

This project is part of a Test-before-invest (TBI) initiative for IDA, developed as a prototype (TRL 3-4) to demonstrate the capabilities of AI-powered chatbots for space reservation management.

## Technical Details

- Built with Streamlit for the web interface
- Uses OpenAI's language models for natural language processing
- Polars for efficient data handling
- Implements function calling for availability checking and reservation management

## Limitations

- Prototype version (TRL 3-4)
- Standalone system without integration to existing IDA systems
- Demo database with generated dummy data
- Croatian language support only