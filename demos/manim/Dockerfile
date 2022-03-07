FROM python:3.10

WORKDIR /code

RUN apt-get update && apt-get install -y libcairo2-dev \ 
libpango1.0-dev \
ffmpeg \
texlive \
texlive-latex-extra \
texlive-fonts-extra \
texlive-science

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
