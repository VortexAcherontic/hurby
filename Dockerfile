FROM python:3

WORKDIR /app

COPY . .
RUN pip3 install pipreqs
RUN pipreqs .
RUN pip3 install -r requirements.txt

CMD [ "python", "hurby/run.py"]
