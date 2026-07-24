FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg curl unzip

# Install Deno (JS runtime needed by yt-dlp for signature decryption)
RUN curl -fsSL https://deno.land/install.sh | sh
ENV PATH="/root/.deno/bin:${PATH}"

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
