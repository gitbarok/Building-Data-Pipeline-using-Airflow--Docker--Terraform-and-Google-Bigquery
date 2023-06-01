FROM apache/airflow:2.6.1

ENV AIRFLOW_HOME=/opt/airflow

COPY requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt

WORKDIR $AIRFLOW_HOME

USER $AIRFLOW_UID


