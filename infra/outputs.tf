# infra/outputs.tf
output "app_url" {
  description = "URL de LinkPulse en staging"
  value       = "http://localhost:${var.app_port}"
}
output "container_id" {
  description = "ID du conteneur applicatif de staging"
  value       = docker_container.linkpulse_staging.id
}
output "network_name" {
  description = "Nom du reseau Docker partage"
  value       = data.docker_network.cicd.name
}
