FROM python:3.10.9

RUN apt-get update && apt-get install -y \
    libldap2-dev \
    libsasl2-dev \
    libmariadb-dev \
    build-essential

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install ispyb-models-daiquiri

COPY ./pyispyb /app/pyispyb/
COPY ./config/docker.env /app/config/docker.env
COPY ./uvicorn.sh /app/uvicorn.sh
COPY ./auth.yml /app/auth.yml

ENV ISPYB_ENVIRONMENT="docker"


#EXPOSE 8000

CMD ["uvicorn",\
    "pyispyb.app.main:app",\
    "--host", "0.0.0.0",\
    "--port", "8000",\
    "--root-path", "/api"]
