# import fastapi

# router = fastapi.APIRouter()

# @router.get("/")

# async def index():
#     return {"message": "Hello World"}


# @router.get("/hello/{name}")

# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}

from fastapi import FastAPI, Request, Form, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from config.database import Base, engine, Session
from models.models import Usuarios
from fastapi import Depends

app = FastAPI()

# Configuración para usar plantillas Jinja2
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# Página de inicio con el formulario
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Manejar la solicitud POST desde el formulario
@app.post("/crear", response_class=HTMLResponse)
async def create_user(
    nombre: str = Form(None),
    apellido: str = Form(None),
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
        # Crear el usuario solo con los valores que se pasan
        new_user = Usuarios(
            nombre=nombre,
            apellido=apellido,
            direccion=direccion,
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
        return RedirectResponse(url="/lista", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@app.get("/lista", response_class=HTMLResponse)
def read_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(Usuarios).all()
    return templates.TemplateResponse("lista_usuarios.html", {"request": request, "users": users})

@app.get("/usuario", response_class=HTMLResponse)
def search_user(request: Request, id: int, db: Session = Depends(get_db)):
    user = db.query(Usuarios).filter(Usuarios.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    
    return templates.TemplateResponse("detalle_usuario.html", {"request": request, "user": user})

# Ruta para eliminar un usuario por ID
@app.get("/eliminar/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.get(Usuarios, id)
    
    # Verifica si el usuario existe antes de eliminarlo y lanza una excepción si no existe
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado para eliminar")
    
    db.delete(user)
    db.commit()
    return RedirectResponse(url=app.url_path_for("read_users"), status_code=status.HTTP_303_SEE_OTHER)