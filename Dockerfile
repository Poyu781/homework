FROM puckel/docker-airflow:1.10.9
WORKDIR /usr/local/airflow
COPY . .
RUN mkdir data
RUN pip install -r requirements.txt
ENV PYTHONPATH "/usr/local/airflow"


