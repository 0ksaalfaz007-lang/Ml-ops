FROM jenkins/jenkins:lts

USER root

# Install Docker + basic tools
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        ca-certificates curl gnupg2 lsb-release && \
    curl -fsSL --retry 3 https://download.docker.com/linux/debian/gpg | \
        gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
    https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN groupadd -f docker && usermod -aG docker jenkins
RUN mkdir -p /var/lib/docker && chown -R jenkins:jenkins /var/lib/docker

# Use HTTP update center to avoid SSL issues + pre-install essential plugins
ENV JENKINS_UC=http://updates.jenkins.io

RUN jenkins-plugin-cli --plugins \
    git \
    workflow-aggregator \
    pipeline-stage-view \
    credentials-binding \
    docker-workflow

USER jenkins

VOLUME /var/lib/docker
EXPOSE 8080 50000