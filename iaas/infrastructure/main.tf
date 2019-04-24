provider "google" {
  project = ""
  region  = "asia-northeast1"
  zone    = "asia-northeast1-b"
}

variable "num_envs" {
  default = 1
}

variable "num_benchmarkers" {
  default = 1
}

variable "path_to_private_key" {
  default = ""
}

variable "path_to_private_cert" {
  default = ""
}

resource "google_compute_health_check" "internal-health-check" {
  count = "${var.num_envs}"
  name  = "${format("iaas-health-check-%02d", count.index+1)}"

  timeout_sec        = 1
  check_interval_sec = 5
  healthy_threshold  = 2

  http_health_check {
    port         = 80
    request_path = "/tasks"
  }
}

resource "google_compute_backend_service" "default" {
  count = "${var.num_envs}"
  name  = "${format("iaas-backend-%02d", count.index + 1)}"

  health_checks = ["${element(google_compute_health_check.internal-health-check.*.self_link, count.index)}"]

  backend = {
    group = "${element(google_compute_instance_group.default.*.self_link, count.index)}"
  }
}

resource "google_compute_url_map" "default" {
  count = "${var.num_envs}"
  name  = "${format("iaas-urlmap-%02d", count.index + 1)}"

  default_service = "${element(google_compute_backend_service.default.*.self_link, count.index)}"
}

resource "google_compute_target_https_proxy" "default" {
  count            = "${var.num_envs}"
  name             = "${format("iaas-proxy-%02d", count.index + 1)}"
  url_map          = "${element(google_compute_url_map.default.*.self_link, count.index)}"
  ssl_certificates = ["${google_compute_ssl_certificate.default.self_link}"]
}

resource "google_compute_global_forwarding_rule" "default" {
  count  = "${var.num_envs}"
  name   = "${format("iaas-default-forwarding-rule-%02d", count.index + 1)}"
  target = "${element(google_compute_target_https_proxy.default.*.self_link, count.index)}"

  port_range = "443"
}

resource "google_dns_record_set" "dns" {
  count        = "${var.num_envs}"
  name         = "${format("iaas%02d.example.com.", count.index +1)}"
  managed_zone = "example"
  type         = "A"
  ttl          = 300

  rrdatas = ["${element(google_compute_global_forwarding_rule.default.*.ip_address, count.index)}"]
}

resource "google_compute_ssl_certificate" "default" {
  name        = "hoge-cert"
  description = "ssl wildcard cert for hoge"

  private_key = "${file("${var.path_to_private_key}")}"
  certificate = "${file("${var.path_to_private_cert}")}"
}

resource "google_compute_instance" "benchmarker" {
  count        = "${var.num_benchmarkers}"
  name         = "${format("iaas-bench-%02d", count.index+1)}"
  machine_type = "n1-highcpu-4"
  zone         = "asia-northeast1-b"
  tags         = ["ssh-iaas"]

  boot_disk {
    initialize_params {
      image = ""
    }
  }

  service_account {
    email  = "INPUT_SERVICE_ACCOUNT_HERE"
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }

  allow_stopping_for_update = true

  scheduling {
    preemptible       = true
    automatic_restart = false
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral IP
    }
  }
}

resource "google_compute_instance" "todo" {
  count = "${var.num_envs}"

  name         = "${format("iaas-compute-%02d-1", count.index +1)}"
  machine_type = "n1-highcpu-2"
  zone         = "asia-northeast1-b"
  tags         = ["hoge"]

  boot_disk {
    initialize_params {
      image = "INPUT_APP_VM_IMAGE_HERE"
    }
  }

  service_account {
    email  = "INPUT_SERVICE_ACCOUNT_HERE"
    scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral IP
    }
  }
}

resource "google_compute_instance_group" "default" {
  count = "${var.num_envs}"
  name  = "${format("iaas-instance-group-%02d", count.index +1)}"

  zone      = "asia-northeast1-b"
  instances = ["${element(google_compute_instance.todo.*.self_link, count.index)}"]
}

# Used as queue for benchmarking request
resource "google_redis_instance" "cache" {
  name           = "iaas-queue"
  memory_size_gb = 1
}
