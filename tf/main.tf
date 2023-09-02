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
    namespace = "sedaro"
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

    template {
      spec {
        container {
          name = "scheduler"
          image = "ghcr.io/dask/dask:2023.8.1"
          port {
            name = "scheduler-api"
            container_port = 8786
            protocol = "TCP"
          }
          port {
            name = "scheduler-dashboard"
            container_port = 8787
            protocol = "TCP"
          }
        }
      }
    }
  }

}

