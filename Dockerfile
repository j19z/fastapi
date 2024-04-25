FROM python:3.11.9

WORKDIR /usr/src/app # this is the rounte where the files are going to be stored inside the container. 

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]