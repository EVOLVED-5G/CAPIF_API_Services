#############################################
# AEF SECURITY
#############################################
resource "kubernetes_deployment" "aef_security" {
  metadata {
    name      = "aef-security"
    namespace = "evol5-capif"
    labels = {
      app = "aef-security"
    }
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "aef-security"
      }
    }
    template {
      metadata {
        labels = {
          app = "aef-security"
        }
      }
      spec {
        enable_service_links = false
        container {
          image = "dockerhub.hi.inet/evolved-5g/aef/security_api:latest"
          name  = "aef-security"
          resources {
            limits = {
              cpu    = "125m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "65m"
              memory = "50Mi"
            }
          }

        }
      }
    }
  }
}


resource "kubernetes_service" "aef_security_service" {
  metadata {
    name      = "aef-security"
    namespace = "evol5-capif"
  }
  spec {
    selector = {
      app = kubernetes_deployment.aef_security.spec.0.template.0.metadata[0].labels.app
    }
    port {
      port        = 8080
      target_port = 8080
    }
  }
}
#############################################
# API INVOKER MANAGEMENTinstan
#############################################
resource "kubernetes_deployment" "api_invoker_management" {
  metadata {
    name      = "api-invoker-management"
    namespace = "evol5-capif"
    labels = {
      app = "api-invoker-management"
    }
  }
  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "api-invoker-management"
      }
    }
    template {
      metadata {
        labels = {
          app = "api-invoker-management"
        }
      }
      spec {
        enable_service_links = false
        container {
          image = "dockerhub.hi.inet/evolved-5g/capif/api_invoker_management_api:latest"
          name  = "api-invoker-management"
          resources {
            limits = {
              cpu    = "125m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "65m"
              memory = "50Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "api_invoker_management_service" {
  metadata {
    name      = "api-invoker-management"
    namespace = "evol5-capif"
  }
  spec {
    selector = {
      app = kubernetes_deployment.api_invoker_management.spec.0.template.0.metadata[0].labels.app
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
resource "kubernetes_deployment" "api_provider_management" {
  metadata {
    name      = "api-provider-management"
    namespace = "evol5-capif"
    labels = {
      app = "api-provider-managemen"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "api-provider-managemen"
      }
    }
    template {
      metadata {
        labels = {
          app = "api-provider-managemen"
        }
      }
      spec {
        enable_service_links = false
        container {
          image = "dockerhub.hi.inet/evolved-5g/capif/api_provider_management_api:latest"
          name  = "api-provider-management"
          resources {
            limits = {
              cpu    = "125m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "65m"
              memory = "50Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "api_provider_management_service" {
  metadata {
    name      = "api-provider-management"
    namespace = "evol5-capif"
  }
  spec {
    selector = {
      app = kubernetes_deployment.api_provider_management.spec.0.template.0.metadata[0].labels.app
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
resource "kubernetes_deployment" "access_control_policy" {
  metadata {
    name      = "access-control-policy"
    namespace = "evol5-capif"
    labels = {
      app = "access-control-policy"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "access-control-policy"
      }
    }
    template {
      metadata {
        labels = {
          app = "access-control-policy"
        }
      }
      spec {
        enable_service_links = false
        container {
          image = "dockerhub.hi.inet/evolved-5g/capif/access_control_policy_api:latest"
          name  = "access-control-policy"
          resources {
            limits = {
              cpu    = "125m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "65m"
              memory = "50Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "access_control_policy_service" {
  metadata {
    name      = "access-control-policy"
    namespace = "evol5-capif"
  }
  spec {
    selector = {
      app = kubernetes_deployment.access_control_policy.spec.0.template.0.metadata[0].labels.app
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
resource "kubernetes_deployment" "logs" {
  metadata {
    name      = "logs"
    namespace = "evol5-capif"
    labels = {
      app = "logs"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "logs"
      }
    }
    template {
      metadata {
        labels = {
          app = "logs"
        }
      }
      spec {
        enable_service_links = false
        container {
          image = "dockerhub.hi.inet/evolved-5g/capif/auditing_api:latest"
          name  = "logs"
          resources {
            limits = {
              cpu    = "125m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "65m"
              memory = "50Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "logs_service" {
  metadata {
    name      = "logs"
    namespace = "evol5-capif"
  }
  spec {
    selector = {
      app = kubernetes_deployment.logs.spec.0.template.0.metadata[0].labels.app
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
resource "kubernetes_deployment" "discover_service" {
  metadata {
    name      = "service-apis"
    namespace = "evol5-capif"
    labels = {
      app = "service-apis"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "service-apis"
      }
    }
    template {
      metadata {
        labels = {
          app = "service-apis"
        }
      }
      spec {
        enable_service_links = false
        container {
          image = "dockerhub.hi.inet/evolved-5g/capif/discover_service_api:latest"
          name  = "service-apis"
          resources {
            limits = {
              cpu    = "125m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "65m"
              memory = "50Mi"
            }
          }

        }
      }
    }
  }
}

resource "kubernetes_service" "discover_service_service" {
  metadata {
    name      = "service-apis"
    namespace = "evol5-capif"
  }
  spec {
    selector = {
      app = kubernetes_deployment.discover_service.spec.0.template.0.metadata[0].labels.app
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
resource "kubernetes_deployment" "events" {
  metadata {
    name      = "capif-events"
    namespace = "evol5-capif"
    labels = {
      app = "capif-events"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "capif-events"
      }
    }
    template {
      metadata {
        labels = {
          app = "capif-events"
        }
      }
      spec {
        enable_service_links = false
        container {
          image = "dockerhub.hi.inet/evolved-5g/capif/events_api:latest"
          name  = "capif-events"
          resources {
            limits = {
              cpu    = "125m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "65m"
              memory = "50Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "events_service" {
  metadata {
    name      = "capif-events"
    namespace = "evol5-capif"
  }
  spec {
    selector = {
      app = kubernetes_deployment.events.spec.0.template.0.metadata[0].labels.app
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
resource "kubernetes_deployment" "api_invocation_logs" {
  metadata {
    name      = "api-invocation-logs"
    namespace = "evol5-capif"
    labels = {
      app = "api-invocation-logs"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "api-invocation-logs"
      }
    }
    template {
      metadata {
        labels = {
          app = "api-invocation-logs"
        }
      }
      spec {
        enable_service_links = false
        container {
          image = "dockerhub.hi.inet/evolved-5g/capif/api_invocation_logs_api:latest"
          name  = "api-invocation-logs"
          resources {
            limits = {
              cpu    = "125m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "65m"
              memory = "50Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "api_invocation_logs_service" {
  metadata {
    name      = "api-invocation-logs"
    namespace = "evol5-capif"
  }
  spec {
    selector = {
      app = kubernetes_deployment.api_invocation_logs.spec.0.template.0.metadata[0].labels.app
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
resource "kubernetes_deployment" "publish_service" {
  metadata {
    name      = "published-apis"
    namespace = "evol5-capif"
    labels = {
      app = "published-apis"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "published-apis"
      }
    }
    template {
      metadata {
        labels = {
          app = "published-apis"
        }
      }
      spec {
        enable_service_links = false
        container {
          image = "dockerhub.hi.inet/evolved-5g/capif/publish_service_api:latest"
          name  = "published-apis"
          resources {
            limits = {
              cpu    = "125m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "65m"
              memory = "50Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "publish_service_service" {
  metadata {
    name      = "published-apis"
    namespace = "evol5-capif"
  }
  spec {
    selector = {
      app = kubernetes_deployment.publish_service.spec.0.template.0.metadata[0].labels.app
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
resource "kubernetes_deployment" "routing_info" {
  metadata {
    name      = "capif-routing-info"
    namespace = "evol5-capif"
    labels = {
      app = "capif-routing-info"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "capif-routing-info"
      }
    }
    template {
      metadata {
        labels = {
          app = "capif-routing-info"
        }
      }
      spec {
        enable_service_links = false
        container {
          image = "dockerhub.hi.inet/evolved-5g/capif/routing_info_api:latest"
          name  = "capif-routing-info"
          resources {
            limits = {
              cpu    = "125m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "65m"
              memory = "50Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "routing_info_service" {
  metadata {
    name      = "capif-routing-info"
    namespace = "evol5-capif"
  }
  spec {
    selector = {
      app = kubernetes_deployment.routing_info.spec.0.template.0.metadata[0].labels.app
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
resource "kubernetes_deployment" "security" {
  metadata {
    name      = "capif-security"
    namespace = "evol5-capif"
    labels = {
      app = "capif-security"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "capif-security"
      }
    }
    template {
      metadata {
        labels = {
          app = "capif-security"
        }
      }
      spec {
        enable_service_links = false
        container {
          image = "dockerhub.hi.inet/evolved-5g/capif/security_api:latest"
          name  = "capif-security"
          resources {
            limits = {
              cpu    = "125m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "65m"
              memory = "50Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "security_service" {
  metadata {
    name      = "capif-security"
    namespace = "evol5-capif"
  }
  spec {
    selector = {
      app = kubernetes_deployment.security.spec.0.template.0.metadata[0].labels.app
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
resource "kubernetes_deployment" "jwtauth" {
  metadata {
    name      = "jwtauth"
    namespace = "evol5-capif"
    labels = {
      app = "jwtauth"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "jwtauth"
      }
    }
    template {
      metadata {
        labels = {
          app = "jwtauth"
        }
      }
      spec {
        enable_service_links = false
        container {
          image = "dockerhub.hi.inet/evolved-5g/jwtauth:latest"
          name  = "jwtauth"
          resources {
            limits = {
              cpu    = "125m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "65m"
              memory = "50Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "jwtauth" {
  metadata {
    name      = "jwtauth"
    namespace = "evol5-capif"
  }
  spec {
    selector = {
      app = kubernetes_deployment.jwtauth.spec.0.template.0.metadata[0].labels.app
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
resource "kubernetes_deployment" "mongo" {
  metadata {
    name      = "mongo"
    namespace = "evol5-capif"
    labels = {
      app = "mongo"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "mongo"
      }
    }
    template {
      metadata {
        labels = {
          app = "mongo"
        }
      }
      spec {
        enable_service_links = false
        container {
          image = "mongo:latest"
          name  = "mongo"
          resources {
            limits = {
              cpu    = "125m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "65m"
              memory = "50Mi"
            }
          }

          env {
            name  = "MONGO_INITDB_ROOT_USERNAME"
            value = "root"
          }

          env {
            name  = "MONGO_INITDB_ROOT_PASSWORD"
            value = "example"
          }

          volume_mount {
            mount_path = "/data/configdb"
            name       = "configdb"
          }

          volume_mount {
            mount_path = "/data/db"
            name       = "db"
          }
        }

        volume {
          name = "configdb"
          empty_dir {
          }
        }

        volume {
          name = "db"
          empty_dir {
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "mongo_service" {
  metadata {
    name      = "mongo"
    namespace = "evol5-capif"
  }
  spec {
    selector = {
      app = kubernetes_deployment.mongo.spec.0.template.0.metadata[0].labels.app
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
resource "kubernetes_deployment" "mongo-express" {
  metadata {
    name      = "mongo-express"
    namespace = "evol5-capif"
    labels = {
      app = "mongo-express"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "mongo-express"
      }
    }
    template {
      metadata {
        labels = {
          app = "mongo-express"
        }
      }
      spec {
        enable_service_links = false
        container {
          image = "mongo-express:latest"
          name  = "mongo-express"
          resources {
            limits = {
              cpu    = "125m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "65m"
              memory = "50Mi"
            }
          }

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
    }
  }
  depends_on = [
    kubernetes_deployment.mongo,
    kubernetes_service.mongo_service
  ]
}

resource "kubernetes_service" "mongo-express_service" {
  metadata {
    name      = "mongo-express"
    namespace = "evol5-capif"
  }
  spec {
    selector = {
      app = kubernetes_deployment.mongo-express.spec.0.template.0.metadata[0].labels.app
    }
    port {
      port        = 8081
      target_port = 8081
    }
  }
}

#############################################
# EASY RSA
#############################################
resource "kubernetes_deployment" "easy-rsa" {
  metadata {
    name      = "easy-rsa"
    namespace = "evol5-capif"
    labels = {
      app = "easy-rsa"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "easy-rsa"
      }
    }
    template {
      metadata {
        labels = {
          app = "easy-rsa"
        }
      }
      spec {
        enable_service_links = false
        container {
          image = "dockerhub.hi.inet/evolved-5g/easy-rsa:latest"
          name  = "easy-rsa"
          resources {
            limits = {
              cpu    = "125m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "65m"
              memory = "50Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "easy-rsa" {
  metadata {
    name      = "easy-rsa"
    namespace = "evol5-capif"
  }
  spec {
    selector = {
      app = kubernetes_deployment.easy-rsa.spec.0.template.0.metadata[0].labels.app
    }
    port {
      port        = 8080
      target_port = 8080
    }
  }
}




#############################################
# NGINX
#############################################
variable "CAPIF_HOSTNAME" {
  description = "Hostname of nginx capif deployed"
  type        = string
  default     = "openshift.evolved-5g.eu"
}
resource "kubernetes_deployment" "nginx" {
  metadata {
    name      = "nginx"
    namespace = "evol5-capif"
    labels = {
      app = "nginx"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "nginx"
      }
    }
    template {
      metadata {
        labels = {
          app = "nginx"
        }
      }
      spec {
        enable_service_links = false
        container {
          image = "dockerhub.hi.inet/evolved-5g/capif/nginx"
          name  = "nginx"
          resources {
            limits = {
              cpu    = "125m"
              memory = "256Mi"
            }
            requests = {
              cpu    = "65m"
              memory = "50Mi"
            }
          }
          env {
            name = "CAPIF_HOSTNAME"
            value = var.CAPIF_HOSTNAME
          }
        }
      }
    }
  }

  depends_on = [
    kubernetes_deployment.aef_security,
    kubernetes_deployment.api_invoker_management,
    kubernetes_deployment.api_provider_management,
    kubernetes_deployment.access_control_policy,
    kubernetes_deployment.logs,
    kubernetes_deployment.events,
    kubernetes_deployment.api_invocation_logs,
    kubernetes_deployment.publish_service,
    kubernetes_deployment.routing_info,
    kubernetes_deployment.security,
    kubernetes_service.aef_security_service,
    kubernetes_service.api_invoker_management_service,
    kubernetes_service.api_provider_management_service,
    kubernetes_service.access_control_policy_service,
    kubernetes_service.logs_service,
    kubernetes_service.events_service,
    kubernetes_service.api_invocation_logs_service,
    kubernetes_service.publish_service_service,
    kubernetes_service.routing_info_service,
    kubernetes_service.security_service,
    kubernetes_service.easy-rsa
  ]
}

resource "kubernetes_service" "nginx_service" {
  metadata {
    name      = "nginx"
    namespace = "evol5-capif"
  }
  spec {
    type = "LoadBalancer"

    selector = {
      app = kubernetes_deployment.nginx.spec.0.template.0.metadata[0].labels.app
    }
    port {
      name = "nginx-http"
      port        = 80
      target_port = 8080
    }

    port {
      name = "nginx-https"
      port        = 443
      target_port = 443
    }
  }
}

# resource "kubernetes_ingress" "nginx_ingress" {
#   metadata {
#     name      = "nginx-ingress5"
#     namespace = "evol5-capif"
#     annotations = {
#       "kubernetes.io/ingress.class"                    = "nginx-ingress"
#       "kubernetes.io/tls-acme"                         = "true"
#       "nginx.ingress.kubernetes.io/force-ssl-redirect" = "true"
#       "nginx.ingress.kubernetes.io/ssl-passthrough"    = "true"
#     }
#   }

#   spec {
#     rule {
#       host = "openshift.evolved-5g.eu"
#       http {
#         path {
#           path = "/"
#           backend {
#             service_name = kubernetes_service.nginx_service.spec.0.selector.app
#             service_port = 443
#           }
#         }
#       }
#     }
#   }
# }
