# Bucket to store website

resource "google_storage_bucket" "website" {
  provider = google
  name     = "example_website_by_rp"
  location = "US"
}

# Make new objects public
resource "google_storage_object_access_control" "public_rule" {
  provider = google
  object   = google_storage_bucket_object.static_site_src.name
  bucket   = google_storage_bucket.website.name
  role     = "READER"
  entity   = "allUsers"
}

# Upload index.html to bucket
resource "google_storage_bucket_object" "static_site_src" {
  provider = google
  name     = "index.html"
  source   = "../website/index.html"
  bucket   = google_storage_bucket.website.name
}
