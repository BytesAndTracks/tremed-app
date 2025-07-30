from pydantic import BaseModel, Field
from typing import Optional, List
import uuid

# Modelos para Produtos
class Product(BaseModel):
    produto: Optional[str] = None
    cod_fornecedor: Optional[str] = None
    anvisa: Optional[str] = None
    preco_unitario_venda: Optional[float] = None
    unidade_medida: Optional[str] = None
    marca: Optional[str] = None
    fornecedor: Optional[str] = None
    observacao: Optional[str] = None
    data_de_atualizacao: Optional[str] = None

    class Config:
        from_attributes = True

# Modelos para Autenticação e Usuários
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: str
    hashed_password: str

    class Config:
        from_attributes = True
        
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None