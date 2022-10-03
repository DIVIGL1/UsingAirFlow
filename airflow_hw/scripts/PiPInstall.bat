rem -----------------------------------------------------------------------------
docker exec -it -u airflow airflow-airflow-scheduler-1 pip install pandas
docker exec -it -u airflow airflow-airflow-scheduler-1 pip install scikit-learn
docker exec -it -u airflow airflow-airflow-worker-1 pip install pandas
docker exec -it -u airflow airflow-airflow-worker-1 pip install scikit-learn
rem -----------------------------------------------------------------------------
