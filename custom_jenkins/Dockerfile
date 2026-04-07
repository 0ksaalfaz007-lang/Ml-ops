FROM jenkins/jenkins:lts

USER root

# -------------------------------
# Install base dependencies + Python
# -------------------------------
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg \
        lsb-release \
        openssl \
        python3 \
        python3-venv \
        python3-pip && \
    update-ca-certificates && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# -------------------------------
# Install Docker (Docker-in-Docker support)
# -------------------------------
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | \
    gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
    https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
    > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y \
        docker-ce \
        docker-ce-cli \
        containerd.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# -------------------------------
# Install Google Cloud SDK (gcloud)
# -------------------------------
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
    gpg --dearmor -o /etc/apt/keyrings/gcloud.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/gcloud.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
    > /etc/apt/sources.list.d/google-cloud-sdk.list && \
    apt-get update -y && \
    apt-get install -y google-cloud-sdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# -------------------------------
# Add Jenkins user to Docker group
# -------------------------------
RUN groupadd -f docker && usermod -aG docker jenkins

# -------------------------------
# Install Jenkins plugins
# -------------------------------
RUN jenkins-plugin-cli --plugins \
    git \
    workflow-aggregator \
    pipeline-stage-view \
    credentials-binding \
    docker-workflow

# -------------------------------
# Switch back to Jenkins user
# -------------------------------
USER jenkins

EXPOSE 8080 50000