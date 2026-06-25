# infra/variables.tf
variable "image_tag" {
  description = "Tag de l'image Docker LinkPulse a deployer (SHA court Git)"
  type        = string
  default     = "latest"
}
# Port 8080 reserve a Jenkins, 9000 a SonarQube -- staging sur 8001
variable "app_port" {
  description = "Port hote expose pour LinkPulse en staging"
  type        = number
  default     = 8001
}
variable "container_name" {
  description = "Nom du conteneur applicatif de staging"
  type        = string
  default     = "linkpulse-staging"
}
variable "data_path" {
  description = "Chemin hote pour la persistance de la base SQLite"
  type        = string
  default     = "/home/labadmin/linkpulse-data"
}
variable "registry" {
  description = "Registry Docker (ex: ghcr.io/votre-pseudo) - reserve a un usage futur"
  type        = string
  default     = "ghcr.io/dspitech"
}
