import os
from dotenv import load_dotenv
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import ssl

load_dotenv()

# Obtener variables de entorno con valores por defecto
POSTGRESQL_ADDON_USER = os.getenv('POSTGRESQL_ADDON_USER', 'uupit9mkwkdby2wuqimw')
POSTGRESQL_ADDON_PASSWORD = os.getenv('POSTGRESQL_ADDON_PASSWORD', 'WLbqR3mqLfxJVbLZRMmds0FVcjPgrd')
POSTGRESQL_ADDON_HOST = os.getenv('POSTGRESQL_ADDON_HOST', 'bxmi248k1opffz8lupql-postgresql.services.clever-cloud.com')
POSTGRESQL_ADDON_PORT = os.getenv('POSTGRESQL_ADDON_PORT', '50013')
POSTGRESQL_ADDON_DB = os.getenv('POSTGRESQL_ADDON_DB', 'bxmi248k1opffz8lupql')

# Construir la URL de conexión
DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRESQL_ADDON_USER}:{POSTGRESQL_ADDON_PASSWORD}"
    f"@{POSTGRESQL_ADDON_HOST}:{POSTGRESQL_ADDON_PORT}/"
    f"{POSTGRESQL_ADDON_DB}"
)

# Configurar SSL sin verificación estricta
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False  # Deshabilitar verificación del hostname
ssl_context.verify_mode = ssl.CERT_NONE  # Deshabilitar verificación del certificado

# Crear el motor con la configuración de SSL y pool limitado
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"ssl": ssl_context},
    pool_size=2,  # Máximo 2 conexiones en el pool
    max_overflow=2,  # Máximo 2 conexiones adicionales si se necesita
    pool_timeout=30,  # Tiempo de espera para obtener una conexión
    pool_pre_ping=True  # Verifica que las conexiones estén vivas antes de usarlas
)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        raise