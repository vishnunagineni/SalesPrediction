FROM python:3.7-slim-buster
#copying requirements file into the container
COPY ./requirements.txt /app/requirements.txt
#changing the work directory
WORKDIR /app
#installing all the dependencies
RUN pip install -r requirements.txt
#copying all the files to container
COPY . /app

#Exposing to particular
EXPOSE 80
#running the flask app
CMD [ "python","./app.py"]
