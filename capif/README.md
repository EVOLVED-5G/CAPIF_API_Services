# CAPIF

![Version: 0.0.1](https://img.shields.io/badge/Version-0.0.1-informational?style=for-the-badge)
![Type: application](https://img.shields.io/badge/Type-application-informational?style=for-the-badge) 
![AppVersion: 3.0](https://img.shields.io/badge/AppVersion-3.0-informational?style=for-the-badge) 

## Description

A CAPIF Helm chart for Kubernetes

## Usage
<fill out>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| apiInvocationLogs.apiInvocationLogs.image.repository | string | `"709233559969.dkr.ecr.eu-central-1.amazonaws.com/evolved5g:capif-services_api-invocation-logs_1"` | The docker image repository to use |
| apiInvocationLogs.apiInvocationLogs.image.tag | string | `""` | The docker image tag to use @default Chart version |
| apiInvocationLogs.apiInvocationLogs.resources.limits.cpu | string | `"100m"` |  |
| apiInvocationLogs.apiInvocationLogs.resources.limits.memory | string | `"128Mi"` |  |
| apiInvocationLogs.apiInvocationLogs.resources.requests.cpu | string | `"100m"` |  |
| apiInvocationLogs.apiInvocationLogs.resources.requests.memory | string | `"128Mi"` |  |
| apiInvocationLogs.ports[0].name | string | `"8080"` |  |
| apiInvocationLogs.ports[0].port | int | `8080` |  |
| apiInvocationLogs.ports[0].targetPort | int | `8080` |  |
| apiInvocationLogs.replicas | int | `1` |  |
| apiInvocationLogs.type | string | `"ClusterIP"` |  |
| apiInvokerManagement.apiInvokerManagement.image.repository | string | `"709233559969.dkr.ecr.eu-central-1.amazonaws.com/evolved5g:capif-services_api-invoker-management_1"` | The docker image repository to use |
| apiInvokerManagement.apiInvokerManagement.image.tag | string | `""` | The docker image tag to use @default Chart version |
| apiInvokerManagement.apiInvokerManagement.resources.limits.cpu | string | `"100m"` |  |
| apiInvokerManagement.apiInvokerManagement.resources.limits.memory | string | `"128Mi"` |  |
| apiInvokerManagement.apiInvokerManagement.resources.requests.cpu | string | `"100m"` |  |
| apiInvokerManagement.apiInvokerManagement.resources.requests.memory | string | `"128Mi"` |  |
| apiInvokerManagement.ports[0].name | string | `"8080"` |  |
| apiInvokerManagement.ports[0].port | int | `8080` |  |
| apiInvokerManagement.ports[0].targetPort | int | `8080` |  |
| apiInvokerManagement.replicas | int | `1` |  |
| apiInvokerManagement.type | string | `"ClusterIP"` |  |
| apiProviderManagement.apiProviderManagement.image.repository | string | `"709233559969.dkr.ecr.eu-central-1.amazonaws.com/evolved5g:capif-services_api-provider-management_1"` | The docker image repository to use |
| apiProviderManagement.apiProviderManagement.image.tag | string | `""` | The docker image tag to use @default Chart version |
| apiProviderManagement.apiProviderManagement.resources.limits.cpu | string | `"100m"` |  |
| apiProviderManagement.apiProviderManagement.resources.limits.memory | string | `"128Mi"` |  |
| apiProviderManagement.apiProviderManagement.resources.requests.cpu | string | `"100m"` |  |
| apiProviderManagement.apiProviderManagement.resources.requests.memory | string | `"128Mi"` |  |
| apiProviderManagement.ports[0].name | string | `"8080"` |  |
| apiProviderManagement.ports[0].port | int | `8080` |  |
| apiProviderManagement.ports[0].targetPort | int | `8080` |  |
| apiProviderManagement.replicas | int | `1` |  |
| apiProviderManagement.type | string | `"ClusterIP"` |  |
| capifEvents.capifEvents.image.repository | string | `"709233559969.dkr.ecr.eu-central-1.amazonaws.com/evolved5g:capif-services_capif-events_1"` | The docker image repository to use |
| capifEvents.capifEvents.image.tag | string | `""` | The docker image tag to use @default Chart version |
| capifEvents.capifEvents.resources.limits.cpu | string | `"100m"` |  |
| capifEvents.capifEvents.resources.limits.memory | string | `"128Mi"` |  |
| capifEvents.capifEvents.resources.requests.cpu | string | `"100m"` |  |
| capifEvents.capifEvents.resources.requests.memory | string | `"128Mi"` |  |
| capifEvents.ports[0].name | string | `"8080"` |  |
| capifEvents.ports[0].port | int | `8080` |  |
| capifEvents.ports[0].targetPort | int | `8080` |  |
| capifEvents.replicas | int | `1` |  |
| capifEvents.type | string | `"ClusterIP"` |  |
| capifRoutingInfo.capifRoutingInfo.image.repository | string | `"709233559969.dkr.ecr.eu-central-1.amazonaws.com/evolved5g:capif-services_capif-routing-info_1"` | The docker image repository to use |
| capifRoutingInfo.capifRoutingInfo.image.tag | string | `""` | The docker image tag to use @default Chart version |
| capifRoutingInfo.capifRoutingInfo.resources.limits.cpu | string | `"100m"` |  |
| capifRoutingInfo.capifRoutingInfo.resources.limits.memory | string | `"128Mi"` |  |
| capifRoutingInfo.capifRoutingInfo.resources.requests.cpu | string | `"100m"` |  |
| capifRoutingInfo.capifRoutingInfo.resources.requests.memory | string | `"128Mi"` |  |
| capifRoutingInfo.ports[0].name | string | `"8080"` |  |
| capifRoutingInfo.ports[0].port | int | `8080` |  |
| capifRoutingInfo.ports[0].targetPort | int | `8080` |  |
| capifRoutingInfo.replicas | int | `1` |  |
| capifRoutingInfo.type | string | `"ClusterIP"` |  |
| capifSecurity.capifSecurity.image.repository | string | `"709233559969.dkr.ecr.eu-central-1.amazonaws.com/evolved5g:capif-services_capif-security_1"` | The docker image repository to use |
| capifSecurity.capifSecurity.image.tag | string | `""` | The docker image tag to use @default Chart version |
| capifSecurity.capifSecurity.resources.limits.cpu | string | `"100m"` |  |
| capifSecurity.capifSecurity.resources.limits.memory | string | `"128Mi"` |  |
| capifSecurity.capifSecurity.resources.requests.cpu | string | `"100m"` |  |
| capifSecurity.capifSecurity.resources.requests.memory | string | `"128Mi"` |  |
| capifSecurity.ports[0].name | string | `"8080"` |  |
| capifSecurity.ports[0].port | int | `8080` |  |
| capifSecurity.ports[0].targetPort | int | `8080` |  |
| capifSecurity.replicas | int | `1` |  |
| capifSecurity.type | string | `"ClusterIP"` |  |
| easyRsa.easyRsa.image.repository | string | `"709233559969.dkr.ecr.eu-central-1.amazonaws.com/evolved5g:capif-services_easy-rsa_1"` | The docker image repository to use |
| easyRsa.easyRsa.image.tag | string | `""` | The docker image tag to use @default Chart version |
| easyRsa.easyRsa.resources.limits.cpu | string | `"100m"` |  |
| easyRsa.easyRsa.resources.limits.memory | string | `"128Mi"` |  |
| easyRsa.easyRsa.resources.requests.cpu | string | `"100m"` |  |
| easyRsa.easyRsa.resources.requests.memory | string | `"128Mi"` |  |
| easyRsa.ports[0].name | string | `"8080"` |  |
| easyRsa.ports[0].port | int | `8080` |  |
| easyRsa.ports[0].targetPort | int | `8080` |  |
| easyRsa.replicas | int | `1` |  |
| easyRsa.type | string | `"ClusterIP"` |  |
| env | string | `"kubernetes-athens"` | The Environment variable. It accepts: 'kuberentes-athens', 'kuberentes-uma', 'openshift' |
| ingress_ip | object | `{"athens":"10.161.1.117","uma":"x.x.x.x"}` | If env: 'kuberentes-athens' or env: 'kuberentes-uma', use the Ip address dude for the kubernetes to your Ingress Controller ej: kubectl -n NAMESPACE_CAPIF get ing  |
| jwtauth.jwtauth.image.repository | string | `"709233559969.dkr.ecr.eu-central-1.amazonaws.com/evolved5g:capif-services_jwtauth_1"` | The docker image repository to use |
| jwtauth.jwtauth.image.tag | string | `""` | The docker image tag to use @default Chart version |
| jwtauth.jwtauth.resources.limits.cpu | string | `"100m"` |  |
| jwtauth.jwtauth.resources.limits.memory | string | `"128Mi"` |  |
| jwtauth.jwtauth.resources.requests.cpu | string | `"100m"` |  |
| jwtauth.jwtauth.resources.requests.memory | string | `"128Mi"` |  |
| jwtauth.ports[0].name | string | `"8080"` |  |
| jwtauth.ports[0].port | int | `8080` |  |
| jwtauth.ports[0].targetPort | int | `8080` |  |
| jwtauth.replicas | int | `1` |  |
| jwtauth.type | string | `"ClusterIP"` |  |
| kubernetesClusterDomain | string | `"cluster.local"` |  |
| logs.logs.image.repository | string | `"709233559969.dkr.ecr.eu-central-1.amazonaws.com/evolved5g:capif-services_logs_1"` | The docker image repository to use |
| logs.logs.image.tag | string | `""` | The docker image tag to use @default Chart version |
| logs.logs.resources.limits.cpu | string | `"100m"` |  |
| logs.logs.resources.limits.memory | string | `"128Mi"` |  |
| logs.logs.resources.requests.cpu | string | `"100m"` |  |
| logs.logs.resources.requests.memory | string | `"128Mi"` |  |
| logs.ports[0].name | string | `"8080"` |  |
| logs.ports[0].port | int | `8080` |  |
| logs.ports[0].targetPort | int | `8080` |  |
| logs.replicas | int | `1` |  |
| logs.type | string | `"ClusterIP"` |  |
| mongo.mongo.env.mongoInitdbRootPassword | string | `"example"` |  |
| mongo.mongo.env.mongoInitdbRootUsername | string | `"root"` |  |
| mongo.mongo.image.repository | string | `"709233559969.dkr.ecr.eu-central-1.amazonaws.com/evolved5g:capif-services_mongo_1"` | The docker image repository to use |
| mongo.mongo.image.tag | string | `""` | The docker image tag to use @default Chart version |
| mongo.mongo.resources | object | `{}` |  |
| mongo.ports[0].name | string | `"27017"` |  |
| mongo.ports[0].port | int | `27017` |  |
| mongo.ports[0].targetPort | int | `27017` |  |
| mongo.replicas | int | `1` |  |
| mongo.type | string | `"ClusterIP"` |  |
| mongoExpress.mongoExpress.env.meConfigMongodbAdminpassword | string | `"example"` |  |
| mongoExpress.mongoExpress.env.meConfigMongodbAdminusername | string | `"root"` |  |
| mongoExpress.mongoExpress.env.meConfigMongodbUrl | string | `"mongodb://root:example@mongo:27017/"` |  |
| mongoExpress.mongoExpress.image.repository | string | `"709233559969.dkr.ecr.eu-central-1.amazonaws.com/evolved5g:capif-services_mongo-express_1"` | The docker image repository to use |
| mongoExpress.mongoExpress.image.tag | string | `""` | The docker image tag to use @default Chart version |
| mongoExpress.mongoExpress.resources.limits.cpu | string | `"100m"` |  |
| mongoExpress.mongoExpress.resources.limits.memory | string | `"128Mi"` |  |
| mongoExpress.mongoExpress.resources.requests.cpu | string | `"100m"` |  |
| mongoExpress.mongoExpress.resources.requests.memory | string | `"128Mi"` |  |
| mongoExpress.ports[0].name | string | `"8082"` |  |
| mongoExpress.ports[0].port | int | `8082` |  |
| mongoExpress.ports[0].targetPort | int | `8081` |  |
| mongoExpress.replicas | int | `1` |  |
| mongoExpress.type | string | `"ClusterIP"` |  |
| nginx.nginx.env.capifHostname | string | `"my-capif.evolved-5g.eu"` | Ingress's host to Capif |
| nginx.nginx.image.repository | string | `"709233559969.dkr.ecr.eu-central-1.amazonaws.com/evolved5g:capif-services_nginx_1"` | The docker image repository to use |
| nginx.nginx.image.tag | string | `""` | The docker image tag to use @default Chart version |
| nginx.nginx.resources.limits.cpu | string | `"100m"` |  |
| nginx.nginx.resources.limits.memory | string | `"128Mi"` |  |
| nginx.nginx.resources.requests.cpu | string | `"100m"` |  |
| nginx.nginx.resources.requests.memory | string | `"128Mi"` |  |
| nginx.ports[0].name | string | `"8080"` |  |
| nginx.ports[0].port | int | `8080` |  |
| nginx.ports[0].targetPort | int | `8080` |  |
| nginx.ports[1].name | string | `"443"` |  |
| nginx.ports[1].port | int | `443` |  |
| nginx.ports[1].targetPort | int | `443` |  |
| nginx.replicas | int | `1` |  |
| nginx.type | string | `"ClusterIP"` |  |
| publishedApis.ports[0].name | string | `"8080"` |  |
| publishedApis.ports[0].port | int | `8080` |  |
| publishedApis.ports[0].targetPort | int | `8080` |  |
| publishedApis.publishedApis.image.repository | string | `"709233559969.dkr.ecr.eu-central-1.amazonaws.com/evolved5g:capif-services_published-apis_1"` | The docker image repository to use |
| publishedApis.publishedApis.image.tag | string | `""` | The docker image tag to use @default Chart version |
| publishedApis.publishedApis.resources.limits.cpu | string | `"100m"` |  |
| publishedApis.publishedApis.resources.limits.memory | string | `"128Mi"` |  |
| publishedApis.publishedApis.resources.requests.cpu | string | `"100m"` |  |
| publishedApis.publishedApis.resources.requests.memory | string | `"128Mi"` |  |
| publishedApis.replicas | int | `1` |  |
| publishedApis.type | string | `"ClusterIP"` |  |
| redis.ports[0].name | string | `"6379"` |  |
| redis.ports[0].port | int | `6379` |  |
| redis.ports[0].targetPort | int | `6379` |  |
| redis.redis.env.redisReplicationMode | string | `"master"` |  |
| redis.redis.image.repository | string | `"709233559969.dkr.ecr.eu-central-1.amazonaws.com/evolved5g:capif-services_redis_1"` | The docker image repository to use |
| redis.redis.image.tag | string | `""` | The docker image tag to use @default Chart version |
| redis.redis.resources.limits.cpu | string | `"100m"` |  |
| redis.redis.resources.limits.memory | string | `"128Mi"` |  |
| redis.redis.resources.requests.cpu | string | `"100m"` |  |
| redis.redis.resources.requests.memory | string | `"128Mi"` |  |
| redis.replicas | int | `1` |  |
| redis.type | string | `"ClusterIP"` |  |
| serviceApis.ports[0].name | string | `"8080"` |  |
| serviceApis.ports[0].port | int | `8080` |  |
| serviceApis.ports[0].targetPort | int | `8080` |  |
| serviceApis.replicas | int | `1` |  |
| serviceApis.serviceApis.image.repository | string | `"709233559969.dkr.ecr.eu-central-1.amazonaws.com/evolved5g:capif-services_service-apis_1"` | The docker image repository to use |
| serviceApis.serviceApis.image.tag | string | `""` | The docker image tag to use @default Chart version |
| serviceApis.serviceApis.resources.limits.cpu | string | `"100m"` |  |
| serviceApis.serviceApis.resources.limits.memory | string | `"128Mi"` |  |
| serviceApis.serviceApis.resources.requests.cpu | string | `"100m"` |  |
| serviceApis.serviceApis.resources.requests.memory | string | `"128Mi"` |  |
| serviceApis.type | string | `"ClusterIP"` |  |






