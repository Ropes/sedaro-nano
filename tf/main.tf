provider "kubernetes" {
  config_path    = "~/.kube/config.minikube"
  config_context = "minikube"
}

resource "kubernetes_namespace" "sedaro" {
  metadata {
    name = "sedaro"
  }
}

resource "kubernetes_service_v1" "dask-scheduler" {
  metadata {
    name = "dask-scheduler"
    namespace = kubernetes_namespace.sedaro.metadata.0.name
  }
  spec {
    selector = {
      app = "dask-scheduler"
    }
    port {
      port        = 8786
      protocol    = "TCP"
    }
    port {
      port        = 8787
      protocol    = "TCP"
    }
  }
}

resource "kubernetes_deployment_v1" "dask-scheduler" {
  metadata {
    name = "dask-scheduler"
    labels = {
      name = "dask-scheduler"
    }
  }
  spec {
    replicas = 1
    selector = {
      match_labels = {
        app = "dask-scheduler"
      }
    }
    container {
      name = "scheduler"
      image = "ghcr.io/dask/dask:2023.8.1"
      port {
        name = "scheduler-api"
        port = 8786
        target_port = 8786
      }
      port {
        name = "scheduler-dashboard"
        port = 8787
        target_port = 8787
      }
      requests = {
        cpu    = "250m"
        memory = "50Mi"
      }
    }
    liveness_probe {
      http_get {
        path = "/status"
        port = 8786
      }

      initial_delay_seconds = 10
      period_seconds        = 3
    }
  }
}

