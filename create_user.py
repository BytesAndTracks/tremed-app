from sqlalchemy.orm import Session
import crud, models
from database import SessionLocal

def create_new_user():
    print("--- Criador de Novo Usuário ---")
    db = SessionLocal()
    try:
        username = input("Digite o nome de usuário do novo vendedor: ").strip()
        # Verifica se o usuário já existe
        if crud.get_user_by_username(db, username=username):
            print(f"Erro: O usuário '{username}' já existe.")
            return

        password = input(f"Digite a senha para '{username}': ").strip()
        user_in = models.UserCreate(username=username, password=password)
        crud.create_user(db=db, user=user_in)
        print(f"Usuário '{username}' criado com sucesso!")

    finally:
        db.close()

if __name__ == "__main__":
    create_new_user()