#FROM nginx:alpine
FROM python:3.10-alpine

# add bash etc as alpine version doesn't have these
RUN apk add --no-cache bash git gawk sed grep bc coreutils 

# this modules enable use to build bcrypt
RUN apk --no-cache add --virtual build-dependencies gcc g++ make libffi-dev

# this needs to match the directory/package name of the python app
COPY . /lister
WORKDIR /lister
RUN mkdir -p /lister/log


# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8400 available to the world outside this container
EXPOSE 8400

# Define environment variables here
# args are passed it from cli or docker-compose.yml

# Run app.py when the container launches
CMD ["gunicorn", "-b", "0.0.0.0:8400", "lister:app"]
