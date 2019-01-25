# -*- coding: utf-8 -*- #

import os
import pickle
import requests
import pandas as pd

BASE_URL = 'https://dataapi.octoparse.com/'

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
        if os.path.exists(self._token_file):
            with open(self._token_file, 'rb') as token:
                self.token_entity = pickle.load(token)
        else:
            self.log_in()

    def _save_token_file(self):
        with open(self._token_file, 'wb') as token:
            pickle.dump(self.token_entity, token)

    def log_in(self):
        """
        Login & get a access token
        :return: token entity
        """

        username = input("Enter Octoparse Username: ")
        password = input('Password: ')
        content = 'username={0}&password={1}&grant_type=password'.format(username, password)
        token_entity = requests.post(self.base_url + 'token', data=content).json()

        if 'access_token' in token_entity:
            self.token_entity = token_entity
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

    def _post_request(self, path, token, body=''):
        res = requests.post(self.base_url + path, headers={'Authorization': 'bearer ' + token}, data=body)
        if res.status_code == 200:
            pass
        else:
            pass
        return res.json()

    def _get_request(self, path, token):
        res = requests.get(self.base_url + path, headers={'Authorization': 'bearer ' + token})
        if res.status_code == 200:
            pass
        else:
            pass
        return res.json()

    def get_data(self, task_id, size=1000):
        """
        Fetch data for a task id

        :param task_id: octoparse task id
        :param size: chunk size to be fetched in each request
        :return: list of data dict
        """

        offset = 0
        data_list = []

        while True:
            url = 'api/alldata/GetDataOfTaskByOffset?taskId={}&offset={}&size={}'.format(task_id, offset, size)

            data = self._get_request(url, self.token_entity['access_token'])

            data_list += data['data']['dataList']

            if data['data']['restTotal'] != 0:
                offset = data['data']['offset']
            else:
                break
        return data_list

    def get_data_df(self, task_id):
        """
        Fetch data for a task id & returns it as pandas.DataFrame
        :param task_id: octoparse task id
        :return: pandas.DataFrame data
        """

        data = self.get_data(task_id)
        df = pd.DataFrame.from_dict(data)
        df = df[list(data[0].keys())]

        return df

    def clear_data(self, task_id):
        """
        Clear data of a task
        :param task_id: octoparse task id
        :return: response from api
        """

        url = 'api/task/removeDataByTaskId?taskId=' + task_id
        response = self._post_request(url, self.token_entity['access_token'])
        return response



