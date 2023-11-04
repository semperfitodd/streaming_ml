locals {
  domain = "brewsentry.com"

  environment = replace(var.environment, "_", "-")

  site_domain = "${local.environment}.${local.domain}"
}