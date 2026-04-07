pipeline {
    agent any
    environment {
        VENV_DIR = 'venv'
    }
    stages {

        stage('Cloning GitHub Repository to jenkins') {
            steps {
                script {
                    echo 'Cloning GitHub Repository to jenkins............'
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'github-token',
                            url: 'https://github.com/0ksaalfaz007-lang/Ml-ops.git'
                        ]]
                    )
                }
            }
        }

        stage('Setting up our Virtual Environment and Installing dependancies'){
            steps{
                script{
                    echo 'Setting up our Virtual Environment and Installing dependancies............'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

    }                                 // ← CLOSE stages
}