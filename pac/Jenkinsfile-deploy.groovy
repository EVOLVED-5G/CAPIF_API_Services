def getContext(deployment) {
    String var = deployment
    if ('openshift'.equals(var)) {
        return 'evol5-nef/api-ocp-epg-hi-inet:6443/system:serviceaccount:evol5-nef:deployer'
    } else {
        return 'kubernetes-admin@kubernetes'
    }
}

def getPath(deployment) {
    String var = deployment
    if ('openshift'.equals(var)) {
        return 'kubeconfig'
    } else {
        return '~/kubeconfig'
    }
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

pipeline {
    agent { node { label 'evol5-openshift' }  }
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
        choice(name: 'DEPLOYMENT', choices: ['kubernetes-athens', 'kubernetes-uma', 'kubernetes-cosmote', 'openshift'], description: 'Environment where the CAPIF will be deployed')
    }
    environment {
        // This is to work around a jenkins bug on the first build of a multi-branch job
        // https://issues.jenkins-ci.org/browse/JENKINS-40574 - it is marked resolved but the last comment says it doesn't work for declaritive pipelines
        BRANCH_NAME = "${params.BRANCH_NAME}"
        AWS_DEFAULT_REGION = "${params.AWS_DEFAULT_REGION}"
        OPENSHIFT_URL = "${params.OPENSHIFT_URL}"
        DEPLOYMENT = "${params.DEPLOYMENT}"
        CONFIG_PATH = getPath("${params.DEPLOYMENT}")
        CONFIG_CONTEXT = getContext("${params.DEPLOYMENT}")
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
                withKubeConfig([credentialsId: 'kubeconfig-os-evol5-capif']) {
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
        }
        stage ('Expose routes and service publicly') {
            steps {
                dir ("${env.WORKSPACE}/iac/terraform/openshift4") {
                    sh '''
                        oc expose service/mongo-express --hostname=mongo-express.apps.ocp-epg.hi.inet
                        oc expose service/nginx --name=ca-root --hostname=${NGINX_HOSTNAME} --path=/ca-root
                        oc expose service/nginx --name=cert-data --hostname=${NGINX_HOSTNAME} --path=/certdata
                        oc expose service/nginx --name=gettoken --hostname=${NGINX_HOSTNAME} --path=/gettoken
                        oc expose service/nginx --name=register --hostname=${NGINX_HOSTNAME} --path=/register
                        oc expose service/nginx --name=sign-csr --hostname=${NGINX_HOSTNAME} --path=/sign-csr
                        oc expose service/nginx --name=test-data --hostname=${NGINX_HOSTNAME} --path=/testdata
                        oc create route passthrough nginx --hostname=${NGINX_HOSTNAME} --service=nginx --port=nginx-https --insecure-policy=None
                        oc patch route nginx -p '{"metadata":{"annotations":{"kubernetes.io/tls-acme":"true"}}}'
                    '''
                }
            }
        }
        stage ('Launch robot tests') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    dir ("${env.WORKSPACE}/") {
                        sh '''
                    sleep 1m
                '''
                    }
                    build job: 'Launch_Robot_Tests',
                        parameters: [
                            string(name: 'BRANCH_NAME', value: "${BRANCH_NAME}"),
                            booleanParam(name: 'RUN_LOCAL_CAPIF', value: false),
                            string(name: 'CAPIF_HOSTNAME', value: "${NGINX_HOSTNAME}")
                        ]
                }
            }
        }
    }
}
