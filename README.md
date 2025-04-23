# Mental Health Journal and Analysis

Welcome to the Mental Health Journal and Analysis project, powered by [crewAI](https://crewai.com). This application provides a platform for users to write journal entries and receive automated therapeutic insights based on different psychological approaches.

## Features

- **Journal Entry System**: Write and save personal journal entries
- **Multi-perspective Analysis**: Receive insights from different therapeutic approaches:
  - Cognitive Behavioral Therapy (CBT)
  - Humanistic Therapy
  - Psychodynamic Therapy
- **Mood Analysis**: Get an assessment of your emotional state based on your journal entries
- **History Tracking**: View all past journal entries and their analyses
- **Web Interface**: User-friendly Flask-based web application

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

## Environment Variables

**IMPORTANT**: Before running the application, you must set up the following environment variables in a `.env` file in the root directory of the project. These variables are essential for the application to function properly.

Create a `.env` file with the following variables:

```
model=
CEREBRAS_API_KEY=
OPIK_API_KEY=
OPIK_WORKSPACE=
WEAVIATE_URL=
WEAVIATE_API_KEY=
```

Fill in the values for each variable:
- `model`: The AI model to use (e.g., llama3.1-8-b)
- `CEREBRAS_API_KEY`: Your Cerebras API key for accessing their AI services
- `OPIK_API_KEY`: Your OPIK API key for tracking and analytics
- `OPIK_WORKSPACE`: Your OPIK workspace identifier
- `WEAVIATE_URL`: The URL for your Weaviate vector database instance
- `WEAVIATE_API_KEY`: Your Weaviate API key for authentication

These credentials are used for AI model access, analytics tracking, and vector database operations that power the therapeutic analysis features.

## Customizing

- Modify `src/mentalhealth/config/agents.yaml` to define your agents
- Modify `src/mentalhealth/config/tasks.yaml` to define your tasks
- Modify `src/mentalhealth/crew.py` to add your own logic, tools and specific args
- Modify `src/mentalhealth/main.py` to add custom inputs for your agents and tasks

## Running the Project

To start the web application, run this from the root folder of your project:

```bash
python -m src.mentalhealth.app
```

This will start a Flask development server, and you can access the application by navigating to `http://localhost:5000` in your web browser.

Alternatively, to run the crew directly without the web interface:

```bash
crewai run
```

This command initializes the Mental Health Crew, assembling the agents and assigning them tasks as defined in your configuration.

## Understanding Your Crew

The Mental Health Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to analyze journal entries from different therapeutic perspectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Project Structure

- `src/mentalhealth/app.py`: Main Flask application
- `src/mentalhealth/crew.py`: CrewAI configuration and setup
- `src/mentalhealth/database.py`: Database operations for journal entries
- `src/mentalhealth/*.md`: Output files for different types of analyses
- `src/mentalhealth/config/`: Configuration files for agents and tasks
- `src/mentalhealth/tools/`: Custom tools for the agents

#Made with <3 @ Into The Vectorverse @ AWS GenAI Loft
