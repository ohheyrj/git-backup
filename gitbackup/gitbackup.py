from common.config import Config
from common.gitlab import GitlabBackup
from common.sql import Sql

import logging


class GitBackup:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
        self.conf = Config()
        self.sql = Sql()

    def main(self):
        logging.info('Starting Git Backup')
        # Setup the database
        logging.info('Setting up DB')
        self.sql.create_tables()

        if self.conf.gitlab_config['enabled'] == 'True':
            GitlabBackup().main()
        logging.info('Finished Git Backup')


if __name__ == "__main__":
    GitBackup().main()
