# LinkPulse - Projet DevOps - E4 ESTIAM Paris -  2026/2026


## Membres du Groupe 10

| N° | Nom et Prénom |
|----|---------------|
| 1 | LO Pape |
| 2 | Youssef EL-ATTAOUI |
| 3 | Olivier POLYNICE |
| 4 | Elodie IPARRAGUIRRE |
| 4 | Randy Neil TCHIMKIO KOUAMO |

<div align="center">

![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![SonarQube](https://img.shields.io/badge/SonarQube-4E9BCD?style=for-the-badge&logo=sonarqube&logoColor=white)
![Trivy](https://img.shields.io/badge/Trivy-1904DA?style=for-the-badge&logo=aqua&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana_as_Code-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![k6](https://img.shields.io/badge/k6-7D64FF?style=for-the-badge&logo=k6&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![FastAPI](https://img.shields.io/badge/API_Key_Auth-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Jenkins](https://img.shields.io/badge/Rollback-D24939?style=for-the-badge&logo=jenkins&logoColor=white)


**Un push sur `main`, et un pipeline Jenkins en 12 étapes build, teste, analyse, sécurise, déploie et supervise automatiquement une vraie API REST - sans aucune intervention manuelle.**

</div>

---

## Concept du projet

**LinkPulse** est une API REST de raccourcissement de liens (façon Bitly) avec suivi des clics, écrite en **Python / FastAPI**. Elle n'est pas un simple « hello world » : elle porte une logique métier réelle (créer un lien, le rediriger, compter les clics, désactiver un lien) qui alimente des métriques Prometheus significatives et un Quality Gate SonarQube crédible.


### Fonctionnalités de l'API

| Endpoint | Méthode | Rôle |
|---|---|---|
| `/api/links` | `POST` | Crée un lien raccourci à partir d'une URL longue |
| `/api/links` | `GET` | Liste les liens (pagination `skip` / `limit`) |
| `/api/links/{code}` | `GET` | Détail d'un lien |
| `/api/links/{code}/stats` | `GET` | Statistiques de clics |
| `/api/links/{code}` | `DELETE` | Désactive un lien |
| `/r/{code}` | `GET` | Redirection HTTP 307 vers l'URL d'origine |
| `/health` | `GET` | Sonde de santé pour Docker / Terraform |
| `/metrics` | `GET` | Métriques Prometheus (`links_created_total`, `redirects_total`, …) |

### Stack DevOps couverte par le lab

| Brique | Outil | Rôle |
|---|---|---|
| Versionnement | Git + GitHub | Source de vérité, déclencheur via webhook |
| Conteneurisation | Docker + Compose | Packaging reproductible |
| CI/CD | Jenkins | Orchestration en 12 stages |
| Qualité | SonarQube | Quality Gate (couverture, bugs, dette) |
| Sécurité | Trivy | Blocage sur CVE CRITICAL/HIGH |
| IaC | Terraform | Déploiement déclaratif app + monitoring |
| Observabilité | Prometheus + Grafana | Métriques et dashboards |
| Registry | GHCR | Images taguées par SHA Git |

### Flux CI/CD (vue d'ensemble)

```
git push main
    │
    ▼
GitHub webhook ──► Jenkins
                      │
    ┌─────────────────┼─────────────────┐
    │ 1 Checkout      │ 2 Lint          │ 3 Tests + couverture
    │ 4 SonarQube     │ 5 QG webhook    │ 6 Build image
    │ 7 Trivy scan    │ 8 Push GHCR     │ 9-10 Terraform
    │ 11 Smoke test   │                 │
    └─────────────────┴─────────────────┘
                      ▼
         linkpulse-staging + Prometheus + Grafana
```

### Résumé du projet 
**1. LinkPulse est une API REST de raccourcissement de liens (façon Bitly) développée en Python/FastAPI, qui sert de support concret pour mettre en œuvre une chaîne CI/CD complète et industrialisée.**

**2. Le projet automatise intégralement le cycle de vie de l'application via un pipeline Jenkins en 12 étapes : linting, tests unitaires avec couverture (98%), analyse SonarQube avec Quality Gate, scan de sécurité Trivy, construction et publication de l'image Docker sur GHCR, puis déploiement déclaratif avec Terraform.**

**3. L'infrastructure de supervision est entièrement codée en Terraform et déploie simultanément l'application sur le port 8001, Prometheus pour la collecte des métriques, Grafana pour la visualisation en dashboards, et Portainer pour la gestion centralisée des conteneurs.**

**4. Le pipeline inclut un Smoke Test post-déploiement qui valide automatiquement la disponibilité de l'API, la présence des métriques métier (liens créés, redirections, taux d'erreur), le bon fonctionnement de Prometheus et Grafana, ainsi que l'intégrité des services de supervision.**

**5. Ce projet démontre une maîtrise complète des outils DevOps modernes : Docker pour la conteneurisation, Jenkins pour l'orchestration CI/CD, SonarQube pour la qualité du code, Trivy pour la sécurité, Terraform pour l'IaC, Prometheus/Grafana pour l'observabilité, et GitHub Actions comme déclencheur via webhook - le tout formant une plateforme d'intégration et de déploiement continu entièrement automatisée et reproductible.**

---

## Table des matières

- [Concept du projet](#concept-du-projet)

### Partie I - Contexte et préparation
- [A. Présentation du lab](#a-présentation-du-lab)
- [B. Prérequis](#b-prérequis)
- [C. Concept](#c-concept)
- [D. Variables à personnaliser](#d-variables-à-personnaliser)
- [E. Architecture cible](#e-architecture-cible)
- [F. Structure finale du projet](#f-structure-finale-du-projet)
- [Concept clé : le réseau `cicd-network`](#concept-clé--le-réseau-cicd-network)

### Partie II - Mise en place pas à pas
- [Phase 0 - Préparation de la VM](#phase-0---préparation-de-la-vm)
- [Phase 1 - Dépôt GitHub et structure](#phase-1---créer-le-dépôt-github-et-la-structure-du-projet)
- [Phase 2 - Code applicatif](#phase-2---code-applicatif)
- [Phase 3 - Conteneurisation](#phase-3---conteneurisation)
- [Phase 4 - Jenkins](#phase-4---jenkins)
- [Phase 5 - SonarQube](#phase-5---sonarqube)
- [Phase 8 - Jenkinsfile et webhooks](#phase-8---jenkinsfile-job-jenkins-et-webhook-github)
- [Phase 9 - Dashboard Grafana as Code](#phase-9---dashboard-grafana-as-code)
- [Phase 10 - Notifications Slack](#phase-10---notifications-slack)
- [Phase 11 - Pre-commit hooks](#phase-11---pre-commit-hooks)
- [Phase 13 - SBOM avec Trivy](#phase-13---sbom-avec-trivy)
- [Phase 14 - Déploiement Portainer](#phase-14---déploiement-portainer)

### Partie III - Utilisation et validation
- [Phase 14 - Gestion et création des liens](#phase-14--gestion-et-création-des-liens)
- [Vérification dans Prometheus](#vérification-dans-prometheus)
- [Interface Grafana](#interface-grafana)

### Partie IV - Extensions et dépannage
- [I. FAQ et dépannage](#i-faq-et-dépannage)
  
---

## A. Présentation du lab

> **Rappel :** le concept détaillé de LinkPulse et le schéma du pipeline se trouvent en tête de document.

### Construction

**LinkPulse** est une API REST de raccourcissement de liens (façon Bitly) avec suivi des clics, écrite en Python/FastAPI. Elle sert de support concret pour mettre en pratique une chaîne CI/CD complète :

| Brique | Outil | Rôle dans le lab |
|---|---|---|
| Versionnement | Git + GitHub | Source de vérité du code, déclencheur du pipeline via webhook |
| Conteneurisation | Docker + Docker Compose | Packager l'application de façon reproductible |
| Automatisation | Jenkins | Orchestrer build, tests, analyse, sécurité, déploiement |
| Qualité du code | SonarQube | Bloquer la publication si le code est insuffisamment testé ou mal écrit |
| Sécurité | Trivy | Bloquer la publication si l'image contient des CVE critiques |
| Infrastructure as Code | Terraform | Déployer l'application et la stack de supervision de façon déclarative |
| Observabilité | Prometheus + Grafana | Mesurer et visualiser le comportement de l'application en continu |


---

## B. Prérequis

Avant de commencer, assurez-vous de disposer de :

- Une **VM Linux** (Ubuntu 22.04/24.04 ou Debian) avec **Docker** et **Docker Compose** installés et fonctionnels (`docker --version`, `docker compose version`).

- Un accès **SSH** à cette VM avec des droits suffisants pour lancer des conteneurs Docker.

- Un **compte GitHub** avec les droits de création de dépôt public, de webhook, et de génération de Personal Access Token.

- Un **compte SonarQube** (auto-hébergé sur la VM dans ce lab - aucun compte externe requis).

- Optionnel : un compte **ngrok** (ou équivalent) si votre VM n'a pas d'IP publique fixe, pour exposer Jenkins à GitHub.

- Au moins **6 Go de RAM** disponibles sur la VM (Jenkins, SonarQube/Elasticsearch, Prometheus et Grafana tournent simultanément).


---

## C. Concept

| Terme | Définition courte |
|---|---|
| **Webhook** | Notification HTTP automatique envoyée par un service A vers un service B dès qu'un événement se produit (ici : un push GitHub, ou la fin d'une analyse SonarQube) |
| **Quality Gate** | Ensemble de seuils de qualité (couverture de tests, bugs, sécurité) qu'un build doit respecter pour continuer dans le pipeline |
| **DooD (Docker-out-of-Docker)** | Technique permettant à un conteneur (Jenkins) de piloter le démon Docker de la machine hôte en montant son socket (`/var/run/docker.sock`), sans faire tourner son propre démon Docker interne |
| **IaC (Infrastructure as Code)** | Décrire l'infrastructure (réseaux, conteneurs) dans des fichiers versionnés plutôt que via des commandes manuelles - ici avec Terraform |
| **Resource vs Data source (Terraform)** | Une *resource* est créée et gérée par Terraform ; un *data source* est seulement lu par Terraform, sans qu'il en revendique la propriété - voir section 0 du déroulé |
| **Healthcheck** | Sonde périodique qui vérifie qu'un conteneur répond correctement, pas seulement qu'il est démarré |
| **Smoke test** | Suite de vérifications rapides après déploiement, pour confirmer que les services essentiels répondent avant de considérer le déploiement réussi |
| **Fail Fast** | Principe consistant à placer les vérifications les moins coûteuses (lint) avant les plus coûteuses (build, déploiement), pour échouer le plus tôt possible |
| **SHA court Git** | Les 7 premiers caractères du hash d'un commit (`git rev-parse --short HEAD`), utilisés comme tag d'image Docker pour une traçabilité exacte code ↔ image |
| **Idempotence** | Propriété d'une opération qui produit toujours le même résultat si on la répète - `terraform apply` rejoué sans changement ne doit rien modifier |

---

## D. Variables à personnaliser

Avant de commencer, repérez ces trois éléments : ils reviennent à plusieurs endroits et **doivent être remplacés partout, de façon cohérente**, sous peine d'erreurs de configuration difficiles à diagnostiquer.

| Placeholder | À remplacer par | Utilisé dans |
|---|---|---|
| `VOTRE_PSEUDO` | Votre pseudo GitHub réel | `Jenkinsfile` (variable `REGISTRY`), `infra/variables.tf` (variable `registry`), commandes `git clone`/`gh repo create` |
| `labadmin` | Votre utilisateur réel sur la VM | `infra/variables.tf` (variable `data_path`, ex. `/home/VOTRE_USER/linkpulse-data`) |
| `<IP_VM>` ou `VOTRE_URL_JENKINS` | L'adresse réelle de votre VM ou l'URL de votre tunnel ngrok | Accès navigateur à Jenkins/SonarQube/Grafana, configuration du webhook GitHub |

> **Astuce :** une fois le dépôt cloné, une recherche `grep -rn "VOTRE_PSEUDO" .` vous permet de vérifier que tous les emplacements ont bien été mis à jour avant de pousser quoi que ce soit.


---

## E. Architecture cible

<img width="1024" height="559" alt="image" src="https://github.com/user-attachments/assets/060ea7e9-036a-46f7-85af-7ce63e1dc43b" />


Tous les conteneurs d'infrastructure (Jenkins, SonarQube, l'application, Prometheus, Grafana) partagent le même réseau Docker `cicd-network`, ce qui leur permet de se contacter **par nom de service** plutôt que par adresse IP.

---

## F. Structure finale du projet

```
linkpulse-api/
├── src/
│   ├── __init__.py
│   ├── main.py                # routes FastAPI + instrumentation Prometheus
│   ├── storage.py              # couche d'accès SQLite
│   ├── shortener.py            # génération de code court unique
│   └── schemas.py              # schémas Pydantic
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # base de test isolée
│   ├── test_api.py             # 9 tests d'intégration
│   └── test_shortener.py       # 3 tests unitaires
├── infra/
│   ├── main.tf                 # data source réseau + image + conteneur app
│   ├── variables.tf            # image_tag, app_port, data_path, registry
│   ├── outputs.tf               # app_url, container_id, network_name
│   └── monitoring.tf            # ressources Prometheus + Grafana
├── monitoring/
│   ├── prometheus.yml           # scrape config
│   └── alerts.yml               # règles d'alerte
├── Dockerfile
├── docker-compose.yml           # environnement de dev local
├── .dockerignore
├── .gitignore
├── requirements.txt
├── Makefile
├── Jenkinsfile                  # pipeline déclaratif 12 stages
└── README.md
```

---

## Concept clé : le réseau `cicd-network`

C'est le point le plus important à comprendre avant de commencer, car il détermine l'ordre exact des opérations.

**`cicd-network` est créé une seule fois, manuellement, en tout premier - avant même de démarrer Jenkins ou SonarQube.** Pourquoi ne peut-on pas laisser Terraform s'en charger ?

- Jenkins doit rejoindre `cicd-network` **dès sa création** pour que le stage `Smoke Test` puisse plus tard résoudre `linkpulse-staging`, `prometheus` et `grafana` par leur nom.

- SonarQube doit rejoindre `cicd-network` **dès sa création** pour que Jenkins puisse le contacter via `http://sonarqube:9000` et que le webhook retour `http://jenkins:8080/sonarqube-webhook/` fonctionne.

- Or Terraform **tourne à l'intérieur de Jenkins** (c'est Jenkins qui exécute `terraform apply` dans le pipeline). Le réseau doit donc déjà exister **avant** que Jenkins lui-même ne démarre.

**Conséquence sur la conception des fichiers Terraform** : dans `infra/main.tf`, le réseau n'est pas déclaré comme une **resource** (que Terraform créerait et revendiquerait comme sienne) mais comme un **data source** (que Terraform se contente de lire) :

```hcl
data "docker_network" "cicd" {
  name = "cicd-network"
}
```

Avec ce choix, il n'y a **plus aucun risque d'erreur `network with name cicd-network already exists`**, et plus besoin de `terraform import`. Le réseau est créé une fois pour toutes en Phase 0, point final - et **aucun `terraform apply` manuel n'est jamais nécessaire** : le tout premier push sur `main` exécute lui-même `terraform init`, `plan` puis `apply` via les stages 9 et 10 du Jenkinsfile.


---

## Phase 0 - Préparation de la VM

Cette phase ne se fait **qu'une seule fois**, avant tout le reste.

### Configuration de la VM

- Se connecter à Azure

![image](https://hackmd.io/_uploads/H1wcOHrzMl.png)

- Lancer le Cloud Shell

![image](https://hackmd.io/_uploads/HkAoOBBMzx.png)

![image](https://hackmd.io/_uploads/rJVkFSHGMg.png)

- **Cloner La configuration de la VM**

```bash
git clone https://github.com/dspitech/DevOps-VM-Ubuntu-Terraform-Azure.git
```

![image](https://hackmd.io/_uploads/r1uWtSrzzg.png)

- Se placer dans le répertoire de la VM

```bash
cd DevOps-VM-Ubuntu-Terraform-Azure
```

![image](https://hackmd.io/_uploads/ryBmKSBGzx.png)

- Exécuter le backend

```bash
chmod +x ./setup-backend.sh
./setup-backend.sh
```

![image](https://hackmd.io/_uploads/Byz9YBSzMl.png)

- vérifier le nom du Storage Account créé

```bash
az storage account list --resource-group OpenLab-TFState-RG --query "[].name" -o tsv
```

![image](https://hackmd.io/_uploads/H1fhYSSMzx.png)

Puis mettez-le dans backend.tf : storage_account_name = "openlabtfstate+"   # ← le nom réel

![image](https://hackmd.io/_uploads/BykW9rHMzx.png)

- Initialiser Terraform (téléchargement des providers)

- Formater les fichiers Terraform selon les conventions

- Vérifier la syntaxe et la cohérence de la configuration

- Afficher les ressources qui vont être créées/modifiées

- Déployer l'infrastructure sans confirmation interactive

```bash
terraform init && terraform fmt && terraform validate && terraform plan && terraform apply -auto-approve
```

![image](https://hackmd.io/_uploads/Hy0GcBSGMg.png)

![image](https://hackmd.io/_uploads/H1iX9BSfGe.png)

![image](https://hackmd.io/_uploads/rJ76crSMfl.png)

![image](https://hackmd.io/_uploads/HJx1oSBGMl.png)

- Télécharger la clé privée SSH générée par Terraform

```bash
download ./openlab_rsa
```

![image](https://hackmd.io/_uploads/Sk7roSSzMx.png)

- Se connecter à la machine distante via SSH

```bash
ssh -i "C:\\Users\\dev\\Downloads\\openlab_rsa" labadmin@4.225.216.24
```

![image](https://hackmd.io/_uploads/HyIYirHGfl.png)

- Vérification rapide des prérequis sur la VM

```bash
echo "=== VÉRIFICATION DES OUTILS INSTALLÉS ===" && \
echo "Docker:      $(docker --version 2>/dev/null || echo 'Non installé')" && \
echo "Compose:     $(docker compose version 2>/dev/null || echo 'Non installé')" && \
echo "Make:        $(make --version 2>/dev/null | head -1 || echo 'Non installé')" && \
echo "Git:         $(git --version 2>/dev/null || echo 'Non installé')" && \
echo "GitHub CLI:  $(gh --version 2>/dev/null | head -1 || echo 'Non installé')" && \
echo "ngrok:       $(ngrok --version 2>/dev/null || echo 'Non installé')" && \
echo "curl:        $(curl --version 2>/dev/null | head -1 || echo 'Non installé')" && \
echo "OS:          $(lsb_release -ds 2>/dev/null || grep PRETTY_NAME /etc/os-release | cut -d'"' -f2)" && \
echo "Kernel:      $(uname -r)" && \
echo "" && \
echo "=== MÉMOIRE ===" && free -h && \
echo "" && \
echo "=== DISQUE ===" && df -h -T && \
echo "" && \
echo "=== UPTIME ===" && uptime
```

![image](https://hackmd.io/_uploads/rJAnirBzfl.png)

#### Création du réseau partage - Jenkins et SonarQube

```bash
docker network inspect cicd-network >/dev/null 2>&1 || docker network create cicd-network
```

![image](https://hackmd.io/_uploads/B12WnSSGfx.png)

**Explication du code :** Cette commande crée un réseau bridge Docker nommé `cicd-network`. L'idiome `inspect ... || create` la rend **idempotente** : si le réseau existe déjà, `inspect` réussit et la création est ignorée - vous pouvez la rejouer sans risque. Tous les conteneurs rejoignant ce réseau pourront se contacter **par nom de service** (ex : `http://sonarqube:9000`) sans connaître leurs adresses IP dynamiques.

`docker network inspect cicd-network >/dev/null 2>&1 || docker network create cicd-network` est un idiome shell classique : la commande de gauche tente d'inspecter le réseau ; si elle échoue (réseau absent), `||` déclenche la création. Résultat : la commande est rejouable sans erreur, peu importe l'état de départ.

À ce stade, `docker network ls` doit afficher une ligne `cicd-network`. Si ce n'est pas le cas, ne passez pas à la suite.

- Vérification

```bash
docker network ls | grep cicd-network
```

![image](https://hackmd.io/_uploads/SJ-Q3HrMfx.png)

- Création du dossier qui persistera la base SQLite de LinkPulse en staging

```bash
mkdir -p \~/linkpulse-data
```

`mkdir -p \~/linkpulse-data` crée le répertoire hôte qui persistera la base SQLite entre les redémarrages du conteneur de staging.

![image](https://hackmd.io/_uploads/B1I83HBMGx.png)

---

## Phase 1 - Créer le dépôt GitHub et la structure du projet

### 1.1 Créer le dépôt sur GitHub

| Champ | Valeur exacte |
|---|---|
| Nom du repo | `linkpulse-api` |
| Visibilité | **Public** (nécessaire pour le webhook GitHub → Jenkins et GHCR) |
| Initialisation | README + `.gitignore` Python + Licence MIT |

```bash
gh auth login
```

![image](https://hackmd.io/_uploads/HJFp3SSGMe.png)

![image](https://hackmd.io/_uploads/SkHA3SHfzg.png)

![image](https://hackmd.io/_uploads/Byg1TBBGfx.png)

![image](https://hackmd.io/_uploads/S1c1TrSMGg.png)

![image](https://hackmd.io/_uploads/H1MZaSBzMg.png)

![image](https://hackmd.io/_uploads/rJjzTHBMGl.png)

![image](https://hackmd.io/_uploads/HkBrTBrfzx.png)

![image](https://hackmd.io/_uploads/SywIarHGfl.png)

![image](https://hackmd.io/_uploads/HJPj6BSzGe.png)

![image](https://hackmd.io/_uploads/rkah6rBzGl.png)

```bash
git config --global user.name "Tech-Devo"
git config --global user.email "devo12@gmail.com"
git config --global --list
```

![image](https://hackmd.io/_uploads/BJi8RrSMzg.png)

```bash
gh repo create linkpulse-api \
  --public \
  --license MIT \
  --gitignore Python
```

![image](https://hackmd.io/_uploads/rkIuCHSMfg.png)

![image](https://hackmd.io/_uploads/SkA9RHHzGl.png)

```bash
git clone https://github.com/dspitech/linkpulse-api.git
```

![image](https://hackmd.io/_uploads/H19RRSSfMx.png)

```bash
cd linkpulse-api
```

![image](https://hackmd.io/_uploads/Skayy8Sffx.png)

### 1.2 Créer l'arborescence complète du projet

```bash
mkdir -p src tests infra monitoring
touch src/__init__.py tests/__init__.py
# Verifier la structure creee
find . -not -path './.git/*' | sort
```

![image](https://hackmd.io/_uploads/SJHEyIBzzx.png)

**Explication :** `mkdir -p src tests infra monitoring` crée les quatre dossiers en une seule commande. `touch src/__init__.py tests/__init__.py` crée les fichiers vides qui transforment `src/` et `tests/` en packages Python importables.

---

## Phase 2 - Code applicatif

Exécutez-les depuis la racine du dépôt `linkpulse-api/`.

### 2.1 `src/storage.py` - couche d'accès SQLite

```bash
cat > src/storage.py <<'EOF'
"""Couche de persistance SQLite pour les liens raccourcis.

Le chemin de la base est piloté par la variable d'environnement DB_PATH,
ce qui permet de pointer vers un volume Docker en staging/production tout
en gardant un fichier local simple en developpement.
"""

import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Optional

DB_PATH = os.environ.get("DB_PATH", "linkpulse.db")


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Cree la table 'links' si elle n'existe pas encore."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS links (
                code TEXT PRIMARY KEY,
                url TEXT NOT NULL,
                created_at TEXT NOT NULL,
                clicks INTEGER NOT NULL DEFAULT 0,
                active INTEGER NOT NULL DEFAULT 1
            )
            """
        )
        conn.commit()


def code_exists(code: str) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM links WHERE code = ?",
            (code,),
        ).fetchone()

    return row is not None


def create_link(code: str, url: str) -> dict:
    created_at = datetime.now(timezone.utc).isoformat()

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO links (code, url, created_at, clicks, active) "
            "VALUES (?, ?, ?, 0, 1)",
            (code, url, created_at),
        )
        conn.commit()

    return {
        "code": code,
        "url": url,
        "created_at": created_at,
        "clicks": 0,
        "active": 1,
    }


def get_link(code: str) -> Optional[dict]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM links WHERE code = ?",
            (code,),
        ).fetchone()

    return dict(row) if row else None


def list_links(skip: int = 0, limit: int = 20) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM links ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, skip),
        ).fetchall()

    return [dict(row) for row in rows]


def increment_clicks(code: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE links SET clicks = clicks + 1 WHERE code = ?",
            (code,),
        )
        conn.commit()


def deactivate_link(code: str) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE links SET active = 0 WHERE code = ?",
            (code,),
        )
        conn.commit()

    return cursor.rowcount > 0


def count_active_links() -> int:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS total FROM links WHERE active = 1"
        ).fetchone()

    return row["total"] if row else 0
EOF
```

![image](https://hackmd.io/_uploads/HyWikIrfGx.png)

**Explication du code - `src/storage.py` :** Ce module implémente le pattern **Repository** : toute la logique d'accès à SQLite est centralisée ici, et le reste de l'application ne manipule que des dictionnaires Python ordinaires. Le décorateur `@contextmanager` sur `get_connection()` garantit que la connexion est **toujours fermée** après usage, même en cas d'exception. `conn.row_factory = sqlite3.Row` permet d'accéder aux colonnes par nom (`row["code"]`) plutôt que par index. `DB_PATH` est lu depuis l'environnement au moment de l'import, ce qui permet d'utiliser `linkpulse.db` en local et un volume Docker monté en staging sans toucher au code.

### 2.2 `src/shortener.py` - génération de code court

```bash
cat > src/shortener.py <<'EOF'
"""Generation de codes courts uniques pour les liens raccourcis."""

import secrets
import string

from src.storage import code_exists

ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 6
MAX_ATTEMPTS = 10


def generate_unique_code() -> str:
    """Genere un code alphanumerique de 6 caracteres garanti unique en base.

    Reessaie jusqu'a MAX_ATTEMPTS fois en cas de collision (tres rare avec
    62^6 combinaisons possibles) avant d'abandonner explicitement.
    """
    for _ in range(MAX_ATTEMPTS):
        candidate = "".join(
            secrets.choice(ALPHABET) for _ in range(CODE_LENGTH)
        )
        if not code_exists(candidate):
            return candidate

    raise RuntimeError(
        "Impossible de generer un code court unique apres "
        f"{MAX_ATTEMPTS} tentatives."
    )
EOF
```

![image](https://hackmd.io/_uploads/HygAkUrfzl.png)

**Explication du code - `src/shortener.py` :** `random.choices(ALPHABET, k=CODE_LENGTH)` tire 6 caractères indépendants parmi 62 (26 minuscules + 26 majuscules + 10 chiffres), donnant 62⁶ ≈ 56 milliards de codes possibles - les collisions sont statistiquement négligeables. La boucle `for _ in range(MAX_ATTEMPTS)` protège contre le cas théorique de saturation : si 10 tentatives successives tombent sur des codes existants, une `RuntimeError` explicite est levée plutôt qu'une boucle infinie. La séparation dans son propre module facilite les tests unitaires indépendants (voir `tests/test_shortener.py`).

### 2.3 `src/schemas.py` - schémas Pydantic

```bash
cat > src/schemas.py <<'EOF'
"""Schemas Pydantic - contrats d'entree/sortie de l'API LinkPulse."""

from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl


class LinkCreateRequest(BaseModel):
    url: HttpUrl = Field(..., description="URL longue a raccourcir")


class LinkBaseResponse(BaseModel):
    code: str
    url: str
    created_at: datetime
    clicks: int
    active: bool


class LinkResponse(LinkBaseResponse):
    short_url: str


class LinkStatsResponse(LinkBaseResponse):
    pass
EOF
```

![image](https://hackmd.io/_uploads/rydWl8BMzx.png)

**Explication du code - `src/schemas.py` :** Les schémas Pydantic jouent deux rôles simultanément. La **validation automatique** des entrées : FastAPI rejette toute requête avec une URL invalide (HTTP 422) avant même d'appeler le handler, sans écrire de code de validation manuel. La **documentation automatique** : ces classes alimentent le Swagger UI généré sur `/docs`. `HttpUrl` de Pydantic v2 valide le format de l'URL ET la normalise (ajout du `/` final), ce qui explique pourquoi `test_redirect_found` compare avec `"https://example.com/"` et non `"https://example.com"`.

### 2.4 `src/main.py` - application FastAPI

```bash
cat > src/main.py <<'EOF'
"""Point d'entree FastAPI de LinkPulse.
Expose :
- /health
- /metrics
- /api/links
- /api/links/{code}/stats
- /r/{code}
- /api/links/{code} (DELETE)
"""

import os
from time import perf_counter

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import RedirectResponse
from prometheus_client import Counter, Gauge, Histogram
from prometheus_fastapi_instrumentator import Instrumentator

from src import storage
from src.schemas import LinkCreateRequest, LinkResponse, LinkStatsResponse
from src.shortener import generate_unique_code

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")

app = FastAPI(title="LinkPulse", version="0.1.0")

storage.init_db()

# --- Metrics ---
links_created_total = Counter(
    "links_created_total",
    "Nombre total de liens courts crees",
)

redirects_total = Counter(
    "redirects_total",
    "Nombre total de tentatives de redirection",
    ["status"],
)

redirect_duration = Histogram(
    "redirect_duration_seconds",
    "Duree de traitement d'une redirection",
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5],
)

active_links_gauge = Gauge(
    "active_links_gauge",
    "Nombre de liens actifs actuellement en base",
)

Instrumentator().instrument(app).expose(app)


def _to_link_response(link: dict) -> LinkResponse:
    return LinkResponse(
        code=link["code"],
        url=link["url"],
        short_url=f"{BASE_URL}/r/{link['code']}",
        created_at=link["created_at"],
        clicks=link["clicks"],
        active=bool(link["active"]),
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/links", response_model=LinkResponse, status_code=201)
def create_link(payload: LinkCreateRequest):
    code = generate_unique_code()

    try:
        link = storage.create_link(code, str(payload.url))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erreur creation lien") from e

    links_created_total.inc()
    active_links_gauge.set(storage.count_active_links())

    return _to_link_response(link)


@app.get("/api/links", response_model=list[LinkResponse])
def get_links(skip: int = 0, limit: int = 20):
    links = storage.list_links(skip=skip, limit=limit)
    return [_to_link_response(link) for link in links]


@app.get("/api/links/{code}/stats", response_model=LinkStatsResponse)
def link_stats(code: str):
    link = storage.get_link(code)

    if not link:
        raise HTTPException(status_code=404, detail="Lien introuvable")

    return LinkStatsResponse(
        code=link["code"],
        url=link["url"],
        created_at=link["created_at"],
        clicks=link["clicks"],
        active=bool(link["active"]),
    )


@app.delete("/api/links/{code}", status_code=204)
def delete_link(code: str):
    ok = storage.deactivate_link(code)

    if not ok:
        raise HTTPException(status_code=404, detail="Lien introuvable")

    active_links_gauge.set(storage.count_active_links())
    return Response(status_code=204)


@app.get("/r/{code}")
def redirect_to_url(code: str):
    start = perf_counter()

    link = storage.get_link(code)

    if not link or not link["active"]:
        redirects_total.labels(status="not_found").inc()
        redirect_duration.observe(perf_counter() - start)

        raise HTTPException(
            status_code=404,
            detail="Lien introuvable ou desactive",
        )

    storage.increment_clicks(code)

    redirects_total.labels(status="found").inc()
    redirect_duration.observe(perf_counter() - start)

    return RedirectResponse(
        url=link["url"],
        status_code=307,
    )
EOF
```

![image](https://hackmd.io/_uploads/rkUBgLSGzx.png)

**Explication du code - `src/main.py` :** Les métriques Prometheus sont instanciées **au niveau module** (une seule fois au démarrage) pour éviter les erreurs de doublon d'enregistrement à chaque requête. `Counter` accumule des valeurs monotones croissantes (liens créés, redirections), `Gauge` représente une valeur instantanée variable (liens actifs), `Histogram` répartit les durées en buckets prédéfinis pour calculer des percentiles. `Instrumentator().instrument(app).expose(app)` ajoute en deux lignes les métriques HTTP standard par route/méthode et crée automatiquement le endpoint `GET /metrics` consommé par Prometheus. `status_code=307` (Temporary Redirect) préserve la méthode HTTP d'origine et signale aux navigateurs que la redirection peut changer.

### 2.5 Tests

```bash
cat > tests/conftest.py <<'EOF'
"""Configuration pytest : isole les tests dans leur propre base SQLite
et nettoie la table 'links' avant chaque test pour garantir l'independance
des tests entre eux.
"""
import os
os.environ["DB_PATH"] = "test_linkpulse.db"
import pytest  # noqa: E402
from src import storage  # noqa: E402
storage.init_db()
@pytest.fixture(autouse=True)
def clean_db():
    with storage.get_connection() as conn:
        conn.execute("DELETE FROM links")
        conn.commit()
    yield
EOF
```

![image](https://hackmd.io/_uploads/HkavgIHzfg.png)

**Explication du code - `tests/conftest.py` :** `conftest.py` est un fichier spécial de pytest chargé automatiquement avant les tests. `os.environ["DB_PATH"] = "test_linkpulse.db"` doit être positionné **avant** l'import de `storage` car Python exécute le module à l'import et lit `DB_PATH` à ce moment précis. La fixture `autouse=True` s'applique à chaque test sans avoir à la déclarer explicitement : chaque test repart d'une table vide, ce qui garantit leur **indépendance totale** - l'ordre d'exécution ne peut pas provoquer d'interférence.

```bash
cat > tests/test_shortener.py <<'EOF'
from src.shortener import ALPHABET, CODE_LENGTH, generate_unique_code
def test_generate_unique_code_length():
    code = generate_unique_code()
    assert len(code) == CODE_LENGTH
def test_generate_unique_code_alphabet():
    code = generate_unique_code()
    assert all(char in ALPHABET for char in code)
def test_generate_unique_code_is_random():
    codes = {generate_unique_code() for _ in range(20)}
    assert len(codes) == 20
EOF
```

![image](https://hackmd.io/_uploads/rJ0tg8HzGl.png)

**Explication du code - `tests/test_shortener.py` :** Ces trois tests unitaires vérifient le comportement de `generate_unique_code()` de façon **orthogonale** : longueur exacte, appartenance de chaque caractère à l'alphabet attendu, et entropie (20 appels successifs doivent produire 20 codes distincts - ce test échouerait si la fonction retournait toujours la même valeur). Ils sont rapides, sans dépendance réseau ni fichier, et s'exécutent même sans base de données initialisée.

```bash
cat > tests/test_api.py <<'EOF'
from fastapi.testclient import TestClient
from src.main import app
client = TestClient(app)
def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
def test_create_link():
    r = client.post("/api/links", json={"url": "https://example.com"})
    assert r.status_code == 201
    data = r.json()
    assert len(data["code"]) == 6
    assert data["clicks"] == 0
    assert data["active"] is True
    assert data["short_url"].endswith(data["code"])
def test_create_link_invalid_url_fails():
    r = client.post("/api/links", json={"url": "not-a-url"})
    assert r.status_code == 422
def test_redirect_found():
    created = client.post(
        "/api/links", json={"url": "https://example.com"}
    ).json()
    r = client.get(f"/r/{created['code']}", follow_redirects=False)
    assert r.status_code == 307
    assert r.headers["location"] == "https://example.com/"
def test_redirect_not_found():
    r = client.get("/r/doesnotexist", follow_redirects=False)
    assert r.status_code == 404
def test_stats_track_clicks():
    created = client.post(
        "/api/links", json={"url": "https://example.com"}
    ).json()
    client.get(f"/r/{created['code']}", follow_redirects=False)
    client.get(f"/r/{created['code']}", follow_redirects=False)
    stats = client.get(f"/api/links/{created['code']}/stats").json()
    assert stats["clicks"] == 2
def test_delete_link_deactivates_it():
    created = client.post(
        "/api/links", json={"url": "https://example.com"}
    ).json()
    r = client.delete(f"/api/links/{created['code']}")
    assert r.status_code == 204
    r2 = client.get(f"/r/{created['code']}", follow_redirects=False)
    assert r2.status_code == 404
def test_delete_unknown_link_returns_404():
    r = client.delete("/api/links/doesnotexist")
    assert r.status_code == 404
def test_list_links_returns_created_link():
    client.post("/api/links", json={"url": "https://example.com"})
    r = client.get("/api/links")
    assert r.status_code == 200
    assert len(r.json()) >= 1
EOF
```

![image](https://hackmd.io/_uploads/Bko3xIrMGl.png)

**Explication du code - `tests/test_api.py` :** `TestClient` de FastAPI/Starlette simule des requêtes HTTP **en mémoire** sans démarrer de serveur réel, rendant les tests très rapides (< 1 s pour 9 tests). `follow_redirects=False` dans `test_redirect_found` est essentiel : on veut vérifier que l'API retourne un 307 avec le bon header `Location`, pas que la redirection aboutit. `test_stats_track_clicks` valide le comportement **transactionnel** : deux appels à `/r/{code}` doivent se refléter en base via `/stats`. `test_delete_link_deactivates_it` vérifie que la désactivation est logique (enregistrement conservé en base, `active=0`) et non une suppression physique.

### 2.6 `requirements.txt`

```bash
cat > requirements.txt <<'EOF'
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.5.3
pytest==7.4.4
pytest-cov==4.1.0
httpx==0.26.0
prometheus-fastapi-instrumentator==6.1.0
prometheus-client==0.19.0
EOF
```

![image](https://hackmd.io/_uploads/rkoClUHzGl.png)

### 2.7 Vérification locale (avant de continuer)

```bash
# Installer python3-venv d'abord
sudo apt update && sudo apt install -y python3-venv python3-pip
# Créer et activer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate
# Installer les dépendances
pip install -r requirements.txt
# Installer flake8 dans le venv
pip install flake8
# Lancer les tests et le lint
pytest tests/ -v --cov=src --cov-report=term-missing
flake8 --max-line-length=100 src/
```

![image](https://hackmd.io/_uploads/H1lAZLrzze.png)

![image](https://hackmd.io/_uploads/ryrkfLBMfg.png)

![image](https://hackmd.io/_uploads/SJrgfISMMl.png)

![image](https://hackmd.io/_uploads/SkrmfIBGfg.png)

![image](https://hackmd.io/_uploads/HJFpGUHzMl.png)

**Résultat attendu : 12 tests verts, couverture ≈ 98%, aucune sortie de flake8.** Voir [section H](#h-exemples-de-sorties-attendues-à-chaque-étape-clé) pour un exemple exact de sortie. Ne passez pas à la suite tant que ce n'est pas le cas.

![image](https://hackmd.io/_uploads/HJtkXLBGMl.png)

### Nettoyage de l'environnement de test

```bash
# 1. Quitter l'environnement virtuel pour revenir au Python système
deactivate
# 2. Supprimer la base de données de test (force la suppression sans confirmation)
#    Permet de repartir d'une base propre lors du prochain test
rm -f test_linkpulse.db
# 3. Vérifier que la base a bien été supprimée
echo "Base de test supprimée"
```

![image](https://hackmd.io/_uploads/ryYq78HMMl.png)


---

## Phase 3 - Conteneurisation

### 3.1 `Dockerfile`

```bash
cat > Dockerfile <<'EOF'
FROM python:3.12-slim
WORKDIR /app
# curl est necessaire pour les healthchecks Docker Compose et Terraform
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
# Etape 1 : copier uniquement le fichier de dependances
# Cette couche est mise en cache tant que requirements.txt ne change pas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Etape 2 : copier le code source (invalide a chaque modification)
COPY src/ ./src/
COPY tests/ ./tests/
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
```

![image](https://hackmd.io/_uploads/rylpX8Szfx.png)

**Explication du code - `Dockerfile` :** L'ordre des instructions exploite le **cache par couche** de Docker : `COPY requirements.txt` + `pip install` forme une couche stable mise en cache tant que les dépendances ne changent pas. Seul `COPY src/` invalide le cache à chaque modification du code source, évitant de réinstaller les packages à chaque build. `python:3.12-slim` réduit la surface d'attaque (moins de packages système pré-installés) et la taille de l'image finale. `curl` est installé explicitement car il est utilisé par les healthchecks Terraform et Docker Compose. `EXPOSE 8000` est déclaratif (documentation), pas une ouverture de port effective - c'est le `-p 8001:8000` de Terraform qui publie réellement le port.

### 3.2 `.dockerignore`

```bash
cat > .dockerignore <<'EOF'
# Depot Git - inutile dans l'image
.git/
.github/
# Artefacts Python
__pycache__/
*.pyc
*.pyo
.pytest_cache/
htmlcov/
coverage.xml
# Secrets et environnements locaux
.env
.env.*
# Bases de donnees locales
linkpulse.db
test_linkpulse.db
# Terraform
*.tfstate
*.tfstate.backup
.terraform/
# Dossiers non necessaires a l'image (utilises par Jenkins/Terraform a part)
infra/
monitoring/
README.md
EOF
```

![image](https://hackmd.io/_uploads/Hk514Irzfl.png)

**Explication du code - `.dockerignore` :** Sans ce fichier, `docker build` enverrait l'intégralité du répertoire au démon Docker (incluant `.git/`, `.terraform/` et les fichiers `.db`), ralentissant le build et risquant d'embarquer des secrets ou des données locales dans l'image. Les dossiers `infra/` et `monitoring/` sont exclus car ils ne font pas partie du code applicatif - Terraform les lit directement depuis le workspace Jenkins, pas depuis l'image Docker.

### 3.3 `docker-compose.yml`

```bash
cat > docker-compose.yml <<'EOF'
version: '3.9'
services:
  linkpulse-api:
    build: .
    container_name: linkpulse-dev
    ports:
      - "8000:8000"   # hote:conteneur
    environment:
      - DB_PATH=/data/linkpulse.db
      - BASE_URL=http://localhost:8000
    volumes:
      - linkpulse-data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
volumes:
  linkpulse-data:
EOF
```

![image](https://hackmd.io/_uploads/H1GM4LSfMx.png)

**Explication du code - `docker-compose.yml` :** Ce fichier définit l'**environnement de développement local** uniquement (port `8000`, conteneur `linkpulse-dev`) - il est totalement indépendant du déploiement staging géré par Terraform (port `8001`, conteneur `linkpulse-staging`). Le `healthcheck` permet à Docker de marquer le conteneur comme `healthy` seulement quand `/health` répond avec succès. Le volume nommé `linkpulse-data` persiste la base SQLite entre les `docker compose down/up` successifs, simulant le comportement d'un volume Docker en staging.

Cet environnement (port `8000`, conteneur `linkpulse-dev`) sert uniquement au développement local. Il est totalement indépendant du déploiement de staging géré par Terraform (port `8001`, conteneur `linkpulse-staging`).

### 3.4 `.gitignore`

```bash
cat > .gitignore <<'EOF'
__pycache__/
*.pyc
*.pyo
.pytest_cache/
htmlcov/
coverage.xml
.env
.env.*
*.db
.venv/
venv/
# Terraform
.terraform/
*.tfstate
*.tfstate.backup
.terraform.lock.hcl
EOF
```

![image](https://hackmd.io/_uploads/B1XH4LBfze.png)

### 3.5 `Makefile`

```bash
cat > Makefile <<'EOF'
IMAGE_NAME = linkpulse-api
PORT       = 8000

.PHONY: build run stop test lint clean tag

build:
	docker build -t $(IMAGE_NAME):latest .

run:
	docker compose up -d

stop:
	docker compose down

# Lance les tests DANS le conteneur Docker (même environnement qu'en CI)
test:
	docker run --rm \
		-v $(PWD):/app \
		-w /app \
		$(IMAGE_NAME):latest \
		pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	docker run --rm \
		-v $(PWD):/app \
		-w /app \
		python:3.12-slim \
		sh -c "pip install flake8 -q && flake8 src/ --max-line-length=100"

clean:
	docker compose down -v
	docker rmi $(IMAGE_NAME):latest || true

tag:
	git tag -a v0.1.0 -m "Premiere version LinkPulse"
	git push origin v0.1.0
EOF

```

![image](https://hackmd.io/_uploads/H1wP4IBzMl.png)

**Explication du code - `Makefile` :** Le Makefile standardise les commandes du projet : tout développeur tape `make test` sans mémoriser la commande `docker run` exacte. La cible `test` monte le répertoire courant comme volume (`-v $(PWD):/app`) pour exécuter pytest **dans le même environnement que la CI**, éliminant les divergences "ça marche chez moi". La cible `lint` utilise l'image officielle `python:3.12-slim` sans construire l'image applicative, accélérant la vérification. **Important :** les recettes Makefile doivent commencer par une **tabulation** (pas des espaces) - c'est une contrainte historique de `make`.

**Attention :** si vous recopiez ce bloc à la main plutôt que via `cat <<'EOF'`, vérifiez que les lignes sous `build:`, `run:`, etc. commencent par une **tabulation**, pas des espaces.

### 3.6 Build, test et premier commit

```bash
make build
make test
make lint
find . -not -path './.git/*' | sort
git add .
git diff --staged --stat
git commit -m "feat: initialiser la structure LinkPulse v0.1"
git push origin main
make tag
git tag -l
```

![image](https://hackmd.io/_uploads/BkA6EUrGMx.png)

![image](https://hackmd.io/_uploads/HkiJHLrfze.png)

![image](https://hackmd.io/_uploads/Hkp4BUrMfl.png)

![image](https://hackmd.io/_uploads/rywLHIBfGl.png)

![image](https://hackmd.io/_uploads/rJ5dS8Bfze.png)

![image](https://hackmd.io/_uploads/rJUiHLrfMg.png)

![image](https://hackmd.io/_uploads/rJGAB8HzMg.png)


---


## Phase 4 - Jenkins

### 4.1 Lancer Jenkins, directement connecté à `cicd-network`

```bash
# Créer un volume Docker nommé "jenkins-data" pour persister les données de Jenkins
# Les données seront conservées même si le conteneur est supprimé
docker volume create jenkins-data
# Vérifier que le volume a été créé
docker volume ls
# Inspecter le volume pour voir son emplacement sur l'hôte
docker volume inspect jenkins-data
# Démarrer Jenkins en mode détaché (-d) avec :
#   - --name jenkins : Nom du conteneur
#   - --network cicd-network : Réseau Docker pour la communication avec d'autres services
#   - -p 8080:8080 : Port HTTP pour l'interface web (hôte:conteneur)
#   - -p 50000:50000 : Port pour les agents Jenkins (hôte:conteneur)
#   - -v jenkins-data:/var/jenkins_home : Montage du volume pour persister les données
#   - -v /var/run/docker.sock:/var/run/docker.sock : Permet à Jenkins de contrôler Docker sur l'hôte
#   - jenkins/jenkins:lts : Image officielle Jenkins LTS (Long Term Support)
docker run -d \
  --name jenkins \
  --network cicd-network \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins-data:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
# Vérifier que le conteneur est en cours d'exécution
docker ps | grep jenkins
# Afficher les logs en temps réel pour suivre le démarrage de Jenkins
# Utile pour récupérer le mot de passe initial d'administration
docker logs -f jenkins
# Attendre que Jenkins soit complètement démarré
# Rechercher dans les logs la ligne : "Jenkins is fully up and running"
# Ce message indique que Jenkins est prêt à être utilisé
```

![image](https://hackmd.io/_uploads/SyKT8LSGMe.png)

![image](https://hackmd.io/_uploads/ryHXvIrGzx.png)

![image](https://hackmd.io/_uploads/S1rUvLrfzl.png)

![image](https://hackmd.io/_uploads/rkCPPUBGzx.png)

**Explication du code :** `--network cicd-network` connecte Jenkins au réseau partagé **dès sa création**, lui permettant d'atteindre `sonarqube:9000` et les conteneurs déployés par Terraform via leur nom de service. `-v /var/run/docker.sock:/var/run/docker.sock` est la clé du **DooD (Docker-out-of-Docker)** : Jenkins contrôle le démon Docker de l'hôte en partageant son socket Unix, sans faire tourner son propre démon interne. `-v jenkins-data:/var/jenkins_home` persiste la configuration Jenkins, les plugins et les credentials entre les redémarrages du conteneur.

```bash
docker inspect jenkins --format '{{json .NetworkSettings.Networks}}' | python3 -m json.tool
# Doit afficher une cle "cicd-network"
```

![image](https://hackmd.io/_uploads/BkWovIrzfx.png)

### 4.2 Donner à Jenkins l'accès au démon Docker de l'hôte (DooD)

```bash
docker exec -u root jenkins bash -c "apt-get update -q && apt-get install -y docker.io"
docker exec -u root jenkins chmod 666 /var/run/docker.sock
docker exec -u jenkins jenkins docker ps
```

![image](https://hackmd.io/_uploads/Sknzu8SfMe.png)

![image](https://hackmd.io/_uploads/BydE_USfGe.png)

![image](https://hackmd.io/_uploads/H1w9KIBzGg.png)

**Explication du code :** `apt-get install docker.io` installe uniquement le **client** Docker (la commande `docker`) dans le conteneur Jenkins - pas un second démon. `chmod 666 /var/run/docker.sock` accorde à l'utilisateur `jenkins` (non-root) l'accès au socket Unix partagé depuis l'hôte. La commande de vérification `docker exec -u jenkins jenkins docker ps` confirme que Jenkins peut effectivement lister les conteneurs de l'hôte - c'est le test minimal fonctionnel du DooD.

### 4.3 Installer Terraform DANS le conteneur Jenkins

```bash
docker exec -u root jenkins bash -c "
  apt-get update -q &&
  apt-get install -y wget unzip curl &&
  wget https://releases.hashicorp.com/terraform/1.7.0/terraform_1.7.0_linux_amd64.zip &&
  unzip terraform_1.7.0_linux_amd64.zip &&
  mv terraform /usr/local/bin/ &&
  terraform version
"
docker exec jenkins terraform version
```

![image](https://hackmd.io/_uploads/S1zv5LSfGx.png)

![image](https://hackmd.io/_uploads/rkPOqLBfMg.png)

**Explication du code :** Terraform est installé **à l'intérieur du conteneur Jenkins** (pas sur l'hôte) car c'est Jenkins qui exécutera `terraform apply` dans le pipeline. Le binaire est placé dans `/usr/local/bin/` pour être dans le `PATH` sans configuration supplémentaire. La version est fixée à `1.7.0` pour garantir la reproductibilité des builds - une mise à jour involontaire de Terraform ne cassera pas le pipeline.

### 4.4 Première configuration de l'interface Jenkins

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

![image](https://hackmd.io/_uploads/Skis5LBGMl.png)

1\. Ouvrez `http://<IP_VM>:8080`, collez le mot de passe.

2\. **Install suggested plugins**.

3\. Créez votre compte administrateur.

4\. **Save and Finish → Start using Jenkins**.

![image](https://hackmd.io/_uploads/BysQiUBfGg.png)

![image](https://hackmd.io/_uploads/r1lSsUHfze.png)

![image](https://hackmd.io/_uploads/rkRroUBGGx.png)

![image](https://hackmd.io/_uploads/ryKniLHGMg.png)

![image](https://hackmd.io/_uploads/rk4ao8rfGg.png)

![image](https://hackmd.io/_uploads/SyNAiUBGMe.png)

![image](https://hackmd.io/_uploads/B1Gg2IHMMe.png)

### 4.5 Installer les plugins additionnels

`Administrer Jenkins → Plugins → Available plugins` : `Docker Pipeline`, `Git`, `Pipeline`, `SonarQube Scanner`, `Blue Ocean`.

```bash
# Installer le plugin Docker Pipeline
docker exec jenkins sh -c "jenkins-plugin-cli --plugins docker-workflow"
# Installer le plugin SonarQube Scanner
docker exec jenkins sh -c "jenkins-plugin-cli --plugins sonar"
# Installer le plugin Git
docker exec jenkins sh -c "jenkins-plugin-cli --plugins git"
# Installer Blue Ocean pour une interface moderne
docker exec jenkins sh -c "jenkins-plugin-cli --plugins blueocean"
# Installer l'intégration GitHub
docker exec jenkins sh -c "jenkins-plugin-cli --plugins github"
# Installer le plugin Slack pour les notifications
docker exec jenkins sh -c "jenkins-plugin-cli --plugins slack"
# Installer les étapes Docker
docker exec jenkins sh -c "jenkins-plugin-cli --plugins docker-build-step"
# Redémarrer Jenkins après l'installation de chaque plugin
docker restart jenkins
# Créer une fonction pour vérifier un plugin
check_plugin() {
    local name=$1
    local file=$2
    if docker exec jenkins sh -c "ls /var/jenkins_home/plugins/$file 2>/dev/null" > /dev/null; then
        echo " $name : Installé"
    else
        echo " $name : Non installé"
    fi
}
# Vérifier tous les plugins
echo "=== VÉRIFICATION DES PLUGINS JENKINS ==="
echo "----------------------------------------"
check_plugin "Docker Pipeline" "docker-workflow.jpi"
check_plugin "SonarQube Scanner" "sonar.jpi"
check_plugin "Git" "git.jpi"
check_plugin "Pipeline" "workflow-aggregator.jpi"
check_plugin "Blue Ocean" "blueocean.jpi"
check_plugin "GitHub" "github.jpi"
check_plugin "Slack" "slack.jpi"
check_plugin "Docker Build Step" "docker-build-step.jpi"
echo "----------------------------------------"
echo "Total plugins installés :"
docker exec jenkins ls /var/jenkins_home/plugins/ | wc -l
```

![image](https://hackmd.io/_uploads/BJNNpUHMGx.png)

![image](https://hackmd.io/_uploads/B168RLBfzx.png)

### 4.6 Credentials Jenkins

Créez un token GitHub (`repo`, `read:packages`, `write:packages`), puis :

`Jenkins → Administrer Jenkins → Credentials → System → Global credentials → Add Credentials` :

| ID | Type | Contenu |
|---|---|---|
| `github-token` | Username with password | Pseudo GitHub + token |
| `sonar-token` | Secret text | Créé en Phase 5 |

![image](https://hackmd.io/_uploads/r1lc0UHGzx.png)

![image](https://hackmd.io/_uploads/SJzj0ISMfg.png)

![image](https://hackmd.io/_uploads/Bkm3C8Bfzg.png)

![image](https://hackmd.io/_uploads/HJeX1vHGMg.png)

![image](https://hackmd.io/_uploads/HygNkPHMfg.png)




---

## Phase 5 - SonarQube

### 5.1 Lancer SonarQube, directement connecté à `cicd-network`

```bash
sudo sysctl -w vm.max_map_count=262144
docker run -d \
  --name sonarqube \
  --network cicd-network \
  -p 9000:9000 \
  sonarqube:lts-community
docker logs -f sonarqube | grep 'SonarQube is operational'
```

![image](https://hackmd.io/_uploads/Hk7v1vrzfe.png)

![image](https://hackmd.io/_uploads/Hkpo1PHfzl.png)

![image](https://hackmd.io/_uploads/BJHp1wrGMx.png)

### 5.2 Créer le projet et le token d'analyse

`http://<IP_VM>:9000` → `admin`/`admin` (changez le mot de passe).

![image](https://hackmd.io/_uploads/rkolgvBGfl.png)

![image](https://hackmd.io/_uploads/rk7feDSzGg.png)

![image](https://hackmd.io/_uploads/SkVSgwBffg.png)

![image](https://hackmd.io/_uploads/HkxxbwHfGx.png)

1\. **Create Project** manuellement : `LinkPulse` / `linkpulse-api` / branche `main`.

2\. Méthode d'analyse : **With Jenkins**.

3\. `My Account → Security → Generate Token` : `jenkins-token`, type `Global Analysis Token`.

![image](https://hackmd.io/_uploads/rJ_PgwHzMg.png)

![image](https://hackmd.io/_uploads/H1DtevHGzx.png)

![image](https://hackmd.io/_uploads/SJ2agvrfzx.png)

![image](https://hackmd.io/_uploads/S13ZZPBfGx.png)

![image](https://hackmd.io/_uploads/r1EJfwSzGg.png)

### 5.3 Quality Gate dédiée `LinkPulse-Gate`

| Condition | Seuil |
|---|---|
| Coverage (Overall Code) | ≥ 75 % |
| Reliability Rating | A |
| Security Rating | A |
| Duplicated Lines (%) | < 3 % |

`LinkPulse → Project Settings → Quality Gate → LinkPulse-Gate`.

### 5.4 Enregistrer le token SonarQube dans Jenkins (`sonar-token`, Secret text)

![image](https://hackmd.io/_uploads/HyJlQDrMzg.png)

![image](https://hackmd.io/_uploads/BJzZXvrffl.png)

![image](https://hackmd.io/_uploads/HkjN7PHMzl.png)

### 5.5 Déclarer le serveur SonarQube dans Jenkins

```
Jenkins → Administrer Jenkins → System → SonarQube servers
→ Add SonarQube : Name = sonarqube | URL = http://sonarqube:9000
→ Server authentication token : sonar-token
```

![image](https://hackmd.io/_uploads/Sy1_MvBzGl.png)

![image](https://hackmd.io/_uploads/HkvK7vHGzl.png)

### 5.6 Webhook SonarQube → Jenkins

```
SonarQube → Administration → Configuration → Webhooks → Create
→ Name = jenkins
→ URL  = http://jenkins:8080/sonarqube-webhook/
```

![image](https://hackmd.io/_uploads/Syl6QPrGzx.png)

![image](https://hackmd.io/_uploads/SyilVDBGfl.png)

> **Le `/` final est obligatoire.**

### 5.7 Trivy - aucune installation requise

Le stage `7. Security Scan (Trivy)` du Jenkinsfile lance directement `aquasec/trivy:latest` via `docker run`.

---

## Phase 8 - Jenkinsfile, job Jenkins et webhook GitHub

- Création du fichier 

```bash
nano Jenkinsfile
```

- Fichier Jenkinsfile

```bash
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
          HOST_IP="4.223.169.52"
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
```

![image](https://hackmd.io/_uploads/r1yeHd9Mfg.png)


Remplacez les deux occurrences de `VOTRE_PSEUDO` (variable `REGISTRY`).

### 8.2 Créer le job Jenkins

`Jenkins → Nouveau Item → linkpulse-pipeline → Pipeline → OK`

| Section | Champ | Valeur |
|---|---|---|
| General | GitHub project | `https://github.com/VOTRE_PSEUDO/linkpulse-api` |
| Build Triggers | - | `GitHub hook trigger for GITScm polling` |
| Pipeline | Definition | `Pipeline script from SCM` |
| Pipeline | SCM | `Git` |
| Pipeline | Repository URL | `https://github.com/VOTRE_PSEUDO/linkpulse-api.git` |
| Pipeline | Credentials | `github-token` |
| Pipeline | Branch | `*/main` |
| Pipeline | Script Path | `Jenkinsfile` |

![image](https://hackmd.io/_uploads/ryQZPwrffe.png)

![image](https://hackmd.io/_uploads/HkADwvSGMe.png)

![image](https://hackmd.io/_uploads/HyejvvHMGl.png)

![image](https://hackmd.io/_uploads/ryB2DwSMMl.png)

![image](https://hackmd.io/_uploads/HyvCvPHzfl.png)

![image](https://hackmd.io/_uploads/S1ze_wrMze.png)

![image](https://hackmd.io/_uploads/B1cWuvHMzg.png)

### 8.3 Exposer Jenkins vers Internet

```bash
ngrok config add-authtoken VOTRE_TOKEN_NGROK
nohup ngrok http 8080 --log=stdout --log-level=info > ngrok.log 2>&1 &
sleep 3
curl -s http://localhost:4040/api/tunnels | python3 -c \
  "import sys,json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])"
```

![image](https://hackmd.io/_uploads/ByraBucffg.png)

- Tester le lein de connexion via le navigateur
![image](https://hackmd.io/_uploads/rkRZ8O9fMx.png)
![image](https://hackmd.io/_uploads/rJ8NUu5GMl.png)
![image](https://hackmd.io/_uploads/r1uUI_qzfg.png)


### 8.4 Webhook GitHub → Jenkins

`https://github.com/VOTRE_PSEUDO/linkpulse-api/settings/hooks → Add webhook`

| Champ | Valeur |
|---|---|
| Payload URL | `https://VOTRE_URL_JENKINS/github-webhook/` |
| Content type | `application/json` |
| Which events | Just the push event |

![image](https://hackmd.io/_uploads/H1xVFId9GGx.png)

![image](https://hackmd.io/_uploads/r1WnLucfze.png)
![image](https://hackmd.io/_uploads/BkahU_5zMx.png)
![image](https://hackmd.io/_uploads/rJYAIucfGl.png)



---


## Phase 9 - Dashboard Grafana as Code

### Concept

Au lieu de configurer le dashboard Grafana manuellement via l'interface web, tout est décrit dans des fichiers JSON versionnés. Terraform monte ces fichiers dans le conteneur Grafana au démarrage : le dashboard apparaît automatiquement, sans aucun clic.

**Avantage clé :** si le conteneur Grafana est recréé (nouveau `terraform apply`), le dashboard est restauré instantanément sans intervention humaine.

### Structure des fichiers ajoutés

```
monitoring/
└── grafana/
    ├── provisioning/
    │   ├── datasources/
    │   │   └── prometheus.yml      ← connexion automatique à Prometheus
    │   └── dashboards/
    │       └── linkpulse.yml       ← déclaration du dossier de dashboards
    └── dashboards/
        └── linkpulse.json          ← dashboard complet avec 6 panels
```

```bash
mkdir -p monitoring/grafana/provisioning/datasources
mkdir -p monitoring/grafana/provisioning/dashboards
mkdir -p monitoring/grafana/dashboards
```
![image](https://hackmd.io/_uploads/SybD_u5zMx.png)


#### `monitoring/grafana/provisioning/datasources/prometheus.yml`

```bash
cat > monitoring/grafana/provisioning/datasources/prometheus.yml <<'EOF'
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: false
EOF
```
![image](https://hackmd.io/_uploads/SyIdu_9Mze.png)


#### `monitoring/grafana/provisioning/dashboards/linkpulse.yml`

```bash
cat > monitoring/grafana/provisioning/dashboards/linkpulse.yml <<'EOF'
apiVersion: 1
providers:
  - name: LinkPulse
    folder: LinkPulse
    type: file
    disableDeletion: true
    updateIntervalSeconds: 30
    options:
      path: /var/lib/grafana/dashboards
EOF
```
![image](https://hackmd.io/_uploads/SkXtu_qzGl.png)


#### `monitoring/grafana/dashboards/linkpulse.json`

```bash
cat > monitoring/grafana/dashboards/linkpulse.json <<'EOF'
{
  "title": "LinkPulse — Overview",
  "uid": "linkpulse-overview",
  "timezone": "browser",
  "refresh": "30s",
  "panels": [
    {
      "id": 1, "title": "Liens actifs", "type": "stat",
      "gridPos": {"x": 0, "y": 0, "w": 6, "h": 4},
      "targets": [{"datasource": "Prometheus", "expr": "active_links_gauge"}]
    },
    {
      "id": 2, "title": "Liens créés (total)", "type": "stat",
      "gridPos": {"x": 6, "y": 0, "w": 6, "h": 4},
      "targets": [{"datasource": "Prometheus", "expr": "links_created_total"}]
    },
    {
      "id": 3, "title": "Redirections / seconde", "type": "timeseries",
      "gridPos": {"x": 0, "y": 4, "w": 12, "h": 8},
      "targets": [
        {"datasource": "Prometheus", "expr": "rate(redirects_total{status=\"found\"}[1m])",     "legendFormat": "Trouvés"},
        {"datasource": "Prometheus", "expr": "rate(redirects_total{status=\"not_found\"}[1m])", "legendFormat": "404"}
      ]
    },
    {
      "id": 4, "title": "Latence redirection p99 (ms)", "type": "timeseries",
      "gridPos": {"x": 0, "y": 12, "w": 12, "h": 8},
      "targets": [{"datasource": "Prometheus",
        "expr": "histogram_quantile(0.99, rate(redirect_duration_seconds_bucket[5m])) * 1000",
        "legendFormat": "p99"}]
    },
    {
      "id": 5, "title": "Taux de liens introuvables (%)", "type": "gauge",
      "gridPos": {"x": 12, "y": 0, "w": 6, "h": 8},
      "targets": [{"datasource": "Prometheus",
        "expr": "rate(redirects_total{status=\"not_found\"}[5m]) / rate(redirects_total[5m]) * 100"}],
      "options": {"thresholds": {"steps": [
        {"color": "green", "value": 0},
        {"color": "yellow", "value": 5},
        {"color": "red", "value": 10}
      ]}}
    },
    {
      "id": 6, "title": "API up/down", "type": "stat",
      "gridPos": {"x": 18, "y": 0, "w": 6, "h": 4},
      "targets": [{"datasource": "Prometheus", "expr": "up{job=\"linkpulse-api\"}"}]
    }
  ]
}
EOF
```
![image](https://hackmd.io/_uploads/S1jq_dczMx.png)


### Mise à jour de `infra/monitoring.tf`

Remplacer le bloc `docker_container.grafana` existant :

```bash
cat <<'EOF' > infra/monitoring.tf
# infra/monitoring.tf

resource "docker_image" "prometheus" {
  name         = "prom/prometheus:latest"
  keep_locally = true
}

resource "docker_container" "prometheus" {
  name    = "prometheus"
  image   = docker_image.prometheus.image_id
  restart = "unless-stopped"

  networks_advanced {
    name = data.docker_network.cicd.name
  }

  ports {
    internal = 9090
    external = 9090
  }

  volumes {
    host_path      = "/home/labadmin/linkpulse-api/monitoring/prometheus.yml"
    container_path = "/etc/prometheus/prometheus.yml"
    read_only      = true
  }

  volumes {
    host_path      = "/home/labadmin/linkpulse-api/monitoring/alerts.yml"
    container_path = "/etc/prometheus/alerts.yml"
    read_only      = true
  }

  command = [
    "--config.file=/etc/prometheus/prometheus.yml",
    "--storage.tsdb.retention.time=15d"
  ]

  depends_on = [docker_container.linkpulse_staging]
}

resource "docker_image" "grafana" {
  name         = "grafana/grafana:latest"
  keep_locally = true
}

resource "docker_container" "grafana" {
  name    = "grafana"
  image   = docker_image.grafana.image_id
  restart = "unless-stopped"

  networks_advanced {
    name = data.docker_network.cicd.name
  }

  ports {
    internal = 3000
    external = 3000
  }

  env = [
    "GF_SECURITY_ADMIN_PASSWORD=admin",
    "GF_PATHS_PROVISIONING=/etc/grafana/provisioning"
  ]

  volumes {
    host_path      = "/home/labadmin/linkpulse-api/monitoring/grafana/provisioning/datasources"
    container_path = "/etc/grafana/provisioning/datasources"
    read_only      = true
  }

  volumes {
    host_path      = "/home/labadmin/linkpulse-api/monitoring/grafana/provisioning/dashboards"
    container_path = "/etc/grafana/provisioning/dashboards"
    read_only      = true
  }

  volumes {
    host_path      = "/home/labadmin/linkpulse-api/monitoring/grafana/dashboards"
    container_path = "/var/lib/grafana/dashboards"
    read_only      = true
  }

  depends_on = [docker_container.prometheus]
}
EOF
```
![image](https://hackmd.io/_uploads/rk82uOcGGg.png)


### Panels du dashboard

| Panel | Type | Requête PromQL |
|---|---|---|
| Liens actifs | Stat | `active_links_gauge` |
| Liens créés (total) | Stat | `links_created_total` |
| Redirections / seconde | Time series | `rate(redirects_total[1m])` par statut |
| Latence p99 (ms) | Time series | `histogram_quantile(0.99, rate(redirect_duration_seconds_bucket[5m])) * 1000` |
| Taux liens introuvables (%) | Gauge | `rate(redirects_total{status="not_found"}[5m]) / rate(redirects_total[5m]) * 100` |
| API up/down | Stat | `up{job="linkpulse-api"}` |


---


## Phase 10 - Notifications Slack

### Concept

À chaque fin de pipeline, Jenkins envoie automatiquement un message coloré dans un canal Slack :
- **Vert** avec l'image publiée si le pipeline réussit
- **Rouge** avec le lien vers les logs si le pipeline échoue

Aucun plugin Jenkins supplémentaire n'est nécessaire — tout passe par un simple `curl` vers un Incoming Webhook Slack.

### Mise en place

#### 1.1 Créer l'application Slack et le webhook

1. Aller sur `https://api.slack.com/apps` → **Create New App → From scratch**
2. Nom : `LinkPulse CI` → sélectionner votre workspace
3. **Incoming Webhooks → Activate Incoming Webhooks → ON**
4. **Add New Webhook to Workspace** → choisir le canal `#linkpulse-pipeline` → **Allow**
5. Copier l'URL générée : `https://hooks.slack.com/services/XXX/YYY/ZZZ`

![image](https://hackmd.io/_uploads/rJj95_qMGe.png)
![image](https://hackmd.io/_uploads/S1dkj_cfMx.png)
![image](https://hackmd.io/_uploads/HJWWjO5MMg.png)
![image](https://hackmd.io/_uploads/rJ8midcMfe.png)



#### 1.2 Enregistrer le secret dans Jenkins

```
Jenkins → Administrer Jenkins → Credentials → System → Global credentials
→ Add Credentials
  Type    : Secret text
  ID      : slack-webhook-url
  Secret  : https://hooks.slack.com/services/XXX/YYY/ZZZ
```

![image](https://hackmd.io/_uploads/rkoPid9GGe.png)


### Vérification

```bash
curl -X POST \
-H "Content-type: application/json" \
--data '{"text":"Test Jenkins vers Slack"}' \
"URL_Slack_Canal"
```
![image](https://hackmd.io/_uploads/BkCynO5Mzg.png)


---

## Phase 11 - Pre-commit hooks

### Concept

Les hooks bloquent le `git commit` local si le code ne respecte pas les règles de qualité, **avant même que le code n'atteigne Jenkins**. Principe Fail Fast poussé jusqu'au poste du développeur.

### Installation

```bash
cat > .pre-commit-config.yaml <<'EOF'
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-merge-conflict
EOF

```

![image](https://hackmd.io/_uploads/HkFGhuqzMg.png)

- Ajouter aussi la config Ruff dans pyproject.toml à la racine :

```bash
cat >> pyproject.toml <<'EOF'
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
  "E", "W",
  "F",
  "I",
  "S",
  "B",
  "UP",
]

ignore = [
  "S101",
]

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101", "S106"]
EOF
```

![image](https://hackmd.io/_uploads/Syj72O9GGl.png)


### Ce que chaque hook vérifie

| Hook | Rôle |
|---|---|
| `black` | Formatage automatique du code Python |
| `flake8` | Style PEP8 et erreurs syntaxiques |
| `isort` | Ordre des imports Python |
| `bandit` | Détection de failles de sécurité dans le code |
| `trailing-whitespace` | Espaces en fin de ligne |
| `check-yaml` | Syntaxe des fichiers YAML valide |

- installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install pre-commit ruff
pre-commit install
pre-commit run --all-files
```
![image](https://hackmd.io/_uploads/S1Ywhu5zGe.png)
![image](https://hackmd.io/_uploads/B1KKndqGMx.png)

- Vérification
![image](https://hackmd.io/_uploads/H1Dgpd9ffe.png)


---

## Phase 13 - SBOM avec Trivy

### Concept

Un **SBOM (Software Bill of Materials)** est l'inventaire complet de toutes les dépendances embarquées dans l'image Docker (bibliothèques Python, paquets Debian, etc.), avec leur version et leurs CVE connues. Archivé dans Jenkins à chaque build, il crée une traçabilité complète de la supply chain logicielle.

Son stage a été rajouté dans le Jenkinsfile.


### Phase 14 : Faire un push

Dans cette partie, nous allons déclencher un pipeline afin de vérifier tout.

```bash
git status
git add .
git commit -m "test: declenchement du pipeline complet"
git push origin main
```
![image](https://hackmd.io/_uploads/S1_cad9ffl.png)
![image](https://hackmd.io/_uploads/rJcnau9MMg.png)

dans cette dernière capture, on voit bien qu'il y a une vérification du code avant le push.

- Vérification du build 
![image](https://hackmd.io/_uploads/BJdb9FcMze.png)
![image](https://hackmd.io/_uploads/SJor5F9fGe.png)

- Vérification dans slack
Dans slack on a reçu un u message : build réuissi/
![image](https://hackmd.io/_uploads/SkCYct9GGx.png)

- Voir le Webhook GitHub
![image](https://hackmd.io/_uploads/rypict5MGe.png)

- Vérification dans SonarQube
![image](https://hackmd.io/_uploads/ByzJjYqfGg.png)
![image](https://hackmd.io/_uploads/HJVeoYqfGl.png)
![image](https://hackmd.io/_uploads/BkQfjY5zMx.png)

- Quality Gate
![image](https://hackmd.io/_uploads/SJS-m9qffx.png)



### Phase 14 : Gestion et création des liens 

-  créer 30 URLs avec des données variées

```bash
# Créer le fichier avec nano
nano lien.sh
```

- Insérer le contenu suivant dans ce fichier

```bash
#!/bin/bash

echo "Création de 30 liens raccourcis..."
echo ""

urls=(
  "https://pulsemetrics.io/produit-analytics"
  "https://pulsemetrics.io/produit-monitoring"
  "https://pulsemetrics.io/produit-alerts"
  "https://pulsemetrics.io/produit-dashboard"
  "https://pulsemetrics.io/produit-reports"
  "https://pulsemetrics.io/produit-api"
  "https://pulsemetrics.io/produit-mobile"
  "https://pulsemetrics.io/produit-cloud"
  "https://pulsemetrics.io/produit-enterprise"
  "https://pulsemetrics.io/produit-startup"
  "https://pulsemetrics.io/landing-produit"
  "https://pulsemetrics.io/landing-startup"
  "https://pulsemetrics.io/landing-enterprise"
  "https://pulsemetrics.io/landing-education"
  "https://pulsemetrics.io/landing-nonprofit"
  "https://pulsemetrics.io/promo-ete-2026"
  "https://pulsemetrics.io/promo-hiver-2026"
  "https://pulsemetrics.io/promo-printemps-2026"
  "https://pulsemetrics.io/promo-automne-2026"
  "https://pulsemetrics.io/promo-black-friday"
  "https://pulsemetrics.io/blog/guide-analytics"
  "https://pulsemetrics.io/blog/tutoriel-api"
  "https://pulsemetrics.io/blog/cas-client"
  "https://pulsemetrics.io/blog/meilleures-pratiques"
  "https://pulsemetrics.io/blog/securite-donnees"
  "https://pulsemetrics.io/newsletter-juin"
  "https://pulsemetrics.io/newsletter-juillet"
  "https://pulsemetrics.io/newsletter-aout"
  "https://pulsemetrics.io/newsletter-septembre"
  "https://pulsemetrics.io/newsletter-octobre"
)

count=1
success=0
failed=0

for url in "${urls[@]}"; do
  echo "[$count/30] $url"

  response=$(curl -s -X POST http://localhost:8001/api/links \
    -H "Content-Type: application/json" \
    -d "{\"url\": \"$url\"}")

  if echo "$response" | grep -q '"code"'; then
    code=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['code'])" 2>/dev/null)
    short_url="http://localhost:8001/r/$code"
    echo "  $short_url"
    ((success++))
  else
    echo "   Échec"
    echo "  Réponse: $response"
    ((failed++))
  fi

  echo "---"
  ((count++))
  sleep 0.1
done

echo ""
echo " RÉSULTATS :"
echo "   Succès : $success/30"
echo "   Échecs : $failed/30"
echo ""
echo " Terminé !"
```

![image](https://hackmd.io/_uploads/SkcmDdqMMe.png)

- Rendre le script exécutable

```bash
chmod +x lien.sh
```

- Lancer le fichier

```bash
./lien.sh
```

![image](https://hackmd.io/_uploads/Bk3IsFczGe.png)


### Vérification dans Prometheus

- Se connecter à l'interface

![image](https://hackmd.io/_uploads/H1RghK5MMl.png)


-  Vérifier que le service est UP

```promql
up{job="linkpulse-api"}
```

![image](https://hackmd.io/_uploads/B1OJ7YBzMx.png)

![image](https://hackmd.io/_uploads/SJ2SXYSMfg.png)

-  Nombre total de liens créés

```pormql
links_created_total
```

![image](https://hackmd.io/_uploads/SJMF7KHGzx.png)
![image](https://hackmd.io/_uploads/HyP32F5fMx.png)


-  Taux de création de liens (par minute)

```promql
rate(links_created_total[1m])
```

![image](https://hackmd.io/_uploads/H1HpXtBGfg.png)

-  Nombre total de clics

Générer des clics

```bash
cat > generate_clicks.sh <<'EOF'
#!/bin/bash

echo "Génération de clics..."
echo ""

# Récupérer tous les codes
links=$(curl -s http://localhost:8001/api/links | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('\n'.join([item['code'] for item in data]))
" 2>/dev/null)

if [ -z "$links" ]; then
    echo "Aucun lien trouvé"
    echo "Exécutez d'abord : ./lien.sh"
    exit 1
fi

total_links=$(echo "$links" | wc -l)

echo "$total_links liens trouvés"
echo ""

for i in $(seq 1 50); do
    code=$(echo "$links" | shuf -n 1)

    echo "[$i/50] Clic sur $code"

    curl -s -o /dev/null "http://localhost:8001/r/$code"

    sleep 0.3
done

echo ""
echo "50 clics générés !"
echo ""
echo "Vérifiez dans Prometheus :"
echo "   http://localhost:9090"
echo "   Requête : redirects_total{status=\"found\"}"
EOF
```

![image](https://hackmd.io/_uploads/r1nNnF9Gfg.png)


```bash
chmod +x generate_clicks.sh
```

```bash
./generate_clicks.sh
```

![image](https://hackmd.io/_uploads/S1h0DFHzfl.png)

```promql
# Pour les clics réussis
redirects_total{status="found"}
# Pour les clics sur liens inexistants
redirects_total{status="not_found"}
# Total de tous les clics
sum(redirects_total)
```

![image](https://hackmd.io/_uploads/H1QrdKHMfe.png)

![image](https://hackmd.io/_uploads/Sy7vdYHfzl.png)

![image](https://hackmd.io/_uploads/ByhOutrGfe.png)

-  Liens actifs

```promql
active_links_gauge
```

![image](https://hackmd.io/_uploads/rJnlFtBzfg.png)


---


### Interface Grafana

- Se connecter 
![image](https://hackmd.io/_uploads/rkUx6YcfGx.png)
![image](https://hackmd.io/_uploads/SknW6F9Gzg.png)

- Voir le dossier du Dashboard + Panel
![image](https://hackmd.io/_uploads/r1KETtqMMx.png)

- Tableau de bord
![image](https://hackmd.io/_uploads/SyFWecqzfe.png)


- Panel 
![image](https://hackmd.io/_uploads/HJHTCt5Gfg.png)
![image](https://hackmd.io/_uploads/SyHky5cGMe.png)
![image](https://hackmd.io/_uploads/H1ZG1cqfGg.png)
![image](https://hackmd.io/_uploads/HyrSy55zMg.png)
![image](https://hackmd.io/_uploads/rkr_J99zzx.png)
![image](https://hackmd.io/_uploads/Bk-gg59zzg.png)


### Consulter le SBOM

```bash
# 2. Générer le SBOM localement
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$(pwd)":/output \
  aquasec/trivy:latest image \
  --format cyclonedx \
  --output /output/sbom.json \
  linkpulse-api:latest

# 3. Analyser le SBOM
python3 -c "
import json
with open('sbom.json') as f:
    data = json.load(f)
    components = data.get('components', [])
    print(f' Composants inventoriés : {len(components)}')
    
    # Statistiques par type
    types = {}
    for c in components:
        ctype = c.get('type', 'unknown')
        types[ctype] = types.get(ctype, 0) + 1
    
    print('\n Types de composants:')
    for t, count in types.items():
        print(f'  - {t}: {count}')
    
    print('\n Top 10 composants:')
    for c in components[:10]:
        name = c.get('name', 'N/A')
        version = c.get('version', 'N/A')
        print(f'  - {name} {version}')
"
```
![image](https://hackmd.io/_uploads/HJj_Rt9fMg.png)

---

## Phase 14 - Déploiement Portainer

### Se connecter à Portainer

![image](https://hackmd.io/_uploads/H1EPb9BMfe.png)

![image](https://hackmd.io/_uploads/ByMBW59zzx.png)
![image](https://hackmd.io/_uploads/Bk3Hf5cfzg.png)


Pour trouver le setup token; voici la commande :

```bash
docker logs portainer 2>&1 | grep -i token
```
![image](https://hackmd.io/_uploads/S1jwZqcGfx.png)

![image](https://hackmd.io/_uploads/SJXMGcHGMl.png)


- Voir les conteneurs 
![image](https://hackmd.io/_uploads/By65-c9zze.png)
- Voir les images
![image](https://hackmd.io/_uploads/r1dhb5cMGg.png)
- Voir le réseau
![image](https://hackmd.io/_uploads/Hkm0Wcqzfl.png)
- Voir les conteneurs connectés à ce réseau
![image](https://hackmd.io/_uploads/ByNef59fGx.png)
- Voir les volumes
![image](https://hackmd.io/_uploads/Skxzz55zzg.png)
- Voir les évènements 
![image](https://hackmd.io/_uploads/HkdXz59Mfx.png)



### Commit GitHub + Packages

- Liste des commits
![image](https://hackmd.io/_uploads/rk0pzq9Mfl.png)

- Packages 
![image](https://hackmd.io/_uploads/SJgGt79cGzl.png)


---

## I. FAQ et dépannage

| Symptôme | Cause probable | Action |
|---|---|---|
| `network with name cicd-network already exists` | Terraform tente de créer le réseau au lieu de le lire | Créer le réseau manuellement en Phase 0 ; vérifier le `data "docker_network"` dans `infra/main.tf` |
| Jenkins ne voit pas SonarQube | Conteneurs sur des réseaux différents | Vérifier `--network cicd-network` sur Jenkins et SonarQube |
| Webhook GitHub en échec (timeout) | VM sans IP publique | Exposer Jenkins via ngrok (Phase 8.3) |
| Stage Trivy rouge | CVE réelles dans l'image | Appliquer le [correctif CVE](#phase-9---correctif-cve-trivy) |
| Smoke test : `linkpulse-staging` introuvable | Terraform pas encore appliqué ou image absente | Consulter les logs Jenkins stages 9–10 ; `docker ps -a` |
| SonarQube Quality Gate en attente | Webhook SonarQube → Jenkins mal configuré | URL `http://jenkins:8080/sonarqube-webhook/` (Phase 5.6) |
| Grafana sans données | Source Prometheus mal configurée | URL interne `http://prometheus:9090` (pas `localhost`) |
| `VOTRE_PSEUDO` oublié | Placeholders non remplacés | `grep -rn "VOTRE_PSEUDO" .` avant tout push |

> **Astuce :** en cas d'échec de pipeline, consultez toujours la **Console Output** du stage concerné - les blocs `post { failure { ... } }` du Jenkinsfile affichent les logs des conteneurs impactés.

---

