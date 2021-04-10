#Dockerfile
FROM python:3

WORKDIR /usr/app/dealScraper.py

COPY dealScraper.py dealScraper.py

RUN pip install requests
RUN pip install beautifulsoup4

# 'u' for printing to console
CMD [ "python" ,"-u", "dealScraper.py"]