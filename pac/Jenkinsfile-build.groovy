pipeline {
    agent { node {label 'evol5-slave'}  }
    parameters {
        string(name: 'VERSION', defaultValue: '1.0', description: '')
    }

    environment {
        VERSION="${params.VERSION}"
        AWS_DEFAULT_REGION = 'eu-central-1'
    }

    stages {
        stage('Build') {
            steps {
                dir ("${env.WORKSPACE}") {
                    sh '''
                    docker-compose build --pull
                    '''
                }
            }
        }

        stage('Publish') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker_pull_cred', usernameVariable: 'ARTIFACTORY_USER', passwordVariable: 'ARTIFACTORY_CREDENTIALS')]) {
                    dir ("${env.WORKSPACE}") {
                        sh '''
                        docker login --username ${ARTIFACTORY_USER} --password "${ARTIFACTORY_CREDENTIALS}" dockerhub.hi.inet
                        docker-compose push
                        '''
                    }
                }
            }
        }
    }
}