rem -----------------------------------------------------------------------------
docker cp ../airflow_hw/dags/hw_dag.py airflow-airflow-scheduler-1:/opt/airflow/dags

docker exec -it -u root airflow-airflow-scheduler-1 mkdir airflow_hw
docker exec -it -u root airflow-airflow-worker-1 mkdir airflow_hw
docker cp ../airflow_hw/modules/ airflow-airflow-scheduler-1:/opt/airflow/airflow_hw/
docker cp ../airflow_hw/modules/ airflow-airflow-worker-1:/opt/airflow/airflow_hw/

docker exec -it -u root airflow-airflow-worker-1 mkdir airflow_hw/data
docker exec -it -u root airflow-airflow-worker-1 mkdir airflow_hw/data/models
docker exec -it -u root airflow-airflow-worker-1 mkdir airflow_hw/data/predictions
docker exec -it -u root airflow-airflow-worker-1 mkdir airflow_hw/data/test
docker exec -it -u root airflow-airflow-worker-1 mkdir airflow_hw/data/train

rem -----------------------------------------------------------------------------
docker cp ../airflow_hw/data/test/ airflow-airflow-worker-1:/opt/airflow/airflow_hw/data/
docker cp ../airflow_hw/data/train/ airflow-airflow-worker-1:/opt/airflow/airflow_hw/data/

rem -----------------------------------------------------------------------------
docker exec -it -u root airflow-airflow-worker-1 chmod -R 777 airflow_hw/modules
docker exec -it -u root airflow-airflow-worker-1 chmod -R 777 airflow_hw/data
rem -----------------------------------------------------------------------------
