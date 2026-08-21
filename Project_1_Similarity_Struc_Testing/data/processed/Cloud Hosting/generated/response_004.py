import os
import subprocess
import requests
import json
from urllib .parse import urlparse

def install_java ():
    try :

        subprocess .run (['sudo','apt','update'])
        subprocess .run (['sudo','apt','install','openjdk-11-jdk'])
    except Exception as e :
        print (f"Error installing Java: {e}")

def install_jenkins ():
    try :

        subprocess .run (['curl','-fsSL','https://pkg.jenkins.io/debian-stable/jenkins.io.key','|','sudo','tee','/usr/share/keyrings/jenkins-keyring.asc','>','/dev/null'])
        subprocess .run (['echo','deb','[signed-by=/usr/share/keyrings/jenkins-keyring.asc]','https://pkg.jenkins.io/debian-stable','binary/','|','sudo','tee','/etc/apt/sources.list.d/jenkins.list','>','/dev/null'])

        subprocess .run (['sudo','apt','update'])
        subprocess .run (['sudo','apt','install','jenkins'])
    except Exception as e :
        print (f"Error installing Jenkins: {e}")

def start_jenkins_service ():
    try :

        subprocess .run (['sudo','systemctl','start','jenkins'])
        subprocess .run (['sudo','systemctl','enable','jenkins'])
    except Exception as e :
        print (f"Error starting Jenkins service: {e}")

def access_jenkins ():
    try :

        jenkins_url ='http://localhost:8080'

        subprocess .run (['xdg-open',jenkins_url ])
    except Exception as e :
        print (f"Error accessing Jenkins: {e}")

def configure_jenkins ():
    try :

        plugins =['git','github','docker','pipeline']
        for plugin in plugins :
            subprocess .run (['sudo','jenkins-cli','install-plugin',plugin ])

    except Exception as e :
        print (f"Error configuring Jenkins: {e}")

def create_jenkins_pipeline ():
    try :

        jenkinsfile ="""
        pipeline {
            agent any
            stages {
                stage('Checkout') {
                    steps {
                        checkout scm
                    }
                }
                stage('Build') {
                    steps {
                        sh 'make build'  // or your build command
                    }
                }
                stage('Test') {
                    steps {
                        sh 'make test'  // or your test command
                    }
                }
                stage('Docker Build & Push') {
                    steps {
                        script {
                            dockerImage = docker.build("your_repo/your_app:\${env.BUILD_ID}")
                            docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                                dockerImage.push()
                            }
                        }
                    }
                }
                stage('Deploy to Staging') {
                    steps {
                        sh 'deploy_to_staging_script.sh'
                    }
                }
                stage('Deploy to Production') {
                    steps {
                        input "Deploy to Production?"
                        sh 'deploy_to_prod_script.sh'
                    }
                }
            }
        }
        """
        with open ('Jenkinsfile','w')as f :
            f .write (jenkinsfile )
    except Exception as e :
        print (f"Error creating Jenkins pipeline: {e}")

def main ():
    install_java ()
    install_jenkins ()
    start_jenkins_service ()
    access_jenkins ()
    configure_jenkins ()
    create_jenkins_pipeline ()

if __name__ =="__main__":
    main ()