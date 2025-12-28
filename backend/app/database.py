from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

def from_environment_variable(variable_name: str) -> str:
    """Get a value from an environment variable."""
    import os
    value = os.getenv(variable_name)
    if value is None:
        raise ValueError(f"Environment variable {variable_name} is not set.")
    return value

# get url from environment variable
DATABASE_URL = from_environment_variable("DATABASE_URL")
# DATABASE_URL = "postgresql://mihir:mypassword@localhost/mydb"  

engine = create_engine(DATABASE_URL,pool_pre_ping=True,pool_recycle=300)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
