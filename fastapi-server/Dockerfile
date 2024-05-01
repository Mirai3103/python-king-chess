# 
FROM python:3.9

# 
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app
COPY  main.py /code/main.py
COPY ./static /code/static
COPY  ./stockfish /code/stockfish
RUN chmod 777 /code/stockfish/linux/stockfish
EXPOSE 1234
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1234"]