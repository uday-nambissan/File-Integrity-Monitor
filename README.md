# File Integrity Monitor (FIM)

The **File Integrity Monitor (FIM)** is a security tool that detects unauthorized modifications to critical files by calculating and periodically comparing cryptographic hashes (SHA-256). This tool monitors specified file paths, logging any changes and, if configured, sending an alert email for detected modifications. The FIM is designed to run in a Docker container with NGINX, allowing for isolated, containerized security monitoring. Ideal for maintaining the integrity of essential server configuration files and improving file system security.
