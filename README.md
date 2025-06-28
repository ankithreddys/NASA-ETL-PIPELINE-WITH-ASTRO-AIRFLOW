# NASA EPO Data ETL Pipeline

Welcome to the NASA EPO Data ETL Pipeline project\! This repository contains the Apache Airflow setup and DAGs for extracting, transforming, and loading NASA Education and Public Outreach (EPO) data into a PostgreSQL database. The pipeline is designed to run daily, ensuring an up-to-date dataset for analysis and use.

This project was generated using the Astronomer CLI (`astro dev init`) and has been customized to fit the specific requirements of the NASA EPO data ingestion.

-----

## Project Overview

This project implements a robust ETL pipeline for NASA EPO data. Key features include:

  * **Daily Data Ingestion:** An Airflow DAG is scheduled to run every day, automatically collecting the latest NASA EPO data.
  * **PostgreSQL Storage:** All collected and processed data is stored persistently in a PostgreSQL database, ready for querying and reporting.
  * **Containerized Environment:** Leveraging Docker and Astro Runtime, the project provides a consistent and reproducible environment for local development and future deployment.

-----

## Project Contents

Your Astro project is structured as follows:

  - **dags**: This essential folder contains the Python files defining your Airflow DAGs.
      - `etl.py`: This is the core DAG for your project. It orchestrates the entire ETL process for NASA EPO data, from data collection to its storage in PostgreSQL. This DAG is configured to trigger daily.
  - **Dockerfile**: Defines the Docker image used by Astro Runtime. This file specifies the base Airflow image and any additional configurations or dependencies needed for your project.
  - **include**: This directory is reserved for any supplementary files or assets required by your DAGs (e.g., SQL scripts, configuration files). It is currently empty but can be utilized as your project grows.
  - **packages.txt**: Use this file to declare any OS-level packages required by your Airflow environment. Add package names here if your DAGs depend on system libraries not included in the base Astro Runtime image.
  - **requirements.txt**: This crucial file lists all Python packages necessary for your DAGs to execute successfully. You will likely find packages here such as:
      - `psycopg2-binary`: For connecting to and interacting with your PostgreSQL database.
      - Any libraries used for making API calls or parsing data from the NASA EPO source (e.g., `requests`, `pandas`, `json`).
  - **plugins**: This folder is for custom Airflow plugins or community plugins you wish to integrate into your environment. It is empty by default.
  - **airflow\_settings.yaml**: This local-only file is used for managing Airflow Connections, Variables, and Pools during development. **It is highly recommended to define your PostgreSQL connection details here** instead of manually entering them in the Airflow UI, especially for local testing.

-----

## Deploy Your Project Locally

To get your NASA EPO ETL pipeline running on your local machine:

1.  **Navigate to your project root:** Open your terminal and change directory to this project's root folder.

2.  **Start Airflow:** Run the following command:

    ```bash
    astro dev start
    ```

This command will provision and start five Docker containers on your machine, each corresponding to a different Airflow component:

  - **Postgres**: The database server for Airflow's metadata and, critically, for storing your processed NASA EPO data.
  - **Scheduler**: The Airflow component responsible for monitoring and triggering tasks in your `etl` DAG.
  - **DAG Processor**: The Airflow component that parses your DAG files.
  - **API Server**: The backend for the Airflow UI and programmatic API access.
  - **Triggerer**: (Introduced in Airflow 2.2+) The component responsible for running deferred tasks.

Once all five containers are ready, your web browser will automatically open to the Airflow UI at `http://localhost:8080/`. You can log in using the default credentials (username `admin`, password `admin`).

You can also directly access your local PostgreSQL database at `localhost:5432/postgres` with username `postgres` and password `postgres`. This is where you can verify your ingested NASA EPO data.

**Note:** If `localhost:8080` or `localhost:5432` are already in use on your system, you might encounter port conflicts. Refer to the Astronomer documentation on [troubleshooting local deployments](https://www.astronomer.io/docs/astro/cli/troubleshoot-locally#ports-are-not-available-for-my-local-airflow-webserver) for solutions, such as stopping conflicting services or changing the default ports.

-----

## Deploy Your Project to Astronomer

For seamless deployment of your NASA EPO ETL pipeline to a hosted Astronomer environment, follow the instructions in the official Astronomer documentation:

  * [Deploying Code on Astro](https://www.astronomer.io/docs/astro/deploy-code/)

-----

## Contact

This project is maintained with the support of the Astronomer team. For bug reports, feature suggestions, or general inquiries about the Astronomer CLI and platform, please reach out to Astronomer Support.

-----