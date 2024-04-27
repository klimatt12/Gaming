terraform {
  required_providers {
    datadog = {
      source = "DataDog/datadog"
    }
  }
}

# Configure the Datadog provider
provider "datadog" {
  api_key = <ADD LATER>
  app_key = <ADD LATER>
  api_url = "https://us5.datadoghq.com/"
}