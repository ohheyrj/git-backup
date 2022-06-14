import tempfile
from common.config import Config
import logging


class Utils:
    def __init__(self):
        self.general_config = Config().general_config

    def create_working_dir(self):
        self.working_dir = tempfile.TemporaryDirectory(dir=self.general_config['tmp_folder_dir'])
        logging.info('Creating tmp dir: %s', self.working_dir.name)

    def remove_tmp_dir(self):
        self.working_dir.cleanup()

    @property
    def working_dir_name(self):
        return self.working_dir.name
