import os
import logging
from typing import Union

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")


def run_query(sql: str, params: tuple | list | None = None, single: bool = False):
    if not DATABASE_URL:
        raise HTTPException(status_code=500, detail="DATABASE_URL is not set")

    try:
        with psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row,
            connect_timeout=5,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, params)
                return cur.fetchone() if single else cur.fetchall()
    except psycopg.Error as exc:
        logging.exception("Database connection failed: %s", exc)
        raise HTTPException(status_code=500, detail="Database connection failed")

@app.get("/")
def read_root():
    rows = run_query("SELECT * FROM experience LIMIT 100;")
    return {"experience": rows}


@app.get("/experiences")
def list_experiences(sort: str = Query("-date_debut")):
    order = "DESC" if sort.startswith("-") else "ASC"
    field = sort.lstrip("-")
    if field != "date_debut":
        raise HTTPException(status_code=400, detail="Invalid sort field")

    sql = (
        "SELECT e.*, COUNT(p.id) AS project_count "
        "FROM experience e "
        "LEFT JOIN projet p ON p.experience_id = e.id "
        "GROUP BY e.id "
        f"ORDER BY e.date_debut {order} NULLS LAST;"
    )
    rows = run_query(sql)
    return {"experiences": rows}


@app.get("/experiences/{experience_id}/full")
def get_experience_full(experience_id: int):
    experience = run_query(
        "SELECT * FROM experience WHERE id = %s;",
        (experience_id,),
        single=True,
    )
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")

    projects = run_query(
        "SELECT * FROM projet WHERE experience_id = %s ORDER BY date_projet DESC NULLS LAST;",
        (experience_id,),
    )
    skills = run_query(
        "SELECT c.* "
        "FROM competence c "
        "JOIN experience_competence ec ON ec.competence_id = c.id "
        "WHERE ec.experience_id = %s "
        "ORDER BY c.nom;",
        (experience_id,),
    )

    return {"experience": experience, "projects": projects, "skills": skills}


@app.get("/projects/search")
def search_projects(query: str | None = None, skills: str | None = None):
    where_clauses = []
    params: list = []

    if query:
        where_clauses.append("(p.titre ILIKE %s OR p.description ILIKE %s)")
        like = f"%{query}%"
        params.extend([like, like])

    skill_list = []
    if skills:
        skill_list = [s.strip() for s in skills.split(",") if s.strip()]
    if skill_list:
        where_clauses.append(
            "EXISTS ("
            "SELECT 1 FROM projet_competence pc "
            "JOIN competence c ON c.id = pc.competence_id "
            "WHERE pc.projet_id = p.id AND c.nom = ANY(%s)"
            ")"
        )
        params.append(skill_list)

    where_sql = " WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    # Récupérer les projets avec leurs compétences agrégées
    sql = (
        "SELECT p.*, "
        "COALESCE(array_agg(c.nom) FILTER (WHERE c.nom IS NOT NULL), '{}') AS skills "
        "FROM projet p "
        "LEFT JOIN projet_competence pc ON pc.projet_id = p.id "
        "LEFT JOIN competence c ON c.id = pc.competence_id"
        + where_sql
        + " GROUP BY p.id ORDER BY p.date_projet DESC NULLS LAST;"
    )
    rows = run_query(sql, params)
    return {"projects": rows}


@app.get("/skills/top")
def top_skills(k: int = 10):
    if k <= 0:
        raise HTTPException(status_code=400, detail="k must be positive")

    sql = (
        "SELECT c.*, COUNT(*) AS usage_count "
        "FROM ("
        "SELECT competence_id FROM projet_competence "
        "UNION ALL "
        "SELECT competence_id FROM experience_competence"
        ") u "
        "JOIN competence c ON c.id = u.competence_id "
        "GROUP BY c.id "
        "ORDER BY usage_count DESC, c.nom ASC "
        "LIMIT %s;"
    )
    rows = run_query(sql, (k,))
    return {"skills": rows}


@app.get("/projects/{project_id}/similar")
def similar_projects(project_id: int, k: int = 5):
    if k <= 0:
        raise HTTPException(status_code=400, detail="k must be positive")

    sql = (
        "WITH target_skills AS ("
        "SELECT competence_id FROM projet_competence WHERE projet_id = %s"
        ") "
        "SELECT p.*, COUNT(*) AS shared_skills "
        "FROM projet p "
        "JOIN projet_competence pc ON pc.projet_id = p.id "
        "JOIN target_skills ts ON ts.competence_id = pc.competence_id "
        "WHERE p.id <> %s "
        "GROUP BY p.id "
        "ORDER BY shared_skills DESC, p.id ASC "
        "LIMIT %s;"
    )
    rows = run_query(sql, (project_id, project_id, k))
    return {"projects": rows}


@app.get("/projects/featured")
def featured_projects(limit: int = 3):
    """Endpoint optimisé pour la page d'accueil - retourne uniquement les projets principaux"""
    if limit <= 0 or limit > 10:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 10")
    
    sql = (
        "SELECT p.*, "
        "COALESCE(array_agg(c.nom) FILTER (WHERE c.nom IS NOT NULL), '{}') AS skills "
        "FROM projet p "
        "LEFT JOIN projet_competence pc ON pc.projet_id = p.id "
        "LEFT JOIN competence c ON c.id = pc.competence_id "
        "GROUP BY p.id "
        "ORDER BY p.date_projet DESC NULLS LAST "
        "LIMIT %s;"
    )
    rows = run_query(sql, (limit,))
    return {"projects": rows}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}