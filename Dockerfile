FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg curl git

# Install Node.js (needed for PO token provider server)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

WORKDIR /app

# Clone and build the PO token provider server
RUN git clone --single-branch --branch 1.3.1 https://github.com/Brainicism/bgutil-ytdlp-pot-provider.git /app/bgutil-server
WORKDIR /app/bgutil-server/server
RUN npm ci && npx tsc

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Startup script: run PO token server in background, then start API
RUN echo '#!/bin/bash\n\
node /app/bgutil-server/server/build/main.js &\n\
sleep 3\n\
uvicorn main:app --host 0.0.0.0 --port 10000' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]
