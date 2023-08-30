terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0.0"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config.minikube"
}

resource "kubernetes_namespace" "sedaro" {
  metadata {
    labels = {
      name = "sedaro"
    }

    name = "sedaro"
  }
}

