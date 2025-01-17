variable "credentials" {
  description = "My Credentials"
  default     = "./keys/gcloud-creds.json"
  #ex: if you have a directory where this file is called keys with your service account json file
  #saved there as gcloud-creds.json you could use default = "./keys/gcloud-creds.json"
}

variable "project" {
  description = "Project"
  default     = "project-example-340611"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "terraform-demo-terra-bucket-rohitpatra"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}
