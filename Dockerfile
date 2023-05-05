FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /backend

COPY ./requirements.txt /tmp/requirements.txt

COPY ./backend /backend

EXPOSE 8000

RUN python -m venv /py && \
  /py/bin/pip install -r /tmp/requirements.txt

ENV PATH='/py/bin:$PATH'
