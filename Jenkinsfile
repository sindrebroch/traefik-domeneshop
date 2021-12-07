pipeline {

    agent any

    tools {
      dockerTool('docker')
    }

    environment {
        registry = "docker.local.sindrebroch.no/traefik-domeneshop"
    }

    stages {
        stage('Build image') {
            steps {
                sh "docker build . -t docker.local.sindrebroch.no/traefik-domeneshop"
                sh "docker push docker.local.sindrebroch.no/traefik-domeneshop"
            }
        }
    }   
}
