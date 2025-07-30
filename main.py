from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List, Optional

import auth, models, crud
from database import get_db

# Cria a aplicação FastAPI
app = FastAPI(title="API de Consulta Tremed")

# Endpoint de Login
@app.post("/token", response_model=models.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoints de Consulta de Produtos (Protegidos)
# O parâmetro token: str = Depends(auth.oauth2_scheme) protege a rota.
# Apenas usuários com um token válido podem acessá-la.

@app.get("/api/products/search", response_model=List[models.Product])
def search_products_endpoint(
    q: Optional[str] = None,
    brand: Optional[str] = None,
    supplier: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    token: str = Depends(auth.oauth2_scheme)
):
    products = crud.search_products(db, search_term=q, brand=brand, supplier=supplier, min_price=min_price, max_price=max_price, limit=limit, offset=offset)
    return products

@app.get("/api/filters/brands", response_model=List[str])
def get_brands_endpoint(db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    return crud.get_distinct_brands(db)

@app.get("/api/filters/suppliers", response_model=List[str])
def get_suppliers_endpoint(db: Session = Depends(get_db), token: str = Depends(auth.oauth2_scheme)):
    return crud.get_distinct_suppliers(db)