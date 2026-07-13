FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY setup.py .

RUN pip install --no-cache-dir torch torchaudio torchcodec --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir demucs==4.0.1

RUN pip install --no-cache-dir \
    pydub==0.25.1 \
    librosa \
    numpy \
    diffq \
    tqdm \
    watchdog \
    gradio

FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /workspace

COPY . /workspace

RUN pip install --no-cache-dir -e . --no-deps

EXPOSE 7860
CMD ["python", "-m", "museic.gradio_app"]
