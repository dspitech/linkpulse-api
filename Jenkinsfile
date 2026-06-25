pipeline {
  agent any
  environment {
    IMAGE_NAME     = 'linkpulse-api'
    REGISTRY       = 'ghcr.io/dspitech'
    REGISTRY_IMAGE = "${REGISTRY}/${IMAGE_NAME}"
  }
  stages {

    // ============================================================
    // 1. CHECKOUT
    // ============================================================
    stage('1. Checkout') {
      steps {
        checkout scm
        script {
          env.IMAGE_TAG = sh(
            script: 'git rev-parse --short HEAD',
            returnStdout: true
          ).trim()
        }
        echo "Commit : ${env.IMAGE_TAG} | Branche : ${env.BRANCH_NAME}"
      }
    }

    // ============================================================
    // 2. LINT
    // ============================================================
    stage('2. Lint') {
      steps {
        sh '''
          docker run --rm \
            --volumes-from jenkins \
            -w "$WORKSPACE" \
            python:3.12-slim \
            sh -c "pip install flake8 -q && flake8 src/ --max-line-length=100"
        '''
      }
    }

    // ============================================================
    // 3. UNIT TESTS & COVERAGE
    // ============================================================
    stage('3. Unit Tests & Coverage') {
      steps {
        sh '''
          docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
          docker rm -f test-runner 2>/dev/null || true
          set +e
          docker run \
            -e CI=true \
            --name test-runner \
            ${IMAGE_NAME}:${IMAGE_TAG} \
            pytest tests/ -v \
              --cov=src \
              --cov-report=xml:/tmp/coverage.xml \
              --cov-report=term-missing \
              --cov-fail-under=75
          TEST_EXIT_CODE=$?
          set -e
          docker cp test-runner:/tmp/coverage.xml ./coverage.xml 2>/dev/null || true
          docker rm -f test-runner 2>/dev/null || true




          sed -i 's|/app/||g' coverage.xml
          echo "Apercu coverage.xml apres correction des chemins :"
          head -5 coverage.xml

          exit $TEST_EXIT_CODE
        '''
      }
      post {
        failure {
          echo 'Tests echoues ou couverture inferieure a 75%'
        }
      }
    }

    // ============================================================
    // 4. SONARQUBE ANALYSIS
    // ============================================================
    stage('4. SonarQube Analysis') {
      environment {
        SONARQUBE_TOKEN = credentials('sonar-token')
      }
      steps {
        withSonarQubeEnv('sonarqube') {
          sh '''
            docker run --rm \
              --network cicd-network \
              --volumes-from jenkins \
              -w "$WORKSPACE" \
              -e SONAR_HOST_URL="$SONAR_HOST_URL" \
              -e SONAR_TOKEN="$SONARQUBE_TOKEN" \
              sonarsource/sonar-scanner-cli:latest \
              sonar-scanner \
                -Dsonar.projectKey=linkpulse-api \
                -Dsonar.projectName=LinkPulse \
                -Dsonar.projectBaseDir="$WORKSPACE" \
                -Dsonar.sources=src \
                -Dsonar.python.version=3.12 \
                -Dsonar.python.coverage.reportPaths=coverage.xml \
                -Dsonar.sourceEncoding=UTF-8 \
                -Dsonar.scanner.metadataFilePath=$WORKSPACE/report-task.txt
          '''
        }
      }
    }

    // ============================================================
    // 5. QUALITY GATE
    // ============================================================
    stage('5. Quality Gate') {
      steps {
        timeout(time: 15, unit: 'MINUTES') {
          waitForQualityGate abortPipeline: true
        }
      }
    }

    // ============================================================
    // 6. BUILD DOCKER IMAGE
    // ============================================================
    stage('6. Build Docker Image') {
      steps {
        sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
      }
    }

    // ============================================================
    // 7. SECURITY SCAN (TRIVY)
    // ============================================================
    stage('7. Security Scan (Trivy)') {
      steps {
        sh '''
          docker run --rm \
            -v /var/run/docker.sock:/var/run/docker.sock \
            -v trivy-cache:/root/.cache/trivy \
            aquasec/trivy:latest image \
            --severity HIGH,CRITICAL \
            --ignore-unfixed \
            --exit-code 1 \
            --format table \
            ${IMAGE_NAME}:${IMAGE_TAG}
        '''
      }
      post {
        failure {
          echo 'Vulnerabilites CRITICAL ou HIGH detectees - build bloque avant publication.'
        }
      }
    }

    // ============================================================
    // 7.5. GENERATION DU SBOM (Software Bill of Materials)
    // ============================================================
    stage('7.5 SBOM Generation') {
      steps {
        sh '''
          docker run --rm \
            -v /var/run/docker.sock:/var/run/docker.sock \
            -v trivy-cache:/root/.cache/trivy \
            -v "$WORKSPACE":/output \
            aquasec/trivy:latest image \
            --format cyclonedx \
            --output /output/sbom.json \
            ${IMAGE_NAME}:${IMAGE_TAG}
        '''
      }
      post {
        always {
          archiveArtifacts artifacts: 'sbom.json', allowEmptyArchive: true
          echo 'SBOM archive : sbom.json (format CycloneDX)'
        }
      }
    }

    // ============================================================
    // 8. PUSH TO GHCR
    // ============================================================
    stage('8. Push to GHCR') {
      steps {
        withCredentials([usernamePassword(
          credentialsId: 'github-token',
          usernameVariable: 'GITHUB_USER',
          passwordVariable: 'GITHUB_TOKEN'
        )]) {
          sh '''
            echo $GITHUB_TOKEN | docker login ghcr.io -u $GITHUB_USER --password-stdin
            docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY_IMAGE}:${IMAGE_TAG}
            docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY_IMAGE}:latest
            docker push ${REGISTRY_IMAGE}:${IMAGE_TAG}
            docker push ${REGISTRY_IMAGE}:latest
          '''
        }
      }
    }

    // ============================================================
    // 9. TERRAFORM PLAN
    // ============================================================
    stage('9. Terraform Plan') {
      steps {
        sh '''
          terraform -chdir=infra init -upgrade
          terraform -chdir=infra fmt -check
          terraform -chdir=infra validate
        '''
        sh "terraform -chdir=infra plan -var='image_tag=${IMAGE_TAG}'"
      }
    }

    // ============================================================
    // 10. DEPLOYMENT (TERRAFORM APPLY)
    // ============================================================
    stage('10. Deployment') {
      steps {
        sh "terraform -chdir=infra apply -auto-approve -var='image_tag=${IMAGE_TAG}'"
      }
    }

    // ============================================================
    // 10.5. DEPLOIEMENT PORTAINER
    // ============================================================
    stage('10.5 Deploy Portainer') {
      steps {
        sh '''
          echo "Deploiement de Portainer..."
          docker volume create portainer_data 2>/dev/null || true
          docker rm -f portainer 2>/dev/null || true
          docker run -d \
            --name portainer \
            --restart=unless-stopped \
            --network cicd-network \
            -p 9443:9443 \
            -v /var/run/docker.sock:/var/run/docker.sock \
            -v portainer_data:/data \
            portainer/portainer-ce:latest
          echo "Attente du demarrage de Portainer..."
          sleep 10
          if docker ps | grep -q portainer; then
            echo "Portainer deploye avec succes !"
            echo "https://localhost:9443"
          else
            echo "Echec du deploiement de Portainer"
            docker logs portainer --tail 20
            exit 1
          fi
        '''
      }
    }

    // ============================================================
    // 11. SMOKE TEST
    // ============================================================
    stage('11. Smoke Test') {
      steps {
        sh '''
          echo "Attente du demarrage des conteneurs (15s)..."
          sleep 15
          HOST_IP="172.160.228.93"
          echo "Host IP: ${HOST_IP}"

          echo -n "1. Linkpulse : "
          curl -f http://${HOST_IP}:8001/health || exit 1
          echo " /health OK"

          echo -n "2. Metriques : "
          curl -s http://${HOST_IP}:8001/metrics | grep -q links_created_total || exit 1
          echo " /metrics OK"

          echo "3. Attente d un cycle de scrape Prometheus (20s)..."
          sleep 20

          echo -n "4. Prometheus : "
          curl -s "http://${HOST_IP}:9090/api/v1/query?query=up%7Bjob%3D%22linkpulse-api%22%7D" \
            | grep -q '"value"' || exit 1
          echo " Prometheus OK"

          echo -n "5. Grafana : "
          curl -f http://${HOST_IP}:3000/api/health || exit 1
          echo " Grafana OK"

          echo -n "6. Portainer : "
          curl -k -f https://${HOST_IP}:9443/api/status || exit 1
          echo " Portainer OK"

          echo ""
          echo "Smoke Test reussi : tous les services sont operationnels."
        '''
      }
      post {
        failure {
          sh 'docker logs linkpulse-staging --tail 20 || true'
          sh 'docker logs prometheus --tail 20 || true'
          sh 'docker logs portainer --tail 20 || true'
          echo 'Smoke Test KO -- voir logs des conteneurs ci-dessus'
        }
      }
    }

    // ============================================================
    // 12. SLACK NOTIFICATION (NOUVEAU STAGE VISIBLE)
    // ============================================================
    stage('12. Slack Notification') {
      steps {
        script {
          // Récupérer le statut global du pipeline
          def currentStatus = currentBuild.currentResult
          def statusColor = currentStatus == 'SUCCESS' ? '#36a64f' : '#ff0000'
          def statusTitle = currentStatus == 'SUCCESS' ? 'Pipeline reussi' : 'Pipeline en echec'

          withCredentials([string(credentialsId: 'slack-webhook-url', variable: 'SLACK_URL')]) {
            if (currentStatus == 'SUCCESS') {
              sh '''
                JSON=$(printf \
                  '{"attachments":[{"color":"#36a64f","title":" Pipeline reussi - LinkPulse","fields":[{"title":"Commit","value":"%s","short":true},{"title":"Image","value":"%s","short":false},{"title":"Environnement","value":"Staging","short":true}],"footer":"Jenkins - LinkPulse CI","ts":%s}]}' \
                  "$IMAGE_TAG" \
                  "$REGISTRY_IMAGE:$IMAGE_TAG" \
                  "$(date +%s)"
                )
                curl -s -X POST "$SLACK_URL" \
                  -H 'Content-Type: application/json' \
                  -d "$JSON"
              '''
            } else {
              sh '''
                JSON=$(printf \
                  '{"attachments":[{"color":"#ff0000","title":"Pipeline en echec - LinkPulse","fields":[{"title":"Commit","value":"%s","short":true},{"title":"Build","value":"%s","short":true},{"title":"Lien","value":"%s","short":false}],"footer":"Jenkins - LinkPulse CI","ts":%s}]}' \
                  "$IMAGE_TAG" \
                  "$BUILD_NUMBER" \
                  "${BUILD_URL}console" \
                  "$(date +%s)"
                )
                curl -s -X POST "$SLACK_URL" \
                  -H 'Content-Type: application/json' \
                  -d "$JSON"
              '''
            }
          }
        }
      }
    }

  }
  post {
    always {
      sh 'docker rm -f test-runner 2>/dev/null || true'
    }
    success {
      echo "Pipeline reussi - Image : ${REGISTRY_IMAGE}:${IMAGE_TAG}"
    }
    failure {
      echo 'Pipeline en echec - consultez les logs du stage concerne ci-dessus.'
    }
  }
}
