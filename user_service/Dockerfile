FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ENV AWS_ACCESS_KEY_ID=enter_your_access_key_here
# ENV AWS_SECRET_ACCESS_KEY=enter_your_secret_key_here
ENV AWS_REGION=us-east-1

COPY . .

EXPOSE 5001

CMD ["python", "run.py"]
