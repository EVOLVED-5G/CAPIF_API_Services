pipeline {
    agent { node {label 'evol5-slave'}  }
    options {
        disableConcurrentBuilds()
        timeout(time: 1, unit: 'HOURS')
        buildDiscarder(logRotator(daysToKeepStr: '14', numToKeepStr: '30', artifactDaysToKeepStr: '14', artifactNumToKeepStr: '30'))
        ansiColor('xterm')
    }
    parameters {
        string(name: 'BRANCH_NAME', defaultValue: 'develop', description: 'Deployment git branch name')
        string(name: 'VERSION', defaultValue: '1.0', description: '')
    }
    environment {
        // This is to work around a jenkins bug on the first build of a multi-branch job
        // https://issues.jenkins-ci.org/browse/JENKINS-40574 - it is marked resolved but the last comment says it doesn't work for declaritive pipelines
        BRANCH_NAME = "${params.BRANCH_NAME}"
        VERSION = "${params.VERSION}"
        CAPIF_SERVICES_DIRECTORY = "${WORKSPACE}/services"
    }
    stages {
        stage('Build') {
            steps {
                dir ("${env.CAPIF_SERVICES_DIRECTORY}") {
                    sh '''
                        docker-compose build --pull
                    '''
                }
            }
        }
        stage('Publish') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker_pull_cred', usernameVariable: 'ARTIFACTORY_USER', passwordVariable: 'ARTIFACTORY_CREDENTIALS')]) {
                    dir ("${env.CAPIF_SERVICES_DIRECTORY}") {
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