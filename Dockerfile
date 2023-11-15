# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./{{ cookiecutter.project_name }} /code/{{ cookiecutter.project_name }}

# fastapi launch
CMD ["uvicorn", "{{ cookiecutter.project_name }}.__main__:app", "--host", "0.0.0.0", "--port", "80"]