# syntax=docker/dockerfile:1

FROM python:3

#ENV HURBY_DEVMODE=1

WORKDIR /app

COPY . .
RUN pip3 install pipreqs
RUN pipreqs .
RUN pip3 install -r requirements.txt

CMD [ "python", "run.py"]
