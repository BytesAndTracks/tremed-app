from sqlalchemy.orm import Session
from sqlalchemy import text
import uuid
import auth
import models

def get_user_by_username(db: Session, username: str):
    """Busca um usuário pelo nome de usuário."""
    query = text("SELECT * FROM users WHERE username = :username")
    result = db.execute(query, {"username": username}).first()
    if result:
        return models.UserInDB(**result._mapping)
    return None

def create_user(db: Session, user: models.UserCreate):
    """Cria um novo usuário no banco de dados."""
    hashed_password = auth.get_password_hash(user.password)
    # Gera um ID único e aleatório para o novo usuário
    user_id = str(uuid.uuid4())
    
    query = text("""
        INSERT INTO users (id, username, hashed_password)
        VALUES (:id, :username, :hashed_password)
    """)
    db.execute(query, {
        "id": user_id,
        "username": user.username,
        "hashed_password": hashed_password
    })
    db.commit()
    return models.UserInDB(id=user_id, username=user.username, hashed_password=hashed_password)


def search_products(db: Session, search_term: Optional[str], brand: Optional[str], supplier: Optional[str], min_price: Optional[float], max_price: Optional[float], limit: int, offset: int):
    """Busca produtos com filtros avançados."""
    base_query = "SELECT produto, cod_fornecedor, anvisa, preco_unitario_venda, unidade_medida, marca, fornecedor, observacao, data_de_atualizacao FROM produtos WHERE 1=1"
    
    params = {}
    
    if search_term:
        base_query += " AND (produto LIKE :search_term OR marca LIKE :search_term)"
        params["search_term"] = f"%{search_term}%"
    
    if brand:
        base_query += " AND marca = :brand"
        params["brand"] = brand
        
    if supplier:
        base_query += " AND fornecedor = :supplier"
        params["supplier"] = supplier
        
    if min_price is not None:
        base_query += " AND preco_unitario_venda >= :min_price"
        params["min_price"] = min_price
        
    if max_price is not None:
        base_query += " AND preco_unitario_venda <= :max_price"
        params["max_price"] = max_price
        
    base_query += " LIMIT :limit OFFSET :offset"
    params["limit"] = limit
    params["offset"] = offset

    query = text(base_query)
    result = db.execute(query, params)
    
    return [models.Product(**row._mapping) for row in result]

def get_distinct_brands(db: Session):
    """Retorna uma lista de todas as marcas distintas."""
    query = text("SELECT DISTINCT marca FROM produtos WHERE marca IS NOT NULL AND marca != '' ORDER BY marca")
    return [row[0] for row in db.execute(query)]

def get_distinct_suppliers(db: Session):
    """Retorna uma lista de todos os fornecedores distintos."""
    query = text("SELECT DISTINCT fornecedor FROM produtos WHERE fornecedor IS NOT NULL AND fornecedor != '' ORDER BY fornecedor")
    return [row[0] for row in db.execute(query)]