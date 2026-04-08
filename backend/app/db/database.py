import sqlite3
import os
from typing import List, Dict, Any
from pathlib import Path

# Updated for SaaS structure: Looks for DB in backend/ root
DB_PATH = Path(__file__).resolve().parent.parent.parent / "mentors.db"

def init_db():
    # Ensure directory exists (though it should in backend/)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mentors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT,
            title TEXT,
            avatar_url TEXT,
            tech_stack TEXT -- Comma separated
        )
    ''')
    
    # Simple check for existing data
    cursor.execute("SELECT COUNT(*) FROM mentors")
    if cursor.fetchone()[0] == 0:
        seed_mentors(conn)
        
    conn.commit()
    conn.close()

def seed_mentors(conn):
    mentors = [
        ("David Henderson", "Google", "Senior Staff Engineer (Python/ML)", "https://api.dicebear.com/7.x/avataaars/svg?seed=david", "Python,FastAPI,SQL,Docker,Kubernetes"),
        ("Alice Chen", "Netflix", "Engineering Manager (Distributed Systems)", "https://api.dicebear.com/7.x/avataaars/svg?seed=alice", "Microservices,Cassandra,System Design,Go,Java"),
        ("Rohan Sharma", "Meta", "Senior Machine Learning Engineer", "https://api.dicebear.com/7.x/avataaars/svg?seed=rohan", "PyTorch,TensorFlow,Numpy,Python,Scikit-learn"),
        ("Sarah Jenkins", "Stripe", "Principal Frontend Engineer", "https://api.dicebear.com/7.x/avataaars/svg?seed=sarah", "React,TypeScript,Next.js,JS,TailwindCSS"),
        ("Kunal Nayyar", "AWS", "Cloud Architect (Serverless)", "https://api.dicebear.com/7.x/avataaars/svg?seed=kunal", "AWS,Lambda,DynamoDB,Infrastructure,Terraform"),
        ("Elena Moreno", "Uber", "Senior Product Engineer", "https://api.dicebear.com/7.x/avataaars/svg?seed=elena", "React Native,GraphQL,SQL,Node.js,Mobile"),
        ("Sujay Bansal", "OpenAI", "ML Infrastructure Lead", "https://api.dicebear.com/7.x/avataaars/svg?seed=sujay", "GPU,PyTorch,Scale,Python,Ray,CUDA"),
        ("Nishant Gunjal", "Microsoft", "Principal Software Engineer (Azure Core)", "https://api.dicebear.com/7.x/avataaars/svg?seed=nish", "Azure,Dotnet,C#,SQL,Distributed Systems"),
        ("Meera Thakur", "Apple", "Senior Embedded Systems Engineer", "https://api.dicebear.com/7.x/avataaars/svg?seed=meera", "C,C++,Rust,Embedded,RTOS"),
        ("Tanay Pratap", "Spotify", "Senior Backend Engineer", "https://api.dicebear.com/7.x/avataaars/svg?seed=tanay", "Java,SpringBoot,Kafka,BigData,PostgreSQL"),
        ("Marcus Thorne", "Citadel", "Quantitative Software Engineer", "https://api.dicebear.com/7.x/avataaars/svg?seed=marcus", "C++,Python,Low Latency,Algorithms"),
        ("Priya Das", "Airbnb", "Staff Software Engineer (Payments)", "https://api.dicebear.com/7.x/avataaars/svg?seed=priya", "Ruby,Rails,Java,Kafka,System Design"),
        ("Liam O'Connor", "Vercel", "Head of Developer Relations", "https://api.dicebear.com/7.x/avataaars/svg?seed=liam", "Next.js,React,Edge,JavaScript,Performance"),
        ("Fatima Zahra", "GitLab", "DevOps Engineering Lead", "https://api.dicebear.com/7.x/avataaars/svg?seed=fatima", "Git,CI/CD,Go,Terraform,Kubernetes"),
        ("Hiroshi Tanaka", "Sony", "Senior Security Researcher", "https://api.dicebear.com/7.x/avataaars/svg?seed=hiroshi", "Security,C,Python,Networking,Exploit"),
        ("Chloe Bell", "Discord", "Staff Backend Engineer (Elixir)", "https://api.dicebear.com/7.x/avataaars/svg?seed=chloe", "Elixir,Erlang,Websockets,Realtime"),
        ("Arjun Reddy", "DoorDash", "Senior Data Scientist (Dispatch)", "https://api.dicebear.com/7.x/avataaars/svg?seed=arjun", "Python,Pandas,ML,Stats,Optimized"),
        ("Sofia Rossi", "Cloudflare", "Systems Engineer (Edge Networking)", "https://api.dicebear.com/7.x/avataaars/svg?seed=sofia", "Rust,Go,Networking,WASM,Linux"),
        ("Kevin Zhang", "Roblox", "Principal Game Engine Engineer", "https://api.dicebear.com/7.x/avataaars/svg?seed=kevin", "C++,Graphics,Vulkan,Physics,Math"),
        ("Aisha Diallo", "Coinbase", "Senior Blockchain Engineer", "https://api.dicebear.com/7.x/avataaars/svg?seed=aisha", "Solidity,Go,Ethereum,Cryptography"),
        ("Oliver Schmidt", "SAP", "Principal Enterprise Architect", "https://api.dicebear.com/7.x/avataaars/svg?seed=oliver", "Java,SAP,Cloud,Kubernetes,ERP"),
        ("Maya Gupta", "LinkedIn", "Senior Data Engineer", "https://api.dicebear.com/7.x/avataaars/svg?seed=maya", "Spark,Scala,Airflow,DataLake,Python"),
        ("James Wilson", "Meta", "Senior Full Stack Engineer", "https://api.dicebear.com/7.x/avataaars/svg?seed=james", "React,Node.js,GraphQL,Relay,Python"),
        ("Amelia Watson", "Palantir", "Forward Deployed Engineer", "https://api.dicebear.com/7.x/avataaars/svg?seed=amelia", "Python,PostgreSQL,React,BigData"),
        ("Lucas Silva", "Docker", "Maintainer & Core contributor", "https://api.dicebear.com/7.x/avataaars/svg?seed=lucas", "Go,Docker,Containers,Linux,Containerd")
    ]
    conn.executemany("INSERT INTO mentors (name, company, title, avatar_url, tech_stack) VALUES (?,?,?,?,?)", mentors)

def find_best_mentors(target_title: str, user_tools: list, limit: int = 1) -> List[Dict[str, Any]]:
    # Open connection to the dynamic path
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mentors")
    mentors = cursor.fetchall()
    conn.close()

    scored = []
    title_words = target_title.lower().split() if target_title else []
    
    for m in mentors:
        score = 0
        m_stack = m['tech_stack'].split(',') if m['tech_stack'] else []
        overlap = set(m_stack).intersection(set(user_tools))
        score += len(overlap) * 3
        m_title = m['title'].lower()
        for word in title_words:
            if word in m_title:
                score += 2
        scored.append((score, m))

    scored.sort(key=lambda x: x[0], reverse=True)
    
    results = []
    for s, m in scored[:limit]:
        results.append({
            "name": m['name'],
            "company": m['company'],
            "title": m['title'],
            "avatar_url": m['avatar_url'],
            "tech_stack": m['tech_stack'].split(',')
        })
    return results
