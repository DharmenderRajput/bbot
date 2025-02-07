from bbot.modules.bucket_aws import bucket_aws


class bucket_azure(bucket_aws):
    watched_events = ["DNS_NAME", "STORAGE_BUCKET"]
    produced_events = ["STORAGE_BUCKET", "FINDING"]
    flags = ["active", "safe", "cloud-enum"]
    meta = {"description": "Check for Azure storage blobs related to target"}
    options = {"max_threads": 10, "permutations": False}
    options_desc = {
        "max_threads": "Maximum number of threads for HTTP requests",
        "permutations": "Whether to try permutations",
    }

    cloud_helper_name = "azure"
    delimiters = ("", "-")
    base_domains = ["blob.core.windows.net"]
    # Dirbusting is required to know whether a bucket is public
    supports_open_check = False

    def check_bucket_exists(self, bucket_name, url):
        response = self.helpers.request(url)
        status_code = getattr(response, "status_code", 0)
        existent_bucket = status_code != 0
        return (existent_bucket, set())

    def check_bucket_open(self, bucket_name, url):
        response = self.helpers.request(url)
        tags = self.gen_tags_exists(response)
        status_code = getattr(response, "status_code", 404)
        content = getattr(response, "text", "")
        open_bucket = status_code == 200 and "Contents" in content
        msg = ""
        if open_bucket:
            msg = "Open storage bucket"
        return (msg, tags)
