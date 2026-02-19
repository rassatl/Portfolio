import os
import logging
from typing import Union

import psycopg
import bcrypt
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

# Modèle pour la login
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    user_id: int | None = None

class ProjectRequest(BaseModel):
    titre: str
    description: str
    github_url: str | None = None
    lien_url: str | None = None
    date_projet: str | None = None
    experience_id: int | None = None
    skills: list[str] = []
    user_id: int | None = None

class ProjectResponse(BaseModel):
    success: bool
    message: str
    project_id: int | None = None

class DeleteProjectRequest(BaseModel):
    user_id: int

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
                # Pour les SELECT ou les opérations avec RETURNING, fetch les résultats
                if sql.strip().upper().startswith('SELECT') or 'RETURNING' in sql.upper():
                    return cur.fetchone() if single else cur.fetchall()
                # Pour les autres opérations (DELETE, UPDATE, INSERT sans RETURNING)
                return None
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
        "SELECT p.id, p.titre, p.description, p.github_url, p.lien_url, p.date_projet, p.experience_id, p.user_id, "
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
        "SELECT p.id, p.titre, p.description, p.github_url, p.lien_url, p.date_projet, p.experience_id, p.user_id, COUNT(*) AS shared_skills "
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
        "SELECT p.id, p.titre, p.description, p.github_url, p.lien_url, p.date_projet, p.experience_id, p.user_id, "
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


@app.post("/login")
def login(request: LoginRequest):
    """
    Route de connexion - Vérifie les identifiants de l'utilisateur
    """
    try:
        # Chercher l'utilisateur par username
        user = run_query(
            'SELECT id, username, password_hash FROM users WHERE username = %s;',
            (request.username,),
            single=True
        )
        
        # Vérifier que l'utilisateur existe
        if not user:
            raise HTTPException(status_code=401, detail="Identifiants invalides")
        
        # Vérifier le password avec bcrypt
        password_correct = bcrypt.checkpw(
            request.password.encode('utf-8'),
            user['password_hash'].encode('utf-8')
        )
        
        if not password_correct:
            raise HTTPException(status_code=401, detail="Identifiants invalides")
        
        # Connexion réussie
        return LoginResponse(
            success=True,
            message="Connexion réussie",
            user_id=user['id']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Erreur lors de la connexion: %s", e)
        raise HTTPException(status_code=500, detail="Erreur serveur")


@app.post("/projects")
def create_project(request: ProjectRequest):
    """
    Route de création de projet - Ajoute un nouveau projet à la base de données
    """
    try:
        logging.info(f"Creating project with data: {request.dict()}")
        
        # Insérer le projet
        insert_sql = (
            "INSERT INTO projet (titre, description, github_url, lien_url, date_projet, experience_id, user_id) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s) "
            "RETURNING id;"
        )
        result = run_query(
            insert_sql,
            (
                request.titre,
                request.description,
                request.github_url,
                request.lien_url,
                request.date_projet,
                request.experience_id,
                request.user_id
            ),
            single=True
        )
        
        if not result:
            raise HTTPException(status_code=500, detail="Erreur lors de la création du projet")
        
        project_id = result['id']
        
        # Ajouter les compétences si fournies
        if request.skills:
            for skill_name in request.skills:
                # Chercher ou créer la compétence
                skill = run_query(
                    "SELECT id FROM competence WHERE nom = %s;",
                    (skill_name,),
                    single=True
                )
                
                if skill:
                    skill_id = skill['id']
                else:
                    # Créer la compétence si elle n'existe pas
                    skill_result = run_query(
                        "INSERT INTO competence (nom) VALUES (%s) RETURNING id;",
                        (skill_name,),
                        single=True
                    )
                    skill_id = skill_result['id']
                
                # Ajouter la relation projet-compétence
                run_query(
                    "INSERT INTO projet_competence (projet_id, competence_id) VALUES (%s, %s);",
                    (project_id, skill_id)
                )
        
        return ProjectResponse(
            success=True,
            message="Projet créé avec succès",
            project_id=project_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Erreur lors de la création du projet: %s", e)
        raise HTTPException(status_code=500, detail="Erreur serveur")


@app.delete("/projects/{project_id}")
def delete_project(project_id: int, request: DeleteProjectRequest):
    """
    Route de suppression de projet - Supprime un projet si l'utilisateur en est le propriétaire
    """
    try:
        # Vérifier que le projet existe et appartient à l'utilisateur
        project = run_query(
            "SELECT id, user_id FROM projet WHERE id = %s;",
            (project_id,),
            single=True
        )
        
        if not project:
            raise HTTPException(status_code=404, detail="Projet non trouvé")
        
        # Vérifier que l'utilisateur est le propriétaire
        if project['user_id'] != request.user_id:
            raise HTTPException(status_code=403, detail="Vous ne pouvez pas supprimer ce projet")
        
        # Supprimer les relations projet_competence
        run_query(
            "DELETE FROM projet_competence WHERE projet_id = %s;",
            (project_id,)
        )
        
        # Supprimer le projet
        run_query(
            "DELETE FROM projet WHERE id = %s;",
            (project_id,)
        )
        
        return {"success": True, "message": "Projet supprimé avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Erreur lors de la suppression du projet: %s", e)
        raise HTTPException(status_code=500, detail="Erreur serveur")
