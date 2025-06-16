
<br/>
<div align="center">
<a href="https://github.com/ShaanCoding/ReadME-Generator">
<img src="https://cdn.prod.website-files.com/627df74f79858fa879bb51b1/65257913c33d82a87b86775a_mindsdb%20(1).png" alt="Logo" width="80" height="80">
</a>
<h3 align="center">CLI MindsDB</h3>
<p align="center">
A CLI Mindsdb tool to automate the process for Knowledge Base (KB)


  


</p>
</div>

## Why CLI MindsDB✅

MindsDB enables humans, AI, agents, and applications to get highly accurate answers across disparate data sources and types. With this technology, we can make the complex process to be loveable and easy to handling by just create the data, store the data & make mindsdb process it from behind it. 

CLI Mindsdb help you to automate the process from create knowledge base, ingest the data, do semantic search, execute mindsdb query, and create to sync a job all in one process by just called the command that you want to process it by a second.🔥
### Built With

- [MindsDB](https://mindsdb.com/)
- [Python](https://www.python.org/)
- [SQLite](https://sqlite.org/)
- [Docker](https://www.docker.com/)

### Key Features
1.) Knowledge Base with Metadata:
<ul>
  <li>Creates SQLite KB with metadata columns (source, category, importance)</li>
  <li>Builds MindsDB datasource for advanced querying</li>
  <li>ingest command with metadata parameters</li>
</ul>

2.) Semantic Search with Filtering:
<ul>
  <li>search command with content search and metadata filtering</li>
  <li>Combines LIKE queries with metadata conditions</li>
  <li>Example: search "AI" --source=research --min-importance=3</li>
</ul>

3.) Automated Data Sync:
<ul>
  <li>create_job sets up periodic data ingestion</li>
  <li>Simulates fetching from external sources</li>
  <li>Uses MindsDB's job scheduler (runs hourly)</li>
</ul>

### Prerequisites

Make sure that you install this prerequisite to make it work.

1.) Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) 

2.) Open Docker Desktop and type this in your terminal to start mindsdb:
```sh
  docker run -p 47334:47334 mindsdb/mindsdb
  ```

3.) Do install requests package from python by type in your terminal:
  ```sh
  pip install requests
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/daviddprtma/cli-mindsdb.git
   ```
2. Create KB Structure
   ```sh
   python kb_cli.py init
   ```
3. Create Sync Job
   ```sh
   python kb_cli.py create_job
   ```
4. Create Ingest Data
   ```sh
   python kb_cli.py ingest "Transformers revolutionized NLP" \--source=research --category=ml --importance=5
   ```
5. Find semantic search
   ```sh
   python kb_cli.py search "AI" --category=ml
   ```
## The Architecture
![image](https://github.com/user-attachments/assets/fd373eef-fa5e-479c-aa5a-557f7f573166)

### Video Presentation
Here's the video presentation of CLI MindsDB: 
<br> 
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/tAXSHTLhkqg/0.jpg)](https://www.youtube.com/watch?v=tAXSHTLhkqg)
