# soc-chatbot

### Quick Start Guide

#### Prerequisite

- Python
- Poetry Follow this [Poetry installation tutorial](https://python-poetry.org/docs/#installing-with-pipx) to install Poetry on your system

Follow these instructions to set up and run the chatbot application:

#### 1. Install Dependencies

Make sure Poetry is installed on your system, then navigate to your project's root directory and run:

```bash
poetry install --no-root
```

#### 2. Set Up Environment Variables

Rename your environment file and update it with your configuration values:

```bash
mv .env.example .env
```

Edit the `.env` file to configure your environment variables:

- **DOCHUB_AUTH_KEY**: Your personal authentication key used to access and retrieve content from DocHub.

- **OPENAI_API_KEY**: Your OpenAI API key, which allows your chatbot to interact with OpenAI services.

#### 2. Activate the Poetry Virtual Environment

Activate the Poetry-managed Python environment:

```bash
poetry shell
```

#### 3. Run the Chatbot Application

Start the chatbot server by executing:

```bash
python app.py
```

Your application should now be running and accessible at the specified address (usually `http://localhost:3000`).

#### Notes:
