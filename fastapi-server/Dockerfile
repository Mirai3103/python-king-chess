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
EXPOSE 1234
CMD ["python", "main.py"]