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
