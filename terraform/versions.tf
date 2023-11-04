provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Owner       = var.owner
      Project     = var.environment
      Provisioner = "Terraform"
    }
  }
}

terraform {
  required_version = "~> 1.6.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}