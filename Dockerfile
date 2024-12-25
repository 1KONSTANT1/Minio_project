FROM python:3.9-slim

WORKDIR /python_script

COPY ./script.py /python_script

RUN pip3 install --upgrade pillow minio numpy

CMD ["python3", "script.py"]