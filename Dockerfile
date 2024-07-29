FROM ubuntu:latest
LABEL authors="Admin"
EXPOSE 8000
WORKDIR /app

#ENTRYPOINT ["top", "-b"]

RUN apt update && apt install -y python3 python3-pip libpq-dev
#RUN python3 --version


COPY / /app
RUN pip3 install -r requirements.txt --break-system-packages
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]