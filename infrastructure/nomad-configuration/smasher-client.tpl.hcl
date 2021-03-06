# This is a Nomad Configuration file for an instance dedicated to
# running smasher jobs.

log_level = "WARN"

# Setup data dir
data_dir = "/tmp/nomad_client1"

# Enable the client
client {
    enabled = true
    servers = ["${nomad_lead_server_ip}:4647"]

    meta {
      is_smasher = "true"
    }
}

consul {
  auto_advertise      = false
  server_auto_join    = false
  client_auto_join    = false
}

# Disabled because it slows Nomad down. We dream it will be fixed one day!
# telemetry {
#   publish_allocation_metrics = true
#   publish_node_metrics       = true
#   statsd_address = "${nomad_lead_server_ip}:8125"
# }
