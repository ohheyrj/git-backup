import datetime
import logging
import time

import requests

import gitlab
from common.config import Config
from common.sql import Sql
from common.storage import Storage
from common.utils import Utils


class GitlabBackup:
    def __init__(self):
        logging.getLogger(__name__)
        self.sql = Sql()
        self.storage = Storage()

        self.utils = Utils()
        self.utils.create_working_dir()

        self.gitlab_config = Config().gitlab_config

        self.gitlab_client = gitlab.Gitlab(private_token=self.gitlab_config['private_token'])

        try:
            logging.info('Attempting auth to Gitlab')
            self.gitlab_client.auth()
        except gitlab.exceptions.GitlabAuthenticationError as err:
            logging.error(f'Error with Gitlab auth: {err}')
            raise

    def get_projects(self):
        return self.gitlab_client.projects.list(all=True, owned=True)

    def get_latest_commit(self, project) -> str:
        """Get the latest commit of the gitlab project.

        Args:
            project: The project entity used to get the commit.

        Returns:
            str: The latest commit ID.
        """
        logging.info('Looking up commits from project %s', project.id)

        url = f'https://gitlab.com/api/v4/projects/{project.id}/repository/commits?all=True&order=topo&per_page=1&page=1' # pylint: disable=line-too-long

        headers = {
            'PRIVATE-TOKEN': self.gitlab_config['private_token']
        }

        request_response = requests.get(url, headers=headers)

        return request_response.json()[0]['id']

    def export_project(self, project):
        logging.info('Exporting project %s', project.name)

        project_data = self.gitlab_client.projects.get(project.id)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"gitlab_{project.id}_{timestamp}.tgz"

        project_export = project_data.exports.create()
        project_export.refresh()

        while project_export.export_status != 'finished':
            time.sleep(1)
            project_export.refresh()

        with open(f'{self.utils.working_dir_name}/{filename}', 'wb') as export_file:
            logging.info(f'Saving export: {filename}')
            project_export.download(streamed=True, action=export_file.write)
            return filename

    def main(self):
        logging.info('Gitlab enabled, starting Gitlab backup')

        gitlab_projects = self.get_projects()

        proj_count = 1

        for project in gitlab_projects:
            logging.info('Gitlab project %s of %s', proj_count, len(gitlab_projects))

            last_commit = self.get_latest_commit(project)
            commit_in_db = self.sql.find_last_commit_id('gitlab', project.id)

            if last_commit != commit_in_db:
                logging.info('Commits do not match, backup required')

                export_file = self.export_project(project)

                file_to_upload = f'{self.utils.working_dir_name}/{export_file}'
                self.storage.upload_file(
                    file_to_upload,
                    f'gitlab/{project.path_with_namespace}/{export_file}')

                self.sql.add_commit_to_db('gitlab', project.id, last_commit)

            proj_count += 1
        self.utils.remove_tmp_dir()
