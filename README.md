# Streamlit

Web application using Streamlit to read and write data in Snowflake

## Requirements

For building and running the application you need:

- [Python 3.8.10](https://www.python.org/downloads/release/python-3810/)
- [pipenv](https://www.jetbrains.com/help/pycharm/pipenv.html)

## How to use
### To run the application locally

#### Option 1: Run the application in docker
Required: Docker Desktop

1. Run: `docker-compose up --build`
2. Open browser: `http://localhost:8501/`


#### Option 2: Run the application in virtualenv

1. Run: `.\venv\Scripts\Activate.ps1`
2. Run: `streamlit run .\src\Main.py`
3. Open browser: `http://localhost:8501/`
