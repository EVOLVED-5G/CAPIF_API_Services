pipeline {
    agent {label params.AGENT == "evol5-slave1" ? "" : params.AGENT }
   options {
        disableConcurrentBuilds()
        timeout(time: 1, unit: 'HOURS')
        buildDiscarder(logRotator(daysToKeepStr: '14', numToKeepStr: '30', artifactDaysToKeepStr: '14', artifactNumToKeepStr: '30'))
        ansiColor('xterm')
    }
    parameters {               
        string(name: 'BRANCH_NAME', defaultValue: 'develop', description: 'Deployment git branch name')
        string(name: 'VERSION', defaultValue: '1.0', description: '')
        choice(name: "AGENT", choices: ["evol5-slave", "evol5-athens"]) 
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
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'evolved5g-pull', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    dir ("${env.CAPIF_SERVICES_DIRECTORY}") {
                        sh '''
                            $(aws ecr get-login --no-include-email)
                            docker-compose push
                        '''
                    }
                }
            }
        }
    }
}