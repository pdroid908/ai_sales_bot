FROM python:3.12-slim

# Membuat user agar lebih aman
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Menginstal dependensi
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Menyalin kode dan data
COPY --chown=user . /app

# Hugging Face wajib menggunakan port 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]