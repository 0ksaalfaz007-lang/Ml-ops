-- building docker image
docker built -t jenkins-dind .

-- runnning docker image
docker run -d --name jenkins-dind --privileged -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins-dind

-- getting docker logins for jenkins
docker logs jenkins-dind

-- jenkins password
Jenkins Password : 70cb740cf99a4c31a5839eddbf19a1e8  copy pass and add to web-browser

-- go to browser
localhost:8080 -> select install plugins options to install all plugins at once

-- running docker container for jenkins
docker exec -u root -it jenkins-dind bash

--- run below cmds inside jenkins-container
apt update -y
apt install -y python3
python3 --version
ln -s /usr/bin/python3 /usr/bin/python
python -version
apt install -y python3-pip
apt install -y python3-venv
exit


----------- add the Google Cloud SDK GPG key before installing:

apt-get install -y curl gnupg

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg \
  | gpg --dearmor -o /usr/share/keyrings/google-cloud.gpg

echo "deb [signed-by=/usr/share/keyrings/google-cloud.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
  | tee /etc/apt/sources.list.d/google-cloud-sdk.list
✅ Then install
apt-get update
apt-get install -y google-cloud-sdk

🧪 Verify installation
gcloud version

If it prints a version → ✅ installed successfully.

