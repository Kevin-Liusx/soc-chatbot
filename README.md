# soc-chatbot

## Quick Start Guide

This guide explains how to run the chatbot either **locally** using [Poetry](https://python-poetry.org/) or on a **remote GPU server** using Python virtual environments (`venv`).

---

### 🖥️ Option 1: Running on Local Machine (with Poetry)

#### Prerequisite

- Python
- [Poetry](https://python-poetry.org/docs/#installing-with-pipx) (recommended for local development)

#### 1. Install Dependencies

Make sure Poetry is installed on your system, then navigate to your project's root directory and run:

```bash
poetry install --no-root
```

#### 2. Set Up Environment Variables

Create your environment file:

```bash
touch .env
```

Edit the `.env` file to configure your environment variables:

- **DOCHUB_USERNAME**: The username for your DocHub account. This is typically the email address or username you use to log in to DocHub.

- **DOCHUB_PASSWORD**: The password for your DocHub account. Ensure this is kept secure and not shared publicly.

- **OPENAI_API_KEY**: Your OpenAI API key, which allows your chatbot to interact with OpenAI services.

- **CHATBOT_API_KEY**: SOC chatbot api key, make sure to add this key to the frontend as well. This key could be anything as long as the key in the frontend matches the key stored in the backend

#### 3. Activate the Poetry Virtual Environment

Activate the Poetry-managed Python environment:

```bash
poetry shell
```

#### 4. Run the Chatbot Application

Start the chatbot server by executing:

```bash
python app.py
```

Your application should now be running and accessible at the address `http://localhost:3000`.

### 🖥️ Option 2: Running on Remote GPU Server (with venv)

#### Prerequisite

- Python

#### 1. Create the virtual environment

Make sure Python is installed on your system, then navigate to your project's root directory and run:

```bash
python3 -m venv venv
```

#### 2. Set Up Environment Variables

Create your environment file:

```bash
touch .env
```

Edit the `.env` file to configure your environment variables:

- **DOCHUB_AUTH_KEY**: Your personal authentication key used to access and retrieve content from DocHub.

- **OPENAI_API_KEY**: Your OpenAI API key, which allows your chatbot to interact with OpenAI services.

- **CHATBOT_API_KEY**: SOC chatbot api key, make sure to add this key to the frontend as well. This key could be anything as long as the key in the frontend matches the key stored in the backend

#### 3. Activate the Virtual Environment

Go to the root directory of your chatbot and activate the environment by running:

```bash
source folder-name/bin/activate
```

#### 4 Install Dependencies

```bash
pip install -r requirements.txt
```

#### 5. Run the Chatbot Application

Start the chatbot server by executing:

```bash
python app.py
```

Make sure your environment is activated
.

#### Notes:

If you see an error saying pandoc is not found after you run the application, please do the following:

- Delete the `data` folder under documents and the `db` folder under models.
- Run the following commands line by line:

```bash
python
import pypandoc
pypandoc.get_pandoc_path()
```

- Run the app.py

#### Ignore this:

gunicorn -w 4 -b :3000 --daemon app:app
pkill gunicorn
ps aux | grep gunicorn
