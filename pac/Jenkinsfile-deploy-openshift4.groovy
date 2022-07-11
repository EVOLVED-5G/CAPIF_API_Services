pipeline {
    agent { node {label 'evol5-openshift'}  }
    options {
        disableConcurrentBuilds()
        timeout(time: 1, unit: 'HOURS')
        buildDiscarder(logRotator(daysToKeepStr: '14', numToKeepStr: '30', artifactDaysToKeepStr: '14', artifactNumToKeepStr: '30'))
        ansiColor('xterm')
    }
    parameters {
        string(name: 'BRANCH_NAME', defaultValue: 'develop', description: 'Deployment git branch name')
        string(name: 'AWS_DEFAULT_REGION', defaultValue: 'eu-central-1', description: 'AWS region')
        string(name: 'OPENSHIFT_URL', defaultValue: 'https://api.ocp-epg.hi.inet:6443', description: 'openshift url')
        string(name: 'NGINX_HOSTNAME', defaultValue: 'openshift.evolved-5g.eu', description: 'Nginx eposition route in OpenShift')
        choice(name: "DEPLOYMENT", choices: ["openshift", "kubernetes-athens", "kubernetes-uma"]) 

    }
    environment {
        // This is to work around a jenkins bug on the first build of a multi-branch job
        // https://issues.jenkins-ci.org/browse/JENKINS-40574 - it is marked resolved but the last comment says it doesn't work for declaritive pipelines
        BRANCH_NAME = "${params.BRANCH_NAME}"
        AWS_DEFAULT_REGION = "${params.AWS_DEFAULT_REGION}"
        OPENSHIFT_URL= "${params.OPENSHIFT_URL}"
    }
    stages {
        stage('Login openshift') {
            steps {
                withCredentials([string(credentialsId: 'token-os-capif', variable: 'TOKEN')]) {
                    dir ("${env.WORKSPACE}/iac/terraform/") {
                        sh '''
                            oc login --insecure-skip-tls-verify --token=$TOKEN $OPENSHIFT_URL
                        '''
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
                    dir ("${env.WORKSPACE}/iac/terraform/openshift4") {
                        sh '''
                            terraform init  -reconfigure                                             \
                                -backend-config="bucket=evolved5g-openshift-terraform-states"        \
                                -backend-config="key=capif"
                            terraform validate
                            terraform plan -var CAPIF_HOSTNAME=${NGINX_HOSTNAME}  -out deployment.tfplan
                            terraform apply --auto-approve -lock-timeout=15m deployment.tfplan
                        '''
                    }
                }
            }
        }
        stage ('Expose routes and service publicly') {
            steps {
                dir ("${env.WORKSPACE}/iac/terraform/openshift4") {
                    sh '''
                        oc expose service/nginx --hostname=${NGINX_HOSTNAME}
                        oc expose service/mongo-express --hostname=mongo-express.apps.ocp-epg.hi.inet
                        oc patch route nginx -p '{"metadata":{"annotations":{"kubernetes.io/tls-acme":"true"}}}'
                    '''
                }
            }
        }
        // stage ('Launch robot tests') {
        //     steps {
        //         catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
        //             build job: 'Launch_Robot_Tests',
        //                 parameters: [
        //                     string(name: 'BRANCH_NAME', value: "develop"),
        //                     string(name: 'CAPIF_HOSTNAME', value: "NGINX_HOSTNAME")
        //                 ]
        //         }
        //     }
        // }
    }
}
