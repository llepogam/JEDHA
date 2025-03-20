FROM continuumio/miniconda3

WORKDIR /home/app

RUN apt-get update
RUN apt-get install nano unzip
RUN apt install curl -y

RUN curl -fsSL https://get.deta.dev/cli.sh | sh

COPY requirements.txt /dependencies/requirements.txt
RUN pip install --no-cache-dir -r /dependencies/requirements.txt


COPY . /home/app

# Use shell form of CMD to allow environment variable substitution
CMD streamlit run app.py --server.port=${PORT} --server.address=0.0.0.0