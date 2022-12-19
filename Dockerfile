FROM python:3.8.10-slim
COPY src/ /app/src

COPY requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit", "run"]
CMD ["src/Main.py"]
