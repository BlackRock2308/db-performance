# Hadoop/Spark Cluster Performance Project
This project allows you to set up and run a Hadoop/Spark cluster using Docker, as well as execute Spark jobs on the cluster. The project includes an environment.yaml file to create a virtual environment with Conda.

## Prerequisites

- Docker <br>
- Docker Compose <br>
- Conda (Anaconda or Miniconda)

## Project Setup
1. Clone the Repository <br>
- `clone https://gitlab.com/smbaye/db-perf.git` <br>
- cd db-perf
2. Create Conda Environment
Use the provided environnement.yaml file to create and activate the virtual environment:<br>
- `Create conda environment`
- `conda env create -f environnement.yaml`

## Activate the environment
`conda activate db-perf`
3. Setup Hadoop/Spark Cluster with Docker
Navigate to the infrastructure directory and use Docker Compose to set up the cluster: <br>
- `cd infra`
-  `docker-compose up -d`
4. Verify Cluster Status <br>
Check that all containers are running:
- `docker-compose ps` <br>
5. Submit Spark Job
Use the provided spark-submit.sh script to run a job on the cluster:
Make script executable  <br> : `chmod +x spark-submit.sh`

## Submit the Spark job
 run `./spark-submit.sh`
Troubleshooting

Ensure Docker is running before starting docker-compose
Check container logs if services fail to start:
`docker-compose logs [service-name]`


### Notes

The conda environment db-perf contains all necessary dependencies
Adjust Docker Compose configuration in infra/docker-compose.yml if needed
Modify spark-submit.sh to specify your specific Spark job requirements.
You also need to modify a little bit in your docker-compose.yaml especially certain paths there.
Check carrefully before running the code.