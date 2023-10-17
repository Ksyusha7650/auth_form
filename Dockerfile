FROM python:3.9

# system update & package install
COPY . .
WORKDIR .

# pip & requirements
RUN pip install --no-cache-dir --upgrade -r requirements.txt\
pip install flask_bootstrap

EXPOSE 8000

# Execute
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]