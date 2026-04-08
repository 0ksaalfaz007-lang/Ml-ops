pipeline{
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "mlops-new-447207"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages{
        stage('Cloning Github repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-classic-token', url: 'https://github.com/0ksaalfaz007-lang/Ml-ops.git']])
                }
            }
        }

        stage('Setting up Virtual Environment'){
            steps{
                script{
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Building and Pushing Docker Image to GCR'){
            steps{
                script{
                    echo 'Building and Pushing Docker Image to GCR.............'
                    sh '''
                    export PATH=$PATH:${GCLOUD_PATH}
                    gcloud config set project ${GCP_PROJECT}
                    gcloud auth configure-docker --quiet
                    docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                    docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                    '''
                }
            }
        }
    }
}