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
    'All Capif Services': 'all',
    'CAPIF Api Invoker Management': 'capif_api_invoker_management',
    'CAPIF Api Publish Management': 'capif_api_publish_service',
    'CAPIF Api Discover Service': 'capif_api_discover_service',
    'CUSTOM': 'CUSTOM'
    ]


String runCapifLocal(String nginxHost) {
    return nginxHost.matches('^(http|https)://localhost.*') ? 'true' : 'false'
}


// ################################################
// ## Pipeline
// ################################################

pipeline {
    agent { node { label 'evol5-slave' }  }
    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(daysToKeepStr: '14', numToKeepStr: '30', artifactDaysToKeepStr: '14', artifactNumToKeepStr: '30'))
        ansiColor('xterm')
    }
    parameters {
        choice(name: 'TESTS', choices: test_plan.keySet() as ArrayList, description: 'Select option to run. Prefix')
        string(name: 'CUSTOM_TEST', defaultValue: '', description: 'If CUSTOM is set in TESTS, here you can add test tag')
        string (name: 'NGINX_HOSTNAME', defaultValue: 'http://localhost:8080', description:'Nginx to forward requests')
        string(name: 'ROBOT_DOCKER_IMAGE_VERSION', defaultValue: '1.0', description: 'Robot Docker image version')
        string(name: 'ROBOT_COMMON_LIBRARY', defaultValue: 'develop', description: 'Common Robot library branch to use')
        string(name: 'CAPIF_SERVICES_BRANCH', defaultValue: 'develop', description: 'CAPIF Services Branch To Use')
        string(name: 'ROBOT_TEST_OPTIONS', defaultValue: '', description: 'Options to set in test to robot testing. --variable <key>:<value>, --include <tag>, --exclude <tag>')
    }
    environment {
        CAPIF_SERVICES_DIRECTORY = "${WORKSPACE}/capif"
        ROBOT_TESTS_DIRECTORY = "${CAPIF_SERVICES_DIRECTORY}/tests"
        ROBOT_COMMON_DIRECTORY = "${WORKSPACE}/common"
        ROBOT_RESULTS_DIRECTORY = "${WORKSPACE}/results"
        CUSTOM_TEST = "${params.CUSTOM_TEST}"
        ROBOT_COMMON_LIBRARY = "${params.ROBOT_COMMON_LIBRARY}"
        NGINX_HOSTNAME = "${params.NGINX_HOSTNAME}"
        CAPIF_SERVICES_BRANCH = "${params.CAPIF_SERVICES_BRANCH}"
        ROBOT_TEST_OPTIONS = setRobotOptionsValue("${params.ROBOT_TEST_OPTIONS}")
        ROBOT_TESTS_INCLUDE = robotTestSelection("${params.TESTS}", "${params.CUSTOM_TEST}")
        ROBOT_VERSION = robotDockerVersion("${params.ROBOT_DOCKER_IMAGE_VERSION}")
        ROBOT_IMAGE_NAME = 'dockerhub.hi.inet/5ghacking/evolved-robot-test-image'
        RUN_LOCAL_CAPIF = runCapifLocal("${params.NGINX_HOSTNAME}")
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
                        sh 'git clone --branch ${CAPIF_SERVICES_BRANCH} https://${GIT_USER}:${GIT_PASS}@github.com/EVOLVED-5G/CAPIF_API_Services.git capif'
                        sh "mkdir ${ROBOT_RESULTS_DIRECTORY}"
                   }
                }
            }
        }

        stage('Launch CAPIF Docker Compose') {
            when {
                expression { RUN_LOCAL_CAPIF == 'true' }
            }
            steps {
                dir ("${CAPIF_SERVICES_DIRECTORY}") {
                        sh '''
                            ./run.sh
                           '''
                }
                dir ("${CAPIF_SERVICES_DIRECTORY}") {
                        sh '''
                            ./check_services_are_running.sh
                           '''
                }
            }
        }

        stage('Launch tests') {
            steps {
                dir ("${env.WORKSPACE}") {
                    sh """
                        docker pull ${ROBOT_IMAGE_NAME}:${ROBOT_VERSION}
                        docker run -t \
                            --network="host" \
                            --rm \
                            -v ${ROBOT_COMMON_DIRECTORY}:/opt/robot-tests/common \
                            -v ${ROBOT_TESTS_DIRECTORY}:/opt/robot-tests/tests \
                            -v ${ROBOT_RESULTS_DIRECTORY}:/opt/robot-tests/results \
                            ${ROBOT_IMAGE_NAME}:${ROBOT_VERSION} \
                            --variable NGINX_HOSTNAME:${NGINX_HOSTNAME} \
                            ${ROBOT_TESTS_INCLUDE} ${ROBOT_TEST_OPTIONS}
                    """
                }
            }
        }
    }
    post {
        always {
            script {
                dir ("${CAPIF_SERVICES_DIRECTORY}") {
                    echo 'Shutdown all capif services'
                    sh 'sudo ./clean_capif_docker_services.sh'
                }
                dir ("${env.WORKSPACE}") {
                    echo 'Remove common robot directory'
                    sh 'sudo rm -rf common/'
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
                dir ("${env.WORKSPACE}") {
                    sh 'sudo rm -rf tests/'
                    sh 'sudo rm -rf capif/'
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
