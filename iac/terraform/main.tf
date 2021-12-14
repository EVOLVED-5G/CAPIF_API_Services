#############################################
# AEF SECURITY
#############################################
resource "kubernetes_pod" "aef_security" {
  metadata {
    name      = "aef_security"
    namespace = "evolved5g"
    labels = {
      app = "aef_security"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/aef/security_api:latest"
      name  = "aef_security"
    }
  }
}

resource "kubernetes_service" "aef_security_service" {
  metadata {
    name      = "aef_security_service"
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
    name      = "api_invoker_management"
    namespace = "evolved5g"
    labels = {
      app = "api_invoker_management"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/capif/api_invoker_management_api:latest"
      name  = "api_invoker_management"
    }
  }
}

resource "kubernetes_service" "api_invoker_management_service" {
  metadata {
    name      = "api_invoker_management_service"
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
    name      = "api_provider_management"
    namespace = "evolved5g"
    labels = {
      app = "api_provider_management"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/capif/api_provider_management_api:latest"
      name  = "api_provider_management"
    }
  }
}

resource "kubernetes_service" "api_provider_management_service" {
  metadata {
    name      = "api_provider_management_service"
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
    name      = "access_control_policy"
    namespace = "evolved5g"
    labels = {
      app = "access_control_policy"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/capif/access_control_policy_api:latest"
      name  = "access_control_policy"
    }
  }
}

resource "kubernetes_service" "access_control_policy_service" {
  metadata {
    name      = "access_control_policy_service"
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
      image = "dockerhub.hi.inet/evolved-5g/capif/logs_api:latest"
      name  = "logs"
    }
  }
}

resource "kubernetes_service" "logs_service" {
  metadata {
    name      = "logs_service"
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
    name      = "discover_service"
    namespace = "evolved5g"
    labels = {
      app = "discover_service"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/capif/discover_service_api:latest"
      name  = "discover_service"
    }
  }
}

resource "kubernetes_service" "discover_service_service" {
  metadata {
    name      = "discover_service_service"
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
    name      = "events_service"
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
    name      = "api_invocation_logs"
    namespace = "evolved5g"
    labels = {
      app = "api_invocation_logs"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/capif/api_invocation_logs_api:latest"
      name  = "api_invocation_logs"
    }
  }
}

resource "kubernetes_service" "api_invocation_logs_service" {
  metadata {
    name      = "api_invocation_logs_service"
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
    name      = "publish_service"
    namespace = "evolved5g"
    labels = {
      app = "publish_service"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/capif/publish_service_api:latest"
      name  = "publish_service"
    }
  }
}

resource "kubernetes_service" "publish_service_service" {
  metadata {
    name      = "publish_service_service"
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
    name      = "routing_info"
    namespace = "evolved5g"
    labels = {
      app = "routing_info"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/capif/routing_info_api:latest"
      name  = "routing_info"
    }
  }
}

resource "kubernetes_service" "routing_info_service" {
  metadata {
    name      = "routing_info_service"
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
    name      = "security_service"
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
# JWTAUTH
#############################################
resource "kubernetes_pod" "jwtauth" {
  metadata {
    name      = "jwtauth"
    namespace = "evolved5g"
    labels = {
      app = "jwtauth"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/jwtauth:latest"
      name  = "jwtauth"
    }
  }
}

resource "kubernetes_service" "jwtauth_service" {
  metadata {
    name      = "jwtauth_service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.jwtauth.metadata.0.labels.app
    }
    port {
      port        = 8080
      target_port = 8080
    }
  }
}
