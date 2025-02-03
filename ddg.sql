CREATE DATABASE airflow_db;
CREATE USER 'airflowr'@'localhost' IDENTIFIED BY 'airflow';
GRANT ALL PRIVILEGES ON airflow_db.* TO 'airflow_user'@'localhost';
FLUSH PRIVILEGES;
