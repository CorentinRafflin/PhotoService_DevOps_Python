# Use an official Python runtime as a parent image
FROM nginx 

COPY default.conf /etc/nginx/conf.d/default.conf

ADD dist /usr/share/nginx/html

WORKDIR /backend_service

# Copy the directory contents of backend_service into the container at /backend_service
ADD . /backend_service

# Install pip3
RUN apt update && apt install -y python3-pip

# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

CMD ["sh","-c","nginx -g 'daemon on;' && python3 backend_service_main.py"]

