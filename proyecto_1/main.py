# import fastapi

# router = fastapi.APIRouter()

# @router.get("/")

# async def index():
#     return {"message": "Hello World"}


# @router.get("/hello/{name}")

# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}


from fastapi import FastAPI, Request, Form, Security, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi.responses import HTMLResponse, RedirectResponse
from config.database import Base, engine, Session, get_db
from fastapi.templating import Jinja2Templates
from models.models import Usuarios, Token
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import ValidationError
from sqlalchemy.orm import Session
from urllib.parse import quote
from jose import JWTError, jwt
from typing import Annotated
from typing import Tuple
import configparser
import requests
import uvicorn


app = FastAPI()

config = configparser.ConfigParser()
config.read('config.ini')

Base.metadata.create_all(bind=engine)

# Configuración OAuth2
# openssl rand -hex 32
SECRET_KEY = config['API']['SECRET_KEY']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

API_KEY = config['API']['API_KEY']

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)

# Configuración para usar plantillas Jinja2
templates = Jinja2Templates(directory="templates")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Función para obtener el usuario por nombre de usuario
def get_user( db: Session, nombre: str):
    return db.query(Usuarios).filter(Usuarios.nombre == nombre).first()

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.contraseña):
        return False
    return user

async def geocode_address(api_key: str, address: str) -> Tuple[float, float]:
    base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = {"key": api_key, "address": quote(address)}

    response = requests.get(base_url, params=params).json()
    response.keys()

    if response['status'] == 'OK':
        location = response["results"][0]["geometry"]
        return location['location']['lat'] , location['location']['lng']
    else:
        print(response['text'])
        raise Exception("Error in geocoding request")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = Usuarios(nombre=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(db, username=token_data.nombre)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: Annotated[Usuarios, Security(get_current_user, scopes=["me", "items"])]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Rutas CRUD
@app.post("/token", response_class=HTMLResponse, response_model=Token)
async def login_for_access_token(
    nombre: str = Form(...),
    contraseña: str = Form(...), 
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, nombre, contraseña)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # En lugar de usar form_data.scopes, asigna directamente todos los permisos necesarios
    all_scopes = ["me", "items"]

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.nombre, "scopes": all_scopes},
        expires_delta=access_token_expires,
    )

    # Redirige a /lista
    response = RedirectResponse(url="/lista", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="Authorization", value=f"Bearer {access_token}")

    return response

# Página de inicio con el formulario
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Manejar la solicitud POST desde el formulario
@app.post("/crear", response_class=HTMLResponse)
async def create_user(
    nombre: str = Form(None),
    apellido: str = Form(None),
    contraseña: str = Form(None),
    direccion: str = Form(None),
    tipo: str = Form(None),
    ciudad: str = Form(None),
    longitud: float = Form(None),
    latitud: float = Form(None),
    estado_geo: bool = Form(None),
    cargo: str = Form(None),
    db: Session = Depends(get_db)
):
    try:
        contraseña = get_password_hash(contraseña)
        # Crear el usuario solo con los valores que se pasan
        new_user = Usuarios(
            nombre=nombre,
            apellido=apellido,
            direccion=direccion,
            contraseña=contraseña,
            tipo=tipo,
            ciudad=ciudad,
            longitud=longitud,
            latitud=latitud,
            estado_geo=estado_geo,
            cargo=cargo
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/crear_usuario", response_class=HTMLResponse)
async def read_users(request: Request):
    return templates.TemplateResponse("registro_usuario.html", {"request": request})

@app.get("/lista", response_class=HTMLResponse)
async def read_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(Usuarios).all()
    return templates.TemplateResponse("lista_usuarios.html", {"request": request, "users": users})

@app.get("/usuario", response_class=HTMLResponse)
async def search_user(request: Request, id: int, db: Session = Depends(get_db)):
    user = db.query(Usuarios).filter(Usuarios.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    return templates.TemplateResponse("detalle_usuario.html", {"request": request, "user": user})

# Ruta para eliminar un usuario por ID
@app.get("/eliminar/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(Usuarios).filter(Usuarios.id == id).first()

    # Verifica si el usuario existe antes de eliminarlo y lanza una excepción si no existe
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado para eliminar")

    db.delete(user)
    db.commit()
    return RedirectResponse(url=app.url_path_for("read_users"), status_code=status.HTTP_303_SEE_OTHER)

@app.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(Usuarios).filter(Usuarios.id == id).first()

    # Verifica si el usuario existe antes de eliminarlo y lanza una excepción si no existe
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado para eliminar")

    db.delete(user)
    db.commit()
    return RedirectResponse(url=app.url_path_for("read_users"), status_code=status.HTTP_303_SEE_OTHER)



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)