#############################################
# AEF SECURITY
#############################################
resource "kubernetes_pod" "aef_security" {
  metadata {
    name      = "aef-security"
    namespace = "evolved5g"
    labels = {
      app = "aef_security"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/aef/security_api:latest"
      name  = "aef-security"
    }
  }
}

resource "kubernetes_service" "aef_security_service" {
  metadata {
    name      = "aef-security-service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.aef_security.metadata.0.labels.app
    }
    port {
      port        = 8080
      target_port = 8080
    }
  }
}
#############################################
# API INVOKER MANAGEMENT
#############################################
resource "kubernetes_pod" "api_invoker_management" {
  metadata {
    name      = "api-invoker-management"
    namespace = "evolved5g"
    labels = {
      app = "api_invoker_management"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/capif/api_invoker_management_api:latest"
      name  = "api-invoker-management"
    }
  }
}

resource "kubernetes_service" "api_invoker_management_service" {
  metadata {
    name      = "api-invoker-management-service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.api_invoker_management.metadata.0.labels.app
    }
    port {
      port        = 8080
      target_port = 8080
    }
  }
}

#############################################
# API PROVIDER MANAGEMENT
#############################################
resource "kubernetes_pod" "api_provider_management" {
  metadata {
    name      = "api-provider-management"
    namespace = "evolved5g"
    labels = {
      app = "api_provider_management"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/capif/api_provider_management_api:latest"
      name  = "api-provider-management"
    }
  }
}

resource "kubernetes_service" "api_provider_management_service" {
  metadata {
    name      = "api-provider-management-service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.api_provider_management.metadata.0.labels.app
    }
    port {
      port        = 8080
      target_port = 8080
    }
  }
}

#############################################
# ACCESS CONTROL POLICY
#############################################
resource "kubernetes_pod" "access_control_policy" {
  metadata {
    name      = "access-control-policy"
    namespace = "evolved5g"
    labels = {
      app = "access_control_policy"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/capif/access_control_policy_api:latest"
      name  = "access-control-policy"
    }
  }
}

resource "kubernetes_service" "access_control_policy_service" {
  metadata {
    name      = "access-control-policy-service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.access_control_policy.metadata.0.labels.app
    }
    port {
      port        = 8080
      target_port = 8080
    }
  }
}

#############################################
# LOGS
#############################################
resource "kubernetes_pod" "logs" {
  metadata {
    name      = "logs"
    namespace = "evolved5g"
    labels = {
      app = "logs"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/capif/auditing_api:latest"
      name  = "logs"
    }
  }
}

resource "kubernetes_service" "logs_service" {
  metadata {
    name      = "logs-service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.logs.metadata.0.labels.app
    }
    port {
      port        = 8080
      target_port = 8080
    }
  }
}

#############################################
# DISCOVER SERVICE
#############################################
resource "kubernetes_pod" "discover_service" {
  metadata {
    name      = "discover-service"
    namespace = "evolved5g"
    labels = {
      app = "discover_service"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/capif/discover_service_api:latest"
      name  = "discover-service"
    }
  }
}

resource "kubernetes_service" "discover_service_service" {
  metadata {
    name      = "discover-service-service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.discover_service.metadata.0.labels.app
    }
    port {
      port        = 8080
      target_port = 8080
    }
  }
}

#############################################
# EVENTS
#############################################
resource "kubernetes_pod" "events" {
  metadata {
    name      = "events"
    namespace = "evolved5g"
    labels = {
      app = "events"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/capif/events_api:latest"
      name  = "events"
    }
  }
}

resource "kubernetes_service" "events_service" {
  metadata {
    name      = "events-service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.events.metadata.0.labels.app
    }
    port {
      port        = 8080
      target_port = 8080
    }
  }
}

#############################################
# API INVOCATION LOGS
#############################################
resource "kubernetes_pod" "api_invocation_logs" {
  metadata {
    name      = "api-invocation-logs"
    namespace = "evolved5g"
    labels = {
      app = "api_invocation_logs"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/capif/api_invocation_logs_api:latest"
      name  = "api-invocation-logs"
    }
  }
}

resource "kubernetes_service" "api_invocation_logs_service" {
  metadata {
    name      = "api-invocation-logs-service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.api_invocation_logs.metadata.0.labels.app
    }
    port {
      port        = 8080
      target_port = 8080
    }
  }
}

