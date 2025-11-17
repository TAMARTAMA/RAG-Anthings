# OPENSEARCH_DOCKER_README.md

# Running OpenSearch in Docker for Moptimizer

This guide explains how to run OpenSearch in Docker with the current project setup.

---

## 1. Pull the OpenSearch Docker Image

```bash
docker pull opensearchproject/opensearch:latest
```

---

## 2. Run OpenSearch Container

```bash
docker run -d \
  --name opensearch \
  -p 9200:9200 \
  -p 9600:9600 \
  -v opensearch-data:/usr/share/opensearch/data \
  -e discovery.type=single-node \
  -e plugins.security.disabled=true \
  -e OPENSEARCH_JAVA_OPTS="-Xms512m -Xmx512m" \
  -e OPENSEARCH_INITIAL_ADMIN_PASSWORD="MyStrongPassword123!" \
  --runtime=nvidia \
  opensearchproject/opensearch:latest \
  ./opensearch-docker-entrypoint.sh opensearch
```

### Explanation:

- `-d` → run in detached mode (background)  
- `--name opensearch` → container name  
- `-p 9200:9200 -p 9600:9600` → expose container ports to host  
- `-v opensearch-data:/usr/share/opensearch/data` → persistent volume for data  
- `-e ...` → environment variables (single-node, disable security, JVM memory, admin password)  
- `--runtime=nvidia` → use GPU runtime if available  
- `opensearchproject/opensearch:latest` → Docker image  
- `./opensearch-docker-entrypoint.sh opensearch` → entrypoint command  

---

## 3. Verify OpenSearch is Running

```bash
curl -X GET "http://localhost:9200/"
```

Expected response: JSON with cluster information, version, and node name.

---

## 4. Stopping and Removing the Container

```bash
docker stop opensearch
docker rm opensearch
```

---

## 5. Notes

- Data is persisted in the volume `opensearch-data` so you can restart the container without losing data.  
- If you want to reset data, remove the volume:  
```bash
docker volume rm opensearch-data
```  
- Adjust ports or JVM memory as needed for your server resources.

