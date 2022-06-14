import configparser

from .args import Args


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.args = Args()
        self.config.read(self.args.config_file)

    @property
    def gitlab_config(self):
        return self.config['gitlab']

    @property
    def github_config(self):
        return self.config['github']

    @property
    def db_config(self):
        return self.config['db']

    @property
    def general_config(self):
        return self.config['general']

    @property
    def s3_config(self):
        return self.config['s3']
