# 🧠 RAG & Knowledge Graph - Installation Guide

This module manages the long-term memory (RAG) of the application by storing scraped documents and their vectors (Embeddings) in a **Neo4j** database.

## 🛠️ Prerequisites

* **Docker** (Recommended) OR **Neo4j Desktop**
* Python 3.10+
* A Google API key (for `text-embedding-004` embeddings)

---

## 🚀 Option 1: Installation via Docker (Recommended)

This is the simplest method. It automatically installs Neo4j with the necessary plugins (**APOC** and **Graph Data Science**).

1.  Create a `docker-compose.yml` file at the root of the project with this content:

    ```yaml
    version: '3.8'

    services:
      neo4j-local:
        image: neo4j:5.15.0
        container_name: iyp_knowledge_graph
        ports:
          - "7474:7474" # HTTP (Browser)
          - "7687:7687" # Bolt (Python Connection)
        environment:
          - NEO4J_AUTH=neo4j/password_local_123
          - NEO4J_PLUGINS=["apoc", "graph-data-science"]
          - NEO4J_dbms_security_procedures_unrestricted=apoc.*,gds.*
          - NEO4J_server_memory_heap_initial__size=1G
          - NEO4J_server_memory_heap_max__size=2G
        volumes:
          - ./data/neo4j_data:/data
        restart: unless-stopped
    ```

2.  Start the container:
    ```bash
    docker-compose up -d
    ```

3.  Access the interface: [http://localhost:7474](http://localhost:7474)
    * **User:** `neo4j`
    * **Password:** `password_local_123`

---

## 💻 Option 2: Installation via Neo4j Desktop

If you cannot use Docker:

1.  Download and install **Neo4j Desktop**.
2.  Create a new database (Local DBMS).
3.  **IMPORTANT:** Install the required plugins via the "Plugins" tab:
    * ✅ **APOC**
    * ✅ **Graph Data Science Library** (GDS)
4.  Start the database ("Start").

---

## ⚙️ Configuration (.env)

Add the following variables to your `.env` file so the Python code can connect:

```ini
# --- LOCAL NEO4J (RAG) ---
# If using Docker or native Desktop:
NEO4J_LOCAL_URI=bolt://localhost:7687

# 🐧 IF YOU ARE ON WSL (Windows Subsystem for Linux):
# Use the Windows IP (found via `ip route` in WSL) instead of localhost
# NEO4J_LOCAL_URI=bolt://192.168.x.x:7687

NEO4J_LOCAL_USER=neo4j
NEO4J_LOCAL_PASSWORD=motdepasse

# --- EMBEDDINGS ---
# Required for vectorization
GOOGLE_API_KEY=your_google_api_key_here
```