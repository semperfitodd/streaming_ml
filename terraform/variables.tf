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

variable "tags" {
  description = "Default tags for this environment"
  default     = {}
}
