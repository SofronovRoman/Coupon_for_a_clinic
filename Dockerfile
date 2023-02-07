FROM python:3.10

#some envs
WORKDIR /app 

#copy local files
COPY . . 

#install python dependencies
RUN pip install -r requirements.txt

#download and install chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

CMD ["python", "main.py"]