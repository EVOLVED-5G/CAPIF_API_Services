// ################################################
// ## External Imports
// ################################################

import java.time.LocalDateTime
import groovy.json.JsonSlurper

// ################################################
// ## JSON Funtions
// ################################################
// Parse JSON to a map. @param json Json string to parse with name / value properties. @return A map of properties

def parseJsonToMap(String json) {
    final slurper = new JsonSlurper()
    return slurper.parseText(json)
}

// ################################################
// ## Robot Funtions
// ################################################
// Parse JSON to a map. @param json Json string to parse with name / value properties. @return A map of properties

String setRobotOptionsValue(String options) {
    return (options && options != '') ? options : ' '
}

String robotDockerVersion(String options) {
    return (options) ? options : 'latest'
}

String robotTestSelection(String tests, String customTest) {
    if (tests == 'CUSTOM') {
        return (customTest) ? '--include ' + customTest : ' '
    }
    return tests == 'NONE' ? ' ' : '--include ' + test_plan[tests]
}

test_plan = [
    '8-Core': '8',
    '8.1-Basic Features & Functional': '8.1',
    '8.1.1-SCTP Link': '8.1.1',
    '8.1.2-SCTP Reset initiated by eNB': '8.1.2',
    '8.1.3-S1 Setup': '8.1.3',
    '8.1.4-UE EPC attachment': '8.1.4',
    '8.1.5-UE initiated EPC detachment': '8.1.5',
    '8.1.6-EPC initiated EPC detachment': '8.1.6',
    'CUSTOM': 'CUSTOM'
    ]

// ################################################
// ## Pipeline
// ################################################

