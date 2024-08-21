FROM python:3.11.7

WORKDIR /work
COPY ./requirements.txt /work/requirements.txt
RUN python3 -m pip install -r requirements.txt

COPY ./app /work/app
COPY ./main.py /work/main.py
RUN ls -la

CMD ["python3", "main.py"]