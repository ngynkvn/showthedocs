#!/bin/bash

set -x
set -e

if [[ $(whoami) != "showthedocs" ]]; then
  echo 'run this script as user showthedocs'
  read -p "create user showthedocs and switch to it? " -r
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo adduser showthedocs
    sudo usermod -aG sudo showthedocs
    echo 'run sudo -i -u showthedocs and rerun this script'
  else
    exit
  fi
fi

sudo apt-get update -y
sudo apt-get upgrade -y

sudo apt-get install -y git make python-pip
sudo apt-get install -y nginx supervisor
sudo apt-get install -y libxml2-dev libxslt1-dev python-dev npm

echo "showthedocs: setting up sass"
sudo ln -s "$(which nodejs)" /usr/bin/node
sudo npm install -g sass

echo "showthedocs: setting up showthedocs"

sudo pip install --upgrade pip
sudo pip install virtualenv

CLONE=~/repo
git clone https://github.com/idank/showthedocs.git $CLONE
virtualenv env
source env/bin/activate

pip install uwsgi

cd $CLONE
cat <<EOF >>showdocs/config.py

TEST = False
LOG = True
EOF

pip install -r requirements.txt
./getdocs clone

sudo cp misc/supervisor.conf /etc/supervisor/conf.d/uwsgi.conf
sudo cp misc/nginx.conf /etc/nginx/sites-available/showthedocs.conf
cd /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/showthedocs.conf showthedocs
sudo rm default ../sites-available/default || true

cd
mkdir logs
sudo /etc/init.d/supervisor start
sleep 2
sudo supervisorctl reload
sleep 2
sudo supervisorctl restart uwsgi
sudo /etc/init.d/nginx reload

echo "showthedocs: DONE"
