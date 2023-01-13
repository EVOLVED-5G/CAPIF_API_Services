/*
NTH: Create library with helper methods
*/
String netappName(String url) {
    String url2 = url?:'';
    String var = url2.substring(url2.lastIndexOf("/") + 1);
    return var ;
}

pipeline {
    agent { node {label 'evol5-slave2'}  }
    options {
        timeout(time: 10, unit: 'MINUTES')
        retry(2)
    }

    parameters {
        string(name: 'GIT_CAPIF_URL', defaultValue: 'https://github.com/EVOLVED-5G/CAPIF_API_Services', description: 'URL of the Github Repository')
    }

    environment {
        SCANNERHOME = tool 'Sonar Scanner 5';
        NETAPP_NAME = netappName("${params.GIT_CAPIF_URL}").toLowerCase()
        SQ_TOKEN=credentials('SONARQUBE_TOKEN')
    }

    stages {
        stage('Get the code!') {
            options {
                    timeout(time: 10, unit: 'MINUTES')
                    retry(2)
                }
            steps {
                dir ("${WORKSPACE}/") {
                    sh '''
                    mkdir $NETAPP_NAME
                    cd $NETAPP_NAME
                    git clone --single-branch --branch $CHANGE_BRANCH https://github.com/EVOLVED-5G/CAPIF_API_Services .
                    '''
                }
           }
        }

        stage('Get CAPIF Services') {
            steps {
                dir ("${WORKSPACE}/${NETAPP_NAME}/services/") {
                    script{
                        def list = sh(returnStdout: true, script: "ls -d */ | sed 's#/##'").trim().split('\n')
                        list.each{ a->
                            println "Analyze this CAPIF repo=${a}"
                        }
                    }
                }
            }
        }
            
        stage('Analyze') {
            steps {
                dir ("${WORKSPACE}/${NETAPP_NAME}/services/") {
                    script{
                        def list = sh(returnStdout: true, script: "ls -d */ | sed 's#/##'").trim().split('\n')
                            list.each { array ->
                                if(array=="nginx"){
                                    return
                                }
                                if(array=="mosquitto"){
                                    return
                                }
                                if(array=="mosquitto"){
                                    return
                                }
                                stage ("Analyze this CAPIF repo ${array}") {
                                    script {
                                        dir("${WORKSPACE}/${NETAPP_NAME}/.scannerwork"){
                                        withSonarQubeEnv('Evol5-SonarQube') {
                                        sh '''#! /bin/bash
                                        name=$(echo '''+array+''')
                                        
                                        echo $name
                                        ${SCANNERHOME}/bin/sonar-scanner -X \
                                            -Dsonar.projectKey=${NETAPP_NAME}-${CHANGE_BRANCH}-$name \
                                            -Dsonar.projectBaseDir="${WORKSPACE}/${NETAPP_NAME}/" \
                                            -Dsonar.sources=${WORKSPACE}/${NETAPP_NAME}/services/$name \
                                            -Dsonar.host.url=https://sq.mobilesandbox.cloud:9000 \
                                            -Dsonar.login=$SQ_TOKEN \
                                            -Dsonar.projectName=${NETAPP_NAME}-${CHANGE_BRANCH}-$name \
                                            -Dsonar.language=python \
                                            -Dsonar.sourceEncoding=UTF-8
                                    '''
                                        }
                                    }
                                }
                            }
                            // stage("Quality gate ${array}") {
                            //     script {
                            //         def tries = 0
                            //         def sonarResultStatus = "PENDING"
                            //         while ((sonarResultStatus == "PENDING" || sonarResultStatus == "IN_PROGRESS") && tries++ < 15) {
                            //             try {
                            //                 timeout(time: 5, unit: 'SECONDS') {
                            //                     sonarResult = waitForQualityGate abortPipeline: false
                            //                     sonarResultStatus = sonarResult.status
                            //                 }
                            //             } catch(ex) {
                            //                 echo "Waiting for 'SonarQube' report to finish. Attempt: ${tries}"
                            //             }
                            //         }
                            //         if (sonarResultStatus != 'OK') {
                            //             error "Quality gate failure for SonarQube: ${sonarResultStatus}"
                            //         }
                            //     }
                            // }
                        }
                    }
                }
            }
        }
    }
    post {
        cleanup{
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
