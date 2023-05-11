String forceDockerCleanBuild(String options) {
    return (options && options == 'True') ? '--no-cache' : ' '
}

String dockerVersion(String options) {
    return (options) ? options : 'latest'
}

pipeline {
    agent { node { label 'evol5-slave' } }
    options {
        disableConcurrentBuilds()
        ansiColor('xterm')
    }
    parameters {
        string(name: 'BRANCH_NAME', defaultValue: 'develop', description: 'Deployment git branch name')
        choice(name: 'FORCE_DOCKER_CLEAN_BUILD', choices: ['False', 'True'], description: 'Force Docker Clean Build. Default use cached images (False)')
        string(name: 'ROBOT_DOCKER_IMAGE_VERSION', defaultValue: '4.0', description: 'Robot Docker image version')
        booleanParam(name: 'GENERATE_ROBOT_DOCKER_IMAGE', defaultValue: false, description: 'Check if robot docker image should be generated')
    }
    environment {
        BRANCH_NAME = "${params.BRANCH_NAME}"
        CACHE = forceDockerCleanBuild("${params.FORCE_DOCKER_CLEAN_BUILD}")
        ROBOT_VERSION = dockerVersion("${params.ROBOT_DOCKER_IMAGE_VERSION}")
        GENERATE_ROBOT = "${params.GENERATE_ROBOT_DOCKER_IMAGE}"
        ROBOT_IMAGE_NAME="dockerhub.hi.inet/5ghacking/evolved-robot-test-image"
    }
    stages {
        stage ('Generate Evolved Robot Docker tool') {
            when {
                expression { GENERATE_ROBOT == 'true' }
            }
            steps {
                dir ("${WORKSPACE}/tools/robot") {
                    withCredentials([usernamePassword(
                    credentialsId: 'docker_pull_cred',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                   )]) {
                        sh '''
                        docker login --username ${USER} --password ${PASS} dockerhub.hi.inet
                        docker build ${CACHE} . -t ${ROBOT_IMAGE_NAME}:${ROBOT_VERSION}
                        docker push ${ROBOT_IMAGE_NAME}:${ROBOT_VERSION}
                      '''
                   }
                }
            }
        }
    }
    post {
        always {
            echo 'tools built'
            echo ' clean dockerhub credentials'
            sh 'rm -f ${HOME}/.docker/config.json'
        }
    }
}
