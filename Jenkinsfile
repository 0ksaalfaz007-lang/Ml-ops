pipeline {
    agent any
    environment {
        VENV_DIR
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
         stage('Setting up virtual environment and installing dependencies') {
             steps {
                 script {
                     echo 'Setting up virtual environment and installing dependencies'
                     sh '''
                        python3 -m venv venv
                        source venv/bin/activate
                        pip install -r requirements.txt
                        pip install -e .
                     '''
                 }
             }

        }
    }                                 // ← CLOSE stages
}