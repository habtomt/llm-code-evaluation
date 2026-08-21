import os
import yaml
import paramiko
import ssh2

def init_git_repo ():

    with open ('index.html','w')as f :
        f .write ('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Static Site</title>
</head>
<body>
    <h1>Welcome to My Static Website!</h1>
    <p>This site is served using a continuous deployment pipeline.</p>
</body>
</html>''')

    os .system ('git init')
    os .system ('git add .')
    os .system ('git commit -m "Initial commit"')

    os .system ('git remote add origin https://github.com/your-username/your-repo-name.git')
    os .system ('git branch -M main')
    os .system ('git push -u origin main')

def deploy_static_files ():

    with open ('deploy.yml','w')as f :
        workflow ='''name: Deploy to Server

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Copy files via SSH
      uses: appleboy/scp-action@v0.1.8
      with:
        host: ${{ secrets.SERVER_HOST }}
        username: ${{ secrets.SERVER_USER }}
        key: ${{ secrets.SERVER_KEY }}
        source: "src" # Replace with the path to static files, if necessary
        target: "/var/www/html" # Directory on the server
'''
        f .write (yaml .dump (yaml .safe_load (workflow ),default_flow_style =False ))

def configure_secrets ():

    secrets =['SERVER_HOST','SERVER_USER','SERVER_KEY']
    for secret in secrets :
        os .system (f'echo {secret} > .github/secrets/{secret}')

def configure_nginx ():

    ssh_client =paramiko .SSHClient ()
    ssh_client .set_missing_host_key_policy (paramiko .AutoAddPolicy ())
    ssh_client .connect ('your-server-ip',username ='your-username',key_filename ='your-private-key')

    ssh_client .exec_command ('sudo apt update')
    ssh_client .exec_command ('sudo apt install nginx')

    nginx_config ='''server {
        listen 80;
        listen [::]:80;

        root /var/www/html;
        index index.html;

        server_name your-domain.com;  # Substitute your domain or server IP

        location / {
            try_files $uri $uri/ =404;
        }
    }'''
    ssh_client .exec_command (f'sudo nano /etc/nginx/sites-available/default')
    stdin ,stdout ,stderr =ssh_client .exec_command (f'echo {nginx_config} >> /etc/nginx/sites-available/default')
    ssh_client .exec_command ('sudo systemctl restart nginx')

    ssh_client .close ()

if __name__ =='__main__':
    init_git_repo ()
    deploy_static_files ()
    configure_secrets ()
    configure_nginx ()