terraform {
  backend "s3" {
    bucket = "bsc.sandbox.terraform.state"
    key    = "streaming_ml/terraform.tfstate"
    region = "us-east-2"
  }
}