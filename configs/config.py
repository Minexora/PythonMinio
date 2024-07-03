
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="MINIO",
    environments=True,
    settings_files=['configs/settings.toml', 'configs/.secrets.toml'],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
