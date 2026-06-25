terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

data "docker_network" "cicd" {
  name = "cicd-network"
}

resource "docker_image" "linkpulse" {
  name         = "linkpulse-api:${var.image_tag}"
  keep_locally = true
}

resource "docker_container" "linkpulse_staging" {
  name  = var.container_name
  image = docker_image.linkpulse.image_id

  restart = "unless-stopped"

  networks_advanced {
    name = data.docker_network.cicd.name
  }

  ports {
    internal = 8000
    external = var.app_port
  }

  env = [
    "ENV=staging",
    "DB_PATH=/data/linkpulse.db",
    "BASE_URL=http://localhost:${var.app_port}"
  ]

  volumes {
    host_path      = var.data_path
    container_path = "/data"
  }

  healthcheck {
    test         = ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"]
    interval     = "30s"
    timeout      = "10s"
    retries      = 3
    start_period = "10s"
  }
}
