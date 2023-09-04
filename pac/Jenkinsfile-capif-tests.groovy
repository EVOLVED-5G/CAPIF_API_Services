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

def getAgent(deployment) {
    String var = deployment
    if ('openshift'.equals(var)) {
        return 'evol5-openshift'
    } else if ('kubernetes-athens'.equals(var)) {
        return 'evol5-athens'
    } else if ('kubernetes-cosmote'.equals(var)) {
        return 'evol5-cosmote'
    } else {
        return 'evol5-slave'
    }
}

test_plan = [
    'All Capif Services': 'all',
    'CAPIF Api Invoker Management': 'capif_api_invoker_management',
    'CAPIF Api Publish Service': 'capif_api_publish_service',
    'CAPIF Api Discover Service': 'capif_api_discover_service',
    'CAPIF Api Events': 'capif_api_events',
    'CAPIF Security Api': 'capif_security_api',
    'CUSTOM': 'CUSTOM'
    ]

// ################################################
// ## Pipeline
// ################################################

pipeline {
    agent { node { label getAgent("${params.DEPLOYMENT }") == 'any' ? '' : getAgent("${params.DEPLOYMENT }") } }
    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(daysToKeepStr: '14', numToKeepStr: '30', artifactDaysToKeepStr: '14', artifactNumToKeepStr: '30'))
        ansiColor('xterm')
        timeout(time: 60, unit: 'MINUTES')
        retry(1)
    }
    parameters {
        string(name: 'BRANCH_NAME', defaultValue: 'develop', description: 'Deployment git branch name')
        booleanParam(name: 'RUN_LOCAL_CAPIF', defaultValue: false, description: 'Run test on local deployment')
        string(name: 'CAPIF_HOSTNAME', defaultValue: 'capifcore', description:'Nginx to forward requests')
        string(name: 'CAPIF_PORT', defaultValue: '8080', description:'Port of capif')
        string(name: 'CAPIF_TLS_PORT', defaultValue: '443', description:'Port of TLS capif')
        choice(name: 'TESTS', choices: test_plan.keySet() as ArrayList, description: 'Select option to run. Prefix')
        string(name: 'CUSTOM_TEST', defaultValue: '', description: 'If CUSTOM is set in TESTS, here you can add test tag')
        string(name: 'ROBOT_DOCKER_IMAGE_VERSION', defaultValue: '4.0', description: 'Robot Docker image version')
        string(name: 'ROBOT_TEST_OPTIONS', defaultValue: '', description: 'Options to set in test to robot testing. --variable <key>:<value>, --include <tag>, --exclude <tag>')
        choice(name: 'DEPLOYMENT', choices: ['kubernetes-athens', 'kubernetes-uma', 'kubernetes-cosmote', 'openshift'], description: 'Environment where the CAPIF is tested')
    }
    environment {
        BRANCH_NAME = "${params.BRANCH_NAME}"
        CAPIF_SERVICES_DIRECTORY = "${WORKSPACE}/services"
        ROBOT_TESTS_DIRECTORY = "${WORKSPACE}/tests"
        ROBOT_RESULTS_DIRECTORY = "${WORKSPACE}/results"
        ROBOT_DOCKER_FILE_FOLDER = "${WORKSPACE}/tools/robot"
        CUSTOM_TEST = "${params.CUSTOM_TEST}"
        CAPIF_HOSTNAME = "${params.CAPIF_HOSTNAME}"
        CAPIF_PORT = "${params.CAPIF_PORT}"
        CAPIF_TLS_PORT = "${params.CAPIF_TLS_PORT}"
        ROBOT_TEST_OPTIONS = setRobotOptionsValue("${params.ROBOT_TEST_OPTIONS}")
        ROBOT_TESTS_INCLUDE = robotTestSelection("${params.TESTS}", "${params.CUSTOM_TEST}")
        ROBOT_VERSION = robotDockerVersion("${params.ROBOT_DOCKER_IMAGE_VERSION}")
        ROBOT_IMAGE_NAME = 'dockerhub.hi.inet/5ghacking/evolved-robot-test-image'
        RUN_LOCAL_CAPIF = "${params.RUN_LOCAL_CAPIF}"
        DEPLOYMENT = "${params.DEPLOYMENT}"
    }
    stages {
        stage('Prepare robot docker image tool') {
            options {
                retry(2)
            }

            steps {
                dir("${env.WORKSPACE}") {
                    withCredentials([usernamePassword(
                    credentialsId: 'docker_pull_cred',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {
                    script {
                        try {
                            sh '''
                            docker login --username ${USER} --password ${PASS} dockerhub.hi.inet
                            docker pull ${ROBOT_IMAGE_NAME}:${ROBOT_VERSION}
                            '''
                    } catch (Exception e) {
                                echo 'Robot Docker version is not currently uploaded to artifactory.'
                            }
                        }
                }
                }
            }
        }
        stage('CAPIF: Local Test') {
            when {
                allOf {
                    expression { RUN_LOCAL_CAPIF == 'true' }
                }
            }
            steps {
                dir("${CAPIF_SERVICES_DIRECTORY}") {
                        sh '''
                            bash ./run.sh ${CAPIF_HOSTNAME}
                           '''
                }
                dir("${CAPIF_SERVICES_DIRECTORY}") {
                        sh '''
                            bash ./check_services_are_running.sh
                           '''
                }
                steps {
                    dir("${env.WORKSPACE}") {
                        sh '''#!/bin/bash
                            echo "Executing tests in local"
                            docker images|grep -Eq '^'$ROBOT_IMAGE_NAME'[ ]+[ ]'$ROBOT_VERSION''
                            if [[ $? -ne 0 ]]; then
                                echo "Building Robot docker image."
                                cd ${ROBOT_DOCKER_FILE_FOLDER}
                                docker build  -t ${ROBOT_IMAGE_NAME}:${ROBOT_VERSION} .
                                cd ${WORKSPACE}
                            fi
                            mkdir -p ${ROBOT_RESULTS_DIRECTORY}
                            docker run --tty --rm --network="host" \
                                -v ${ROBOT_TESTS_DIRECTORY}:/opt/robot-tests/tests \
                                -v ${ROBOT_RESULTS_DIRECTORY}:/opt/robot-tests/results ${ROBOT_IMAGE_NAME}:${ROBOT_VERSION}  \
                                --variable CAPIF_HOSTNAME:${CAPIF_HOSTNAME} \
                                --variable CAPIF_HTTP_PORT:${CAPIF_PORT} \
                                --variable CAPIF_HTTPS_PORT:${CAPIF_TLS_PORT} \
                                ${ROBOT_TESTS_INCLUDE} ${ROBOT_TEST_OPTIONS}
                    '''
                    }
                }
            }
        }
        stage('CAPIF: Launch tests') {
            when {
                expression { RUN_LOCAL_CAPIF == 'false' }
            }
            steps {
                dir("${env.WORKSPACE}") {
                    sh '''#!/bin/bash
                            echo "Executing tests in ${DEPLOYMENT}"
                            docker images|grep -Eq '^'$ROBOT_IMAGE_NAME'[ ]+[ ]'$ROBOT_VERSION''
                            if [[ $? -ne 0 ]]; then
                                echo "Building Robot docker image."
                                cd ${ROBOT_DOCKER_FILE_FOLDER}
                                docker build  -t ${ROBOT_IMAGE_NAME}:${ROBOT_VERSION} .
                                cd ${WORKSPACE}
                            fi
                            mkdir -p ${ROBOT_RESULTS_DIRECTORY}
                            docker run --tty --rm --network="host" \
                                -v ${ROBOT_TESTS_DIRECTORY}:/opt/robot-tests/tests \
                                -v ${ROBOT_RESULTS_DIRECTORY}:/opt/robot-tests/results ${ROBOT_IMAGE_NAME}:${ROBOT_VERSION}  \
                                --variable CAPIF_HOSTNAME:${CAPIF_HOSTNAME} \
                                --variable CAPIF_HTTP_PORT:${CAPIF_PORT} \
                                --variable CAPIF_HTTPS_PORT:${CAPIF_TLS_PORT} \
                                ${ROBOT_TESTS_INCLUDE} ${ROBOT_TEST_OPTIONS}
                    '''
                }
            }
        }
    }
    post {
        always {
            script {
                dir("${env.CAPIF_SERVICES_DIRECTORY}") {
                    echo 'Shutdown all capif services'
                    sh 'sudo ./clean_capif_docker_services.sh'
                }
            }

            script {
                /* Manually clean up /keys due to permissions failure */
                echo 'Robot test executed'
                echo ' clean dockerhub credentials'
                sh 'sudo rm -f ${HOME}/.docker/config.json'
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
                dir("${env.WORKSPACE}") {
                    sh "sudo rm -rf ${env.ROBOT_TESTS_DIRECTORY}"
                    sh "sudo rm -rf ${env.CAPIF_SERVICES_DIRECTORY}"
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
