import argparse
import json
import os
import time
import requests
import sqlite3
from datetime import datetime

# Configuration
MINDSDB_URL = "http://127.0.0.1:47334"
SQLITE_DB = "knowledge_bases.db"
def execute_mindsdb_query(query):
    """🔗 Execute a query against MindsDB"""
    url = f"{MINDSDB_URL}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "query": query,
        "database": "kb_source"
    }
    
    try:
        response = requests.get(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.text 
    except requests.RequestException as e:
        print(f"❌ Error executing MindsDB query: {e}")
        return None

def create_knowledge_base():
    """🔗 CREATE KNOWLEDGE_BASE"""
    # Create SQLite table
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            source TEXT DEFAULT 'manual',
            category TEXT DEFAULT 'general',
            importance INTEGER DEFAULT 1,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_content 
        ON knowledge_base (content)
    """)
    conn.commit()
    conn.close()
    
    # Create MindsDB datasource
    query = f"""
        CREATE DATABASE kb_source
        WITH ENGINE = 'sqlite',
        PARAMETERS = {{
            "db_file": "{SQLITE_DB}"
        }};
    """
    result = execute_mindsdb_query(query)
    if result:
        print("✅ Knowledge base created with SQLite backend and MindsDB integration")

def ingest_data(content, source="manual", category="general", importance=1):
    """🔗 INSERT INTO knowledge_base with metadata"""
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO knowledge_base 
        (content, source, category, importance) 
        VALUES (?, ?, ?, ?)""",
        (content, source, category, importance)
    )
    conn.commit()
    conn.close()
    print(f"📥 Ingested: '{content[:50]}...' ({source}, {category})")

def semantic_search(query, source=None, category=None, min_importance=None):
    """🔗 SEARCH knowledge_base using semantic search"""
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    
    sql_query = "SELECT * FROM knowledge_base WHERE content LIKE ?"
    params = [f"%{query}%"]
    
    if source:
        sql_query += " AND source = ?"
        params.append(source)
    if category:
        sql_query += " AND category = ?"
        params.append(category)
    if min_importance is not None:
        sql_query += " AND importance >= ?"
        params.append(min_importance)
    
    cursor.execute(sql_query, params)
    results = cursor.fetchall()
    
    conn.close()
    
    if results:
        print(f"🔍 Found {len(results)} results for '{query}':")
        for row in results:
            print(f"- {row[1][:50]}... (Source: {row[2]}, Category: {row[3]}, Importance: {row[4]})")
        return [row[1] for row in results]
    else:
        print(f"❌ No results found for '{query}'")
        return []



def create_sync_job():
    """🔗 CREATE JOB for periodic data sync"""
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sync_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_name TEXT NOT NULL,
            last_run DATETIME,
            next_run DATETIME,
            status TEXT DEFAULT 'pending'
        )
    """)
    conn.commit()
    
    # Create a sample job
    cursor.execute("""
        INSERT INTO sync_jobs (job_name, last_run, next_run, status)
        VALUES (?, ?, ?, ?)
    """, ("Periodic Sync", datetime.now(), datetime.now(), "pending"))
    
    conn.commit()
    conn.close()
    
    print("✅ Created periodic sync job for knowledge base updates")

def main():
    parser = argparse.ArgumentParser(
        description="Knowledge Base CLI with MindsDB Integration",
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Init command
    subparsers.add_parser('init', help='🔗 Create knowledge base structure')
    
    # Ingest command
    ingest_parser = subparsers.add_parser('ingest', help='🔗 Add data to knowledge base')
    ingest_parser.add_argument('content', help='Text content to ingest')
    ingest_parser.add_argument('--source', default='manual', help='Data source metadata')
    ingest_parser.add_argument('--category', default='general', help='Content category')
    ingest_parser.add_argument('--importance', type=int, default=1, help='Importance level (1-5)')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='🔗 Semantic content search')
    search_parser.add_argument('query', help='Search term')
    search_parser.add_argument('--source', help='Filter by source metadata')
    search_parser.add_argument('--category', help='Filter by category')
    search_parser.add_argument('--min-importance', type=int, help='Minimum importance level')
    
    # Job command
    subparsers.add_parser('create_job', help='🔗 Create periodic sync job')
    
    
    args = parser.parse_args()
    
    if args.command == 'init':
        create_knowledge_base()
    elif args.command == 'ingest':
        ingest_data(args.content, args.source, args.category, args.importance)
    elif args.command == 'search':
        semantic_search(args.query, args.source, args.category, args.min_importance)
    elif args.command == 'create_job':
        create_sync_job()

if __name__ == "__main__":
    main()
