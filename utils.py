# utils.py
import requests
import xml.etree.ElementTree as ET
import re
from html import unescape
import random

# Expected skill sets
skill_sets = ["Python", "Django", "Flask", "FastAPI", "SQLAlchemy", "NumPy", "Pandas", "SciPy", "Scikit-learn", "React", "Vue", "PostgreSQL", "MySQL", "Celery", "Jenkins", "Pytest", "Unittest", "Peewee", "MongoDB", "ClickHouse", "Jira", "Confluence", "Gen AI", "AWS", "GCP", "Azure", "OpenAI", "LLM", "Anthropic", "AI", "GPT", "Claude", "Gemini", "OOP", "Docker", "Kubernetes", "Git", "Bitbucket", "SQL", "NoSQL", "Express.js", "C++", "asyncio", "aiohttp"]

# Essential functions

def get_skills(experience):
    skills = []
    for skill in skill_sets:
        if skill in experience:
            skills.append(skill)
    return ", ".join(skills)

def fetch_rss_data():
    url = "https://jobs.dou.ua/vacancies/feeds/?category=Python"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # If the request fails, an exception is raised
    
    root = ET.fromstring(response.content)
    
    rss_candidates = []
    for item in root.findall(".//item"):
        title = item.find("title").text
        description = unescape(item.find("description").text)
        
        experience_years = random.randint(2, 10)
        
        rss_candidates.append({
            "name": title,
            "skills": get_skills(description),
            "experience": f"{experience_years} years",
            # "experience": extract_experience(description),
        })
    
    return rss_candidates
