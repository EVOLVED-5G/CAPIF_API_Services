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
        string(name: 'AWS_DEFAULT_REGION', defaultValue: 'eu-central-1', description: 'AWS region')
        string(name: 'OPENSHIFT_URL', defaultValue: 'https://openshift-epg.hi.inet:443', description: 'openshift url')
        string(name: 'NGINX_HOSTNAME', defaultValue: 'nginx-evolved5g.apps-dev.hi.inet', description: 'nginx hostname')
        string(name: 'MONGO_EXPRESS_HOSTNAME', defaultValue: 'mongo-express-evolved5g.apps-dev.hi.inet', description: 'mongo-express hostname')
    }
    environment {
        // This is to work around a jenkins bug on the first build of a multi-branch job
        // https://issues.jenkins-ci.org/browse/JENKINS-40574 - it is marked resolved but the last comment says it doesn't work for declaritive pipelines
        BRANCH_NAME = "${params.BRANCH_NAME}"
        AWS_DEFAULT_REGION = "${params.AWS_DEFAULT_REGION}"
        OPENSHIFT_URL= "${params.OPENSHIFT_URL}"
        NGINX_HOSTNAME= "${params.NGINX_HOSTNAME}"
        MONGO_EXPRESS_HOSTNAME= "${params.MONGO_EXPRESS_HOSTNAME}"
    }
    stages {
        stage('Login openshift') {
            steps {
                withCredentials([string(credentialsId: '18e7aeb8-5552-4cbb-bf66-2402ca6772de', variable: 'TOKEN')]) {
                    dir ("${env.WORKSPACE}/iac/terraform/") {
                        sh '''
                            export KUBECONFIG="./kubeconfig"
                            oc login --insecure-skip-tls-verify --token=$TOKEN $OPENSHIFT_URL
                        '''
                        readFile('kubeconfig')
                    }
                }

            }
        }
        stage ('Deploy app in kubernetes') {
            options {
                retry(2)
            }
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: '328ab84a-aefc-41c1-aca2-1dfae5b150d2', accessKeyVariable: 'AWS_ACCESS_KEY_ID', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    dir ("${env.WORKSPACE}/iac/terraform/") {
                        sh '''
                            terraform init
                            terraform validate
                            terraform plan -out deployment.tfplan
                            terraform apply --auto-approve -lock-timeout=15m deployment.tfplan
                        '''
                    }
                }
            }
        }
        stage ('Expose nginx') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    sh 'oc expose service nginx --hostname=$NGINX_HOSTNAME'
                }   
            }
        }
        stage ('Expose mongo-express') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                    sh 'oc expose service mongo-express --hostname=$MONGO_EXPRESS_HOSTNAME'
                }   
            }
        }
    }
}
