# infra/monitoring.tf

resource "docker_image" "prometheus" {
  name         = "prom/prometheus:latest"
  keep_locally = true
}

resource "docker_container" "prometheus" {
  name    = "prometheus"
  image   = docker_image.prometheus.image_id
  restart = "unless-stopped"

  networks_advanced {
    name = data.docker_network.cicd.name
  }

  ports {
    internal = 9090
    external = 9090
  }

  volumes {
    host_path      = "/home/labadmin/linkpulse-api/monitoring/prometheus.yml"
    container_path = "/etc/prometheus/prometheus.yml"
    read_only      = true
  }

  volumes {
    host_path      = "/home/labadmin/linkpulse-api/monitoring/alerts.yml"
    container_path = "/etc/prometheus/alerts.yml"
    read_only      = true
  }

  command = [
    "--config.file=/etc/prometheus/prometheus.yml",
    "--storage.tsdb.retention.time=15d"
  ]

  depends_on = [docker_container.linkpulse_staging]
}

resource "docker_image" "grafana" {
  name         = "grafana/grafana:latest"
  keep_locally = true
}

resource "docker_container" "grafana" {
  name    = "grafana"
  image   = docker_image.grafana.image_id
  restart = "unless-stopped"

  networks_advanced {
    name = data.docker_network.cicd.name
  }

  ports {
    internal = 3000
    external = 3000
  }

  env = [
    "GF_SECURITY_ADMIN_PASSWORD=admin",
    "GF_PATHS_PROVISIONING=/etc/grafana/provisioning"
  ]

  volumes {
    host_path      = "/home/labadmin/linkpulse-api/monitoring/grafana/provisioning/datasources"
    container_path = "/etc/grafana/provisioning/datasources"
    read_only      = true
  }

  volumes {
    host_path      = "/home/labadmin/linkpulse-api/monitoring/grafana/provisioning/dashboards"
    container_path = "/etc/grafana/provisioning/dashboards"
    read_only      = true
  }

  volumes {
    host_path      = "/home/labadmin/linkpulse-api/monitoring/grafana/dashboards"
    container_path = "/var/lib/grafana/dashboards"
    read_only      = true
  }

  depends_on = [docker_container.prometheus]
}
