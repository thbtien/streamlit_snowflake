
from dynaconf import Dynaconf

# config = LazySettings(
#     PRELOAD_FOR_DYNACONF=["src/config/*"],
#     ROOT_PATH_FOR_DYNACONF="src"
# )

settings = Dynaconf(
    settings_files=["src/config/config.ini"],
    load_dotenv=True,
    environments=True
)