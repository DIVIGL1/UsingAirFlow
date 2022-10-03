cd ../..
mkdir airflow
cd 
cd airflow
copy "..\airflow_hw\scripts\docker-compose.yaml" "docker-compose.yaml"
copy "..\airflow_hw\scripts\CopyData.bat" "CopyData.bat"
copy "..\airflow_hw\scripts\PiPInstall.bat" "PiPInstall.bat"

mkdir logs
mkdir dags
mkdir plugins
docker-compose up airflow-init
docker-compose up
