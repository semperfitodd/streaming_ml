variable "aws_region" {
  description = "AWS Region to deploy resources"
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name we are building"
  default     = "streaming_ml"
}

variable "owner" {
  description = "Owner of the resources"
  default     = "Jake and Todd"
}

variable "search_keywords" {
  description = "Keywords to search for from twitter"
  default     = "green energy, alternative fuels"
}

variable "tags" {
  description = "Default tags for this environment"
  default     = {}
}