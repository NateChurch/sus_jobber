import pathlib
import os
import json
from logging import getLogger
from dotenv import load_dotenv

logger = getLogger(__name__)
LOG = f"{__name__}-"


class Config(object):
    keyvault = None
    missing_attributes = set()

    AZURE_TENANT_ID = None
    AZURE_SUBSCRIPTION_ID = None
    AZURE_CLIENT_ID = None
    AZURE_CLIENT_SECRET = None

    def __init__(self, **kwargs):
        (
            self.BASE_DIR,
            self.SRC_DIR,
            self.VENV_DIR,
            self.CURRENT_DIR
        ) = self.find_local_dirs(kwargs.get("base_dir", None))

        self.dotenv_path = self.find_dot_env_file(
            base_dir=self.BASE_DIR,
            dotenv_path=None
        )

        load_dotenv(dotenv_path=self.dotenv_path)

        for key, value in kwargs.items():
            setattr(self, key, value)

        for key, value in self.__dict__.items():
            if value is None and key in os.environ:
                logger.debug(f"Setting {key} to {os.environ[key]}")
                setattr(self, key, os.environ[key])

        for key, value in self.__class__.__dict__.items():

            if callable(value):
                continue
            if value is None and key in os.environ:
                logger.debug(f"Setting {key} to {os.environ[key]}")
                setattr(self, key, os.environ[key])

    def set_config_value(
            self, env_var: str, secret_name: str = None, var_type=None, default_value=None
    ):
        """
        uses self.get_config_value to get the value of the environment variable and
        then sets it as an attribute of the class
        """
        value = self.get_config_value(
            env_var=env_var,
            secret_name=secret_name,
            var_type=var_type,
            default_value=default_value,
        )
        setattr(self, env_var, value)
        return value

    def find_dot_env_file(self, base_dir: pathlib.Path = None, dotenv_path: pathlib.Path = None) -> pathlib.Path:
        if base_dir is None:
            base_dir = pathlib.Path(os.getcwd())

        if dotenv_path is None:
            paths = [base_dir] + [
                pathlib.Path(path) for path in os.environ.get("PYTHONPATH", "").split(os.pathsep)
            ]

            for path in paths:
                dotenv_path = path.joinpath(".env")
                if dotenv_path.exists():
                    break

        if dotenv_path.exists():
            logger.info(f"{LOG} Located .env file at {dotenv_path}")
            return dotenv_path
        else:
            logger.info(f"CONFIG: Unable to locate .env file at {dotenv_path}")
            logger.info("CONFIG: Does the .env exist and did you enable the workspace?")
            return None

    def find_local_dirs(self, base_dir: pathlib.Path = None) -> (
            tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path]):
        """
        Find the project directory and the src directory
        :param base_dir: if given a base_dir, will use that as the base directory
        :return: base_dir, src_dir, venv_dir, current_dir
        """
        if base_dir is None:
            logger.debug(f"{LOG} No base_dir given.")
            base_dir = pathlib.Path(os.getcwd())
            src_dir = None
            venv_dir = None

            # Find details about the project
            current_path = base_dir
            while (src_dir is None or venv_dir is None) and \
                    current_path != current_path.parent:
                logger.debug(f"{LOG} Current Path: {current_path}")

                if current_path.name == "src":
                    src_dir = current_path
                elif current_path.joinpath("src").exists():
                    src_dir = current_path.joinpath("src")

                if current_path.joinpath(".venv").exists():
                    venv_dir = current_path

                current_path = current_path.parent

            if venv_dir is None:
                logger.info(f"{LOG} Unable to locate venv(project) directory")
                venv_dir = base_dir

            if src_dir is None:
                logger.info(f"{LOG} Unable to locate src directory")
                src_dir = venv_dir

        else:
            logger.info(f"{LOG} Base Dir: {base_dir}")
            base_dir = base_dir
            src_dir = base_dir.joinpath("src")
            venv_dir = base_dir

        current_dir = pathlib.Path(os.getcwd())

        return base_dir, src_dir, venv_dir, current_dir
