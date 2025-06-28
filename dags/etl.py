from airflow.decorators import dag, task
from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.hooks.base import BaseHook
import json
from datetime import datetime, timedelta

from dotenv import load_dotenv
import os

load_dotenv()

@dag(
    dag_id = "nasa_postgress",
    start_date = datetime.now() - timedelta(days=1),
    schedule = "@daily",
    catchup=False
)
def pipeline_tasks():
    
    @task
    def table_creation():
        postgres_hook = PostgresHook(postgres_conn_id = "conn_id")

        create_table_query = """
        CREATE TABLE IF NOT EXISTS apod_data (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE,
            media_type VARCHAR(50))
        """
        postgres_hook.run(create_table_query)

    @task
    def get_nasa_apod_data():
        nasa_conn = BaseHook.get_connection('nasa_api')
        api_key = json.loads(nasa_conn.extra).get('api_key')

        def custom_response_filter(response):
            rate_limit_limit = response.headers.get('X-RateLimit-Limit')
            rate_limit_remaining = response.headers.get('X-RateLimit-Remaining')
            
            print(f"API Rate Limit: {rate_limit_limit}")
            print(f"API Rate Limit Remaining: {rate_limit_remaining}")

            return {
                "data": response.json(),
                "headers": {
                    "X-RateLimit-Limit": rate_limit_limit,
                    "X-RateLimit-Remaining": rate_limit_remaining
                }
            }

        extract_apod_operator = HttpOperator(
            task_id='extract_apod',
            http_conn_id='nasa_api',
            endpoint='planetary/apod',
            method='GET',
            data={'api_key': api_key}, 
            response_filter=custom_response_filter,
        )
        
        return extract_apod_operator.execute(context={})

    @task
    def transform_apod_data(response_data_and_headers):
        raw_data = response_data_and_headers["data"]
        headers = response_data_and_headers["headers"]

        print(f"Transforming data with headers: {headers}")

        apod_data = {
            'title' : raw_data.get('title', ''),
            'explanation' : raw_data.get('explanation', ''),
            'url' : raw_data.get('url', ''),
            'date' : raw_data.get('date', ''),
            'media_type' : raw_data.get('media_type', '')
        }
        return apod_data
    
    @task
    def load_data_to_postgres(apod_data):
        postgres_hook = PostgresHook(postgres_conn_id = "conn_id")

        insert_query = """
        INSERT INTO apod_data (title, explanation, url, date, media_type)
        VALUES (%s,%s,%s,%s,%s);
        """
        postgres_hook.run(insert_query, parameters=(
            apod_data["title"],
            apod_data["explanation"],
            apod_data["url"],
            apod_data["date"],
            apod_data["media_type"]
        ))

    create_table_task = table_creation()
    nasa_data_and_headers = get_nasa_apod_data() 
    transformed_data = transform_apod_data(nasa_data_and_headers)
    
    create_table_task >> nasa_data_and_headers
    nasa_data_and_headers >> transformed_data
    transformed_data >> load_data_to_postgres(transformed_data)

dag = pipeline_tasks()