Code related to the machine learning client goes in this folder.

## Running the Machine Learning Client

To ensure that your machine learning client environment is correctly configured and running in a Docker container, follow these steps:

1. **Update Dependencies**

   In the `machine-learning-client` directory, update your lock file and install the dependencies:
   
   ```bash
   pipenv lock --clear
   pipenv install

2. **Build the Docker Image with the following command**
   docker build -t ml-client .

3.**Run the Docker Container Using**
docker run --rm ml-client

