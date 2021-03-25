#set base image
FROM python:3.7.6

#set a working directory for code files
WORKDIR /code

#copy dependencies to workdir
COPY requirements.txt .

#Install reqs
RUN pip install -r requirements.txt

#copy ml code folder 
COPY mlcode/ .

#execute ml code on container start
CMD ["python", "./run_procs.py"]
