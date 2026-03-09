#!/usr/bin/env python3
import sqlite3
import json

# Connect to the database
conn = sqlite3.connect("/root/.openclaw/memory/main.sqlite")
cursor = conn.cursor()

# Query chunks table
print("=== chunks table ===")
cursor.execute("SELECT id, path, start_line, end_line, SUBSTR(text, 1, 100) FROM chunks LIMIT 3;")
for row in cursor.fetchall():
    print(f"ID: {row[0]}")
    print(f"Path: {row[1]}")
    print(f"Lines: {row[2]}-{row[3]}")
    print(f"Text snippet: {row[4]}")
    print()

# Query chunks_fts table
print("=== chunks_fts table ===")
cursor.execute("SELECT text, id, path, source, model, start_line, end_line FROM chunks_fts LIMIT 3;")
for row in cursor.fetchall():
    print(f"Text snippet: {row[0][:100]}...")
    print(f"ID: {row[1]}")
    print(f"Path: {row[2]}")
    print(f"Source: {row[3]}")
    print(f"Model: {row[4]}")
    print(f"Lines: {row[5]}-{row[6]}")
    print()

# Try to query chunks_vec (vec0 extension might not be available in CLI, but let's try)
print("=== chunks_vec table (first 3 entries) ===")
try:
    cursor.execute("SELECT id, embedding FROM chunks_vec LIMIT 3;")
    for row in cursor.fetchall():
        print(f"ID: {row[0]}")
        print(f"Embedding (first 10 floats): {row[1][:10]}...")
        print()
except Exception as e:
    print(f"Error querying chunks_vec: {e}")
    print("(vec0 extension not available in sqlite3 CLI)")

conn.close()
