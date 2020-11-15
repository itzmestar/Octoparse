from octoparse import Octoparse
import os
import pytest
import pandas as pd


class TestOctoparse:
    """
    Test Octoparse class
    """

    def setup(self):
        """
        Test Setup
        """
        self.octo = Octoparse()
        self.group_id = 380697
        self.task_id = 'c8d468a0-fe3e-4b23-959c-d3786eb9d4d8'

    def test_init(self):
        """
        Test initialization
        :return:
        """
        octo = Octoparse()

        # pickle file should exist after login
        assert os.path.isfile(octo._token_file)

    def test_refresh_token(self):
        """
        Test refresh_token
        :return:
        """
        token = self.octo.refresh_token()
        assert type(token) == str

    def test_list_all_task_groups(self):
        """
        Test list_all_task_groups
        :return:
        """
        groups = self.octo.list_all_task_groups()
        assert type(groups) == list
        assert len(groups) > 0

    def test_list_all_tasks_in_group(self):
        """
        Test list_all_tasks_in_group
        :return:
        """
        tasks = self.octo.list_all_tasks_in_group(group_id=self.group_id)
        assert type(tasks) == list
        assert len(tasks) > 0

    def test_get_task_data(self):
        """
        Test get_task_data
        :return:
        """
        data = self.octo.get_task_data(task_id=self.task_id, offset=11000)
        assert type(data) == list

    def test_get_task_data_df(self):
        """
        Test get_task_data_df
        :return:
        """
        df = self.octo.get_task_data_df(task_id=self.task_id)
        assert type(df) == pd.DataFrame

    def test_get_not_exported_data(self):
        """
        Test get_not_exported_data
        :return:
        """

        data = self.octo.get_not_exported_data(task_id=self.task_id)
        assert type(data) == dict

    def test_update_data_status(self):
        """
        Test update_data_status
        :return:
        """

        resp = self.octo.update_data_status(task_id=self.task_id)
        assert resp['error'] == 'success'

    def test_clear_task_data(self):
        """
        Test clear_task_data
        :return:
        """
        resp = self.octo.clear_task_data(task_id=self.task_id)
        assert resp['error'] == 'success'
