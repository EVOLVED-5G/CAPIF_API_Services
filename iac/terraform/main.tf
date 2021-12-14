resource "kubernetes_pod" "dummy_netapp" {
  metadata {
    name      = "dummy-netapp"
    namespace = "evolved5g"
    labels = {
      app = "dummynetapp"
    }
  }

  spec {
    container {
      image = "dockerhub.hi.inet/evolved-5g/dummy-netapp:latest"
      name  = "dummy-netapp"
    }
  }
}

resource "kubernetes_service" "dummy_netapp_service" {
  metadata {
    name      = "dummy-netapp-service"
    namespace = "evolved5g"
  }
  spec {
    selector = {
      app = kubernetes_pod.dummy_netapp.metadata.0.labels.app
    }
    port {
      port        = 8080
      target_port = 8080
    }
  }
}
