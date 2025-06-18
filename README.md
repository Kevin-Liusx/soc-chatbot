# soc-chatbot

## Quick Start Guide

This guide explains how to run the chatbot either **locally** or on a **remote GPU server** using Python virtual environments (`venv`).

---

### Option 1: Running on Local Machine

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

- **DOCHUB_USERNAME**: The username for your DocHub account. This is typically the email address or username you use to log in to DocHub.

- **DOCHUB_PASSWORD**: The password for your DocHub account. Ensure this is kept secure and not shared publicly.

- **OPENAI_API_KEY**: Your OpenAI API key, which allows your chatbot to interact with OpenAI services.

- **CHATBOT_API_KEY**: SOC chatbot api key, make sure to add this key to the frontend as well. This key could be anything as long as the key in the frontend matches the key stored in the backend

#### 3. Activate the Virtual Environment

Go to the root directory of your chatbot and activate the environment by running:

```bash
source venv/bin/activate
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

If the application initialization process is interrupted or fails unexpectedly, please perform the following cleanup steps before rerunning:

- Delete the `general_data` and `techstaff_data` folders located under the `documents/` directory.
- Delete the `db/` folder located under the models/ directory.

If you see an error saying pandoc is not found after you run the application, please do the following:

- Delete the `general_data` folder and `techstaff_data` folder under documents directory. Delete the `db` folder under models directory.
- Run the following commands line by line:

```bash
python
import pypandoc
pypandoc.get_pandoc_path()
```

- Run the app.py

Your application should now be running and accessible at the address `http://localhost:3000`.

### Option 2: Running on Remote GPU Server (with venv)

#### Prerequisite

- Python
- gunicorn

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

- **DOCHUB_USERNAME**: The username for your DocHub account. This is typically the email address or username you use to log in to DocHub.

- **DOCHUB_PASSWORD**: The password for your DocHub account. Ensure this is kept secure and not shared publicly.

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

#### 5. Create the `run.sh` Script

Inside the project root directory, create a file named `run.sh`:

```bash
touch run.sh
chmod +x run.sh
```

Paste the following content into run.sh:

```bash
gunicorn --workers=4 \
         --bind=0.0.0.0:8000 \
         --log-file=logs/gunicorn.log \
         --log-level=DEBUG \
         --daemon app:app
```

`NOTE:` Ensure the logs/ directory exists, or modify the path accordingly.

#### 6. Run the Chatbot Application

Start the chatbot server by:

```bash
./run.sh
```

This will start the Flask app using gunicorn in the background, bound to port `3000`.
Make sure your environment is activated.

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

Your chatbot should now be live at `http://<server-ip>:3000`.
