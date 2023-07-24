from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# BD por defecto Django 'SQLite3'
SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Conexion BD externa 'PostgreSQL'
POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'nombre_base_datos',
        'USER': 'usuario que conecta a la BD',
        'PASSWORD': 'pasword del user',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Conexion BD externa 'Oracle'
ORACLE = {
    "default": {
        "ENGINE": "django.db.backends.oracle",
        "NAME": "127.0.0.1:1521/orcl",
        "USER": "c##grupo2",
        "PASSWORD": "grupo2",
        'TEST': {
            'USER': 'default_test',
            'TBLSPACE': 'default_test_tbls',
            'TBLSPACE_TMP': 'default_test_tbls_tmp',
        }
    }
}

