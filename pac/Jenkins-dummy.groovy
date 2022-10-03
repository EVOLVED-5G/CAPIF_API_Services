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
        NETAPP_NAME = netappName("${params.GIT_NETAPP_URL}").toLowerCase()
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
                    git clone --single-branch --branch $CHANGE_BRANCH $GIT_CAPIF_URL .
                    '''
                }
           }
        }
        //TODO: Create a project for each NETAPP
        stage('SonarQube Analysis and Wait for Quality Gate') {
            steps {
                withSonarQubeEnv('Evol5-SonarQube') {
                    sh '''
                        ${SCANNERHOME}/bin/sonar-scanner -X \
                            -Dsonar.projectKey=${NETAPP_NAME}-${CHANGE_BRANCH} \
                            -Dsonar.projectBaseDir="${WORKSPACE}/${NETAPP_NAME}/" \
                            -Dsonar.sources="${WORKSPACE}/${NETAPP_NAME}/services/" \
                            -Dsonar.host.url=http://195.235.92.134:9000 \
                            -Dsonar.login=$SQ_TOKEN \
                            -Dsonar.projectName=${NETAPP_NAME}-${CHANGE_BRANCH} \
                            -Dsonar.language=python \
                            -Dsonar.sourceEncoding=UTF-8
                    '''
                }
            }
        }
    }
    // post {
    //     cleanup{
    //         /* clean up our workspace */
    //         deleteDir()
    //         /* clean up tmp directory */
    //         dir("${env.workspace}@tmp") {
    //             deleteDir()
    //         }
    //         /* clean up script directory */
    //         dir("${env.workspace}@script") {
    //             deleteDir()
    //         }
    //     }
    // }
}
