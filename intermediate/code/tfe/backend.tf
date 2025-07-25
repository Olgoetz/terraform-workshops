terraform {
  cloud {                   
    # `cloud` is mutually exclusive with `backend` 
    organization = "AXA-Group-Operations"
    workspaces {
      name = "oliver-sbx-dev"
    }
    hostname = "tfe.axa-cloud.com"
  }
}