def awsCredentials = [[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: '047a2523-0a76-477f-a24d-17efc60b6a82', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]

pipeline {
    agent { node { label 'prod-5gnet-slave-02' }  }
    options {
        disableConcurrentBuilds()
        withCredentials(awsCredentials)
        buildDiscarder(logRotator(daysToKeepStr: '14', numToKeepStr: '30', artifactDaysToKeepStr: '14', artifactNumToKeepStr: '30'))
        ansiColor('xterm')
    }
    parameters {
        string(name: 'BRANCH_NAME', defaultValue: 'develop', description: 'Deployment git branch name')
        string(name: 'SPIRENT_SERVER', defaultValue: 'http://10.95.208.85:8080', description: 'Spirent Server')
        string(name: 'SPIRENT_AUTH_TOKEN_NAME', defaultValue: 'tip_spirent_auth', description: 'Token Name of the Auth to use the Spirent Server')

        string(name: 'ROBOT_DOCKER_IMAGE_VERSION', defaultValue: '1.0', description: 'Robot Docker image version')
        string(name: 'ROBOT_COMMON_LIBRARY', defaultValue: 'develop', description: 'Common Robot library branch to use')
        string(name: 'ROBOT_TEST_LIBRARY', defaultValue: 'develop', description: 'Common Robot library branch to use')
        string(name: 'ROBOT_TEST_OPTIONS', defaultValue: '', description: 'Options to set in test to robot testing. --variable <key>:<value>, --include <tag>, --exclude <tag>')
        choice(name: 'TESTS', choices: test_plan.keySet() as ArrayList, description: 'Select option to run. Prefix')
        string(name: 'CUSTOM_TEST', defaultValue: '', description: 'If CUSTOM is set in TESTS, here you can add test tag')
    }
    environment {
        GIT_BRANCH = "${params.BRANCH_NAME}"
        SPIRENT_SERVER = "${params.SPIRENT_SERVER}"

        SPIRENT_AUTH_TOKEN_NAME = "${params.SPIRENT_AUTH_TOKEN_NAME}"

        ROBOT_TESTS_DIRECTORY = "${WORKSPACE}/tests"
        ROBOT_COMMON_DIRECTORY = "${WORKSPACE}/common"
        ROBOT_RESULTS_DIRECTORY = "${WORKSPACE}/results"
        CUSTOM_TEST = "${params.CUSTOM_TEST}"
        ROBOT_COMMON_LIBRARY = "${params.ROBOT_COMMON_LIBRARY}"
        ROBOT_TEST_LIBRARY = "${params.ROBOT_TEST_LIBRARY}"
        ROBOT_TEST_OPTIONS = setRobotOptionsValue("${params.ROBOT_TEST_OPTIONS}")
        ROBOT_TESTS_INCLUDE = robotTestSelection("${params.TESTS}", "${params.CUSTOM_TEST}")

        ROBOT_VERSION = robotDockerVersion("${params.ROBOT_DOCKER_IMAGE_VERSION}")
        ROBOT_IMAGE_NAME="dockerhub.hi.inet/5ghacking/5gnow-robot-test-image"
    }
    stages {
        stage ('Prepare testing tools') {
            steps {
                dir ("${env.WORKSPACE}") {
                    withCredentials([usernamePassword(
                       credentialsId: 'docker_pull_cred',
                       usernameVariable: 'USER',
                       passwordVariable: 'PASS'
                   )]) {
                        sh '''
                            docker login --username ${USER} --password ${PASS} dockerhub.hi.inet
                           '''
                   }
                }
                dir ("${env.WORKSPACE}") {
                    withCredentials([usernamePassword(
                       credentialsId: 'github_cred',
                       usernameVariable: 'GIT_USER',
                       passwordVariable: 'GIT_PASS'
                   )]) {
                        sh 'git clone --branch ${ROBOT_COMMON_LIBRARY} https://${GIT_USER}:${GIT_PASS}@github.com/Telefonica/robot_test_automation_common.git common'
                        sh 'git clone --branch ${ROBOT_TEST_LIBRARY} https://${GIT_USER}:${GIT_PASS}@github.com/Telefonica/5gnow-robotframework.git tests'
                        sh "mkdir ${ROBOT_RESULTS_DIRECTORY}"
                   }
                }
            }
        }

        stage('Launch tests') {
            steps {
                withCredentials([string(credentialsId: "${SPIRENT_AUTH_TOKEN_NAME}", variable: 'SPIRENT_AUTH')]) {
                    dir ("${env.WORKSPACE}") {
                        sh """
                            docker pull ${ROBOT_IMAGE_NAME}:${ROBOT_VERSION}
                            docker run -t \
                                --rm \
                                -v ${ROBOT_COMMON_DIRECTORY}:/opt/robot-tests/common \
                                -v ${ROBOT_TESTS_DIRECTORY}:/opt/robot-tests/tests \
                                -v ${ROBOT_RESULTS_DIRECTORY}:/opt/robot-tests/results \
                                ${ROBOT_IMAGE_NAME}:${ROBOT_VERSION} \
                                --variable SPIRENT_SERVER:${SPIRENT_SERVER} \
                                --variable SPIRENT_AUTH:${SPIRENT_AUTH} \
                                ${ROBOT_TESTS_INCLUDE} ${ROBOT_TEST_OPTIONS}
                        """
                    }
                }
            }
        }

    }
    post {
        always {
            script {
                /* Manually clean up /keys due to permissions failure */
                echo 'Robot test executed'
                echo ' clean dockerhub credentials'
                sh 'rm -f ${HOME}/.docker/config.json'
            }

            publishHTML([allowMissing: true,
                    alwaysLinkToLastBuild: false,
                    keepAll: true,
                    reportDir: 'results',
                    reportFiles: 'report.html',
                    reportName: 'Robot Framework Tests Report',
                    reportTitles: '',
                    includes:'**/*'])
            junit allowEmptyResults: true, testResults: 'results/xunit.xml'

            script {
                dir ("${env.WORKSPACE}") {
                    sh 'sudo rm -rf tests/'
                    sh 'sudo rm -rf common/'
                }
            }
        }
        cleanup {
            /* clean up our workspace */
            deleteDir()
            /* clean up tmp directory */
            dir("${env.workspace}@tmp") {
                deleteDir()
            }
            /* clean up script directory */
            dir("${env.workspace}@script") {
                deleteDir()
            }
        }
    }
}
