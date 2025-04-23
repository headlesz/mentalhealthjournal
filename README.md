# Mental Health Journal Analysis

A therapeutic journaling application that analyzes journal entries using multiple therapeutic perspectives powered by AI agents.

## Overview

This application allows users to:

1. Write journal entries about their thoughts and feelings
2. Receive therapeutic insights from multiple perspectives:
   - Cognitive Behavioral Therapy (CBT)
   - Humanistic Therapy
   - Psychodynamic Therapy
3. Get a comprehensive therapy summary integrating all perspectives
4. Receive mood analysis with quantitative emotional assessment
5. View history of past journal entries and analyses

## Installation

### Prerequisites

- Python 3.10 or higher
- [UV](https://docs.astral.sh/uv/) package manager

### Setup

1. Clone this repository
2. Install required packages using UV:

```bash
uv add crewai crewai_tools flask
```

3. Create a `.env` file in the project root with the following variables:

```
model=llama3.1-8-b
CEREBRAS_API_KEY=your_cerebras_api_key
```

Replace `your_cerebras_api_key` with your actual Cerebras API key.

## Project Structure

- `src/mentalhealth/`: Main application directory
  - `app.py`: Flask web application
  - `crew.py`: CrewAI configuration and agent setup
  - `database.py`: SQLite database management
  - `config/`: Configuration files
    - `agents.yaml`: Agent definitions
    - `tasks.yaml`: Task definitions
  - `tools/`: Custom tools for agents
  - HTML templates and CSS for the web interface

## Running the Application

Start the Flask web server:

```bash
python -m src.mentalhealth.app
```

Then open your browser to `http://127.0.0.1:5000/` to access the journal interface.

## How It Works

1. User submits a journal entry through the web interface
2. The entry is processed by multiple AI therapist agents:
   - CBT Therapist: Identifies cognitive distortions and negative thought patterns
   - Humanistic Therapist: Focuses on self-actualization and personal growth
   - Psychodynamic Therapist: Explores unconscious patterns and past influences
3. A Therapy Summarizer agent integrates insights from all perspectives
4. A Mood Rater agent provides quantitative emotional assessment
5. Results are displayed in the web interface and stored in the database

## Features

- **Multi-perspective Analysis**: Get insights from different therapeutic approaches
- **Integrated Summary**: Comprehensive therapeutic guidance combining all perspectives
- **Mood Analysis**: Quantitative assessment of emotional states
- **Journal History**: Access and review past entries and analyses
- **Web Interface**: User-friendly interface for journaling and viewing results

## Customization

You can customize the agents and tasks by modifying the YAML configuration files:

- `src/mentalhealth/config/agents.yaml`: Define agent roles, goals, and backstories
- `src/mentalhealth/config/tasks.yaml`: Define task descriptions and expected outputs

# made with <3 @ Into the Vectorverse @ AWS GenAI Loft
