# 1️⃣ Base image: Python
FROM python:3.11-slim

# 2️⃣ Create working directory inside container
WORKDIR /app

# 3️⃣ Copy dependency list first (for caching)
COPY requirements.txt .

# 4️⃣ Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Copy the rest of the backend code
COPY . .

# 6️⃣ Expose port FastAPI runs on
EXPOSE 8000

# 7️⃣ Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
