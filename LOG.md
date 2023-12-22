# 2023-11-22

- I watched the video about how to become a DE, it was well made and brief, and I noticed I should maybe improve my SQL knowledge.. the main points were similar to what we were talking about in our first meeting with Filip 
- I've created the private repo as Filip requested and decided to really write every detail of what I am doing along the way
- doing a zhs setup ...

- finally I got the oh-my-zsh] theme 'half-life-fpop'

- Rancher Desktop is installed (allow max 4 GB memory and 2 CPUs, disable Kubernetes, use container engine moby, allow sudo access)
- I've cloned the repo
-  run a venv 
- I have added the docker-compose.yml from the airflow link
- AirFlow is up and running on the port http://localhost:8080/
- Trying to create initial infrastructure in Google Cloud
- I have Create a Service Accoun 
- Generated a JSON Key for the Service Account and saved it 
- I need to make a billing acount in order to creat a GCS bucket and it'n not accepting my visa card.
- created a AWS S3 bucket to start with for now wheil I'm waiting for the Google billing acount to be created
- I have created a new folder for data and added two files : babak1.csv and babak2.json containing two rows 

- I have created a new user in the IAM named Javid912 I have created the Access keys.
- I have started the first dag in the dag0001.py but still checking the airflow doc
- The GCP billing account finaly worked, now I can get the free terial.
- create a GCS bucket called avalin-bucket with location EU-berlin in the new GCP project.
- uplouded the two files : babak1.csv and babak2.json.
- in the IAM Console (UI) add read permission (`roles/storage.objectViewer`) for the service account of the bucket.
- reviewing the DAG documentation and structure 
- I was working on the redi project(bookstore data warehause) meanwhile and there is still things to be done to make it presentable.
- I have successfully created and mounted a dag to the Airflow container and triggered it.
- using the DAG to sence the files in the GCP bucket ... 
- I have updated the docker-compose.yaml to set the GOOGLE_APPLICATION_CREDENTIALS environment variable to point to the GCP key file inside the Airflow container.
- after updadating the dag0002.py finaly it is working.. 