#############################################
# PUBLISH SERVICE
#############################################
resource "kubernetes_pod" "publish_service" {
  metadata {
    name      = "publish-service"
    namespace = "evolved5g"
    labels = {
      app = "publish_service"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/capif/publish_service_api:latest"
      name  = "publish-service"
    }
  }
}

resource "kubernetes_service" "publish_service_service" {
  metadata {
    name      = "publish-service-service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.publish_service.metadata.0.labels.app
    }
    port {
      port        = 8080
      target_port = 8080
    }
  }
}

#############################################
# ROUTING INFO
#############################################
resource "kubernetes_pod" "routing_info" {
  metadata {
    name      = "routing-info"
    namespace = "evolved5g"
    labels = {
      app = "routing_info"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/capif/routing_info_api:latest"
      name  = "routing-info"
    }
  }
}

resource "kubernetes_service" "routing_info_service" {
  metadata {
    name      = "routing-info-service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.routing_info.metadata.0.labels.app
    }
    port {
      port        = 8080
      target_port = 8080
    }
  }
}

#############################################
# SECURITY
#############################################
resource "kubernetes_pod" "security" {
  metadata {
    name      = "security"
    namespace = "evolved5g"
    labels = {
      app = "security"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/capif/security_api:latest"
      name  = "security"
    }
  }
}

resource "kubernetes_service" "security_service" {
  metadata {
    name      = "security-service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.security.metadata.0.labels.app
    }
    port {
      port        = 8080
      target_port = 8080
    }
  }
}

#############################################
# MONGO
#############################################
resource "kubernetes_pod" "mongo" {
  metadata {
    name      = "mongo"
    namespace = "evolved5g"
    labels = {
      app = "mongo"
    }
  }

  spec {
    container {
      image = "mongo:latest"
      name  = "mongo"

      env {
        name  = "MONGO_INITDB_ROOT_USERNAME"
        value = "root"
      }

      env {
        name  = "MONGO_INITDB_ROOT_PASSWORD"
        value = "example"
      }
    }
  }
}

resource "kubernetes_service" "mongo_service" {
  metadata {
    name      = "mongo-service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.mongo.metadata.0.labels.app
    }
    port {
      port        = 27017
      target_port = 27017
    }
  }
}

#############################################
# MONGO EXPRES
#############################################
resource "kubernetes_pod" "mongo-express" {
  metadata {
    name      = "mongo-express"
    namespace = "evolved5g"
    labels = {
      app = "mongo-express"
    }
  }

  spec {
    container {
      image = "mongo-express:latest"
      name  = "mongo-express"

      env {
        name  = "ME_CONFIG_MONGODB_ADMINUSERNAME"
        value = "root"
      }

      env {
        name  = "ME_CONFIG_MONGODB_ADMINPASSWORD"
        value = "example"
      }

      env {
        name  = "ME_CONFIG_MONGODB_URL"
        value = "mongodb://root:example@mongo:27017/"
      }
    }
  }

  depends_on = [
    kubernetes_service.mongo_service
  ]
}

resource "kubernetes_service" "mongo-express_service" {
  metadata {
    name      = "mongo-express-service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.mongo-express.metadata.0.labels.app
    }
    port {
      port        = 8081
      target_port = 8081
    }
  }
}

#############################################
# NGINX
#############################################
resource "kubernetes_pod" "nginx" {
  metadata {
    name      = "nginx"
    namespace = "evolved5g"
    labels = {
      app = "nginx"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/capif/nginx"
      name  = "nginx"
    }
  }

  depends_on = [
    kubernetes_service.aef_security_service,
    kubernetes_service.api_invoker_management_service,
    kubernetes_service.api_provider_management_service,
    kubernetes_service.access_control_policy_service,
    kubernetes_service.logs_service,
    kubernetes_service.events_service,
    kubernetes_service.api_invocation_logs_service,
    kubernetes_service.publish_service_service,
    kubernetes_service.routing_info_service,
    kubernetes_service.security_service
  ]
}

resource "kubernetes_service" "nginx_service" {
  metadata {
    name      = "nginx-service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.nginx.metadata.0.labels.app
    }
    port {
      port        = 8080
      target_port = 8080
    }
  }
}
