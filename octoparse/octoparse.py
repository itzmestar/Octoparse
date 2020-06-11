# -*- coding: utf-8 -*- #

import os
import pickle
import requests
import pandas as pd
import getpass
from datetime import datetime

BASE_URL = 'https://dataapi.octoparse.com/'

# Helper Methods


def _post_request(url, token, body=None):
    """
    Send a requests.post request
    :param url: URL
    :param token: authorization token
    :param body: body to be sent with request
    :return: json of response
    """
    headers = {
        'Authorization': 'bearer ' + token
    }

    if body is None:
        res = requests.post(url, headers=headers)
    else:
        res = requests.post(url, headers=headers, data=body)
    if res.status_code == 200:
        pass
    else:
        pass
    return res.json()


def _get_request(url, token, params=None):
    """
    Send a requests.get request
    :param self:
    :param path:
    :param token:
    :param params:
    :return:
    """
    headers = {
        'Authorization': 'bearer ' + token
    }
    if params is None:
        res = requests.get(url, headers=headers)
    else:
        res = requests.get(url, headers=headers, params=params)

    if res.status_code == 200:
        pass
    else:
        pass
    return res.json()


class Octoparse:
    """
    Octoparse class to act as octoparse api client.
    All the requests can be made through this class.
    """

    def __init__(self, base_url=BASE_URL):
        """
        :param base_url: url can be changed for advancedapi access
        """
        self.token_entity = None
        self.base_url = base_url
        self._token_file = 'octoparse_token.pickle'
        self._read_token_file()
        self.refresh_token()

    def __del__(self):
        self._save_token_file()

    def _read_token_file(self):
        """
        Read token pickle file from disk
        """
        if os.path.exists(self._token_file):
            with open(self._token_file, 'rb') as token:
                self.token_entity = pickle.load(token)
        else:
            self.log_in()

    def _save_token_file(self):
        """
        Save token pickle file to disk
        """
        with open(self._token_file, 'wb') as token:
            pickle.dump(self.token_entity, token)

    def _get_access_token(self):
        """
        Return the valid access token
        if expired then first refresh the token
        :return: access token string
        """
        if self.token_entity is None:
            self.log_in()
        else:
            # check if token expired
            timedelta = datetime.now() - self.token_entity['datetime']
            if timedelta.total_seconds() > self.token_entity['expires_in']:
                self.refresh_token()
        return self.token_entity['access_token']

    def _get_url(self, path):
        """
        Returns the absolute url
        :param path: relative url path
        :return: absolute url
        """
        return self.base_url + path

    def log_in(self):
        """
        Login & get a access token
        :return: token entity
        """

        username = input("Enter Octoparse Username: ")
        password = getpass.getpass('Password: ')
        content = 'username={0}&password={1}&grant_type=password'.format(username, password)
        token_entity = requests.post(self.base_url + 'token', data=content).json()

        if 'access_token' in token_entity:
            self.token_entity = token_entity
            # add time to token
            self.token_entity['datetime'] = datetime.now()
            self._save_token_file()
            return token_entity
        else:
            exit(1)

    def refresh_token(self):
        """
        refresh the token with refresh token id
        :return: new refreshed token string
        """

        content = 'refresh_token=' + self.token_entity['refresh_token'] + '&grant_type=refresh_token'
        response = requests.post(self.base_url + 'token', data=content)
        if response.status_code == 200:
            token_entity = response.json()
            refresh_token = token_entity.get('access_token', token_entity)
            self.token_entity = token_entity
            self._save_token_file()
            return refresh_token
        else:
            self.log_in()
            return self.token_entity['refresh_token']

    def get_task_data(self, task_id, size=1000):
        """
        Fetch data for a task id

        :param task_id: octoparse task id
        :param size: chunk size to be fetched in each request
        :return: list of data dict
        """

        offset = 0
        data_list = []

        path = 'api/alldata/GetDataOfTaskByOffset'

        while True:
            params = {
                'taskId': task_id,
                'offset': offset,
                'size': size
            }

            data = _get_request(self._get_url(path),
                                self._get_access_token(),
                                params=params
                                )
            data_list += data['data']['dataList']

            if data['data']['restTotal'] != 0:
                offset = data['data']['offset']
            else:
                break
        return data_list

    def get_task_data_df(self, task_id):
        """
        Fetch data for a task id & returns it as pandas.DataFrame
        :param task_id: octoparse task id
        :return: pandas.DataFrame data
        """

        data = self.get_task_data(task_id)
        df = pd.DataFrame.from_dict(data)
        df = df[list(data[0].keys())]

        return df

    def clear_task_data(self, task_id):
        """
        Clear data of a task
        :param task_id: octoparse task id
        :return: response from api
        """

        path = 'api/task/removeDataByTaskId?taskId=' + task_id
        response = _post_request(self._get_url(path), self._get_access_token())
        return response

    def list_all_task_groups(self):
        """
        List All Task Groups
        :return: list -- all task groups
        """

        path = 'api/taskgroup'

        task_groups = list()
        response = _get_request(self._get_url(path), self._get_access_token())

        if 'data' in response:
            task_groups = response['data']
        return task_groups

    def list_all_tasks_in_group(self, group_id):
        """
        List All Tasks in a Group
        :param group_id: a task group id
        :return: list -- all tasks in a group
        """

        path = 'api/task'

        params = {
            'taskgroupId': group_id
        }

        task_list = list()
        response = _get_request(self._get_url(path), self._get_access_token(), params=params)

        if 'data' in response:
            task_list = response['data']
        return task_list

    def get_not_exported_data(self, task_id, size=1000):
        """
        This returns non-exported data. Data will be tagged status = exporting
        (instead of status=exported) after the export.
        This way, the same set of data can be exported multiple times using this method.
        If the user has confirmed receipt of the data and wish to update
        data status to ‘exported’, please call method update_data_status().
        :param task_id: octoparse task id
        :param size: The amount of data rows(range from 1 to 1000)
        :return: json -- task dataList and relevant information
        """

        path = 'api/notexportdata/gettop'

        params = {
            'taskId': task_id,
            'size': size
        }

        data = list()
        response = _get_request(self._get_url(path), self._get_access_token(), params=params)

        if 'data' in response:
            data = response['data']
        return data

    def update_data_status(self, task_id):
        """
        This updates data status from ‘exporting’ to ‘exported’.
        :return: string -- remind message(include error if exists)
        """
        path = 'api/notexportdata/update'

        params = {
            'taskId': task_id
        }
        response = _post_request(self._get_url(path), self._get_access_token(), params=params)

        return response
