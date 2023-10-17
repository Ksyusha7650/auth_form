FROM python:3.6.9

# system update & package install
COPY . .
WORKDIR .

# pip & requirements
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000

# Execute
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]