FROM python:3.11-slim

WORKDIR /app

# Install standard free fonts so the text looks good and isn't just basic pixel font
RUN apt-get update && apt-get install -y fonts-freefont-ttf && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]