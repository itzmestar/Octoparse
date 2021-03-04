from octoparse import Octoparse
import os
import pytest
import pandas as pd
import responses

BASE_URL = 'https://dataapi.octoparse.com/'
OCTOPARSE_USERNAME = 'myuser'
OCTOPARSE_PASSWORD = 'mypass'

TOKEN_ENTITY = {'access_token': '656kdjfdkjf-SkjfdJFDlererrtrtpfP',
                'token_type': 'bearer',
                'expires_in': 99999,
                'refresh_token': '343j656jh234jh343jhjh3j56jhjh45'
                }


@pytest.fixture
def octoparse(monkeypatch):
    monkeypatch.setenv("OCTOPARSE_USERNAME", OCTOPARSE_USERNAME)
    monkeypatch.setenv("OCTOPARSE_PASSWORD", OCTOPARSE_PASSWORD)
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.POST, BASE_URL + 'token',
                 json=TOKEN_ENTITY, status=200,
                 match=[
                     responses.urlencoded_params_matcher({"username": OCTOPARSE_USERNAME,
                                                          "password": OCTOPARSE_PASSWORD,
                                                          "grant_type": "password"})
                 ])

        yield Octoparse()
        os.remove('octoparse_token.pickle')


def test_refresh_token(octoparse):
    """
    Test refresh_token
    """
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.POST, BASE_URL + 'token',
                 json=TOKEN_ENTITY, status=200,
                 match=[
                     responses.urlencoded_params_matcher({"refresh_token": TOKEN_ENTITY['refresh_token'],
                                                          "grant_type": "refresh_token"})
                 ])
        token = octoparse.refresh_token()
        assert token == TOKEN_ENTITY['access_token']
    assert True


def test_list_all_task_groups(octoparse):
    """
    Test list_all_task_groups
    """
    TASK_GROUP = [{'taskGroupId': 12345, 'taskGroupName': 'MyGroup'},
                  {'taskGroupId': 67890, 'taskGroupName': 'TestGroup'}]

    RESP_DATA = {"data": TASK_GROUP,
                 "error": "success",
                 "error_Description": "Operation successes."
                 }

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.GET, BASE_URL + 'api/taskgroup',
                 json=RESP_DATA, status=200
                 )
        group = octoparse.list_all_task_groups()
        assert group == TASK_GROUP


# @pytest.mark.skip(reason="no way of currently testing this")
def test_list_all_tasks_in_group(octoparse):
    """
    Test list_all_tasks_in_group
    :return:
    """
    GROUP_ID = 12345
    TASKS = [{'taskId': 'a08f6125-e2b5-3878-0c90-ded1ed971349', 'taskName': 'First Task'},
             {'taskId': 'f7c6a7e9-6f43-f25e-b131-8c5208a1dc02', 'taskName': 'Second Task'}]
    RESP_DATA = {"data": TASKS,
                 "error": "success",
                 "error_Description": "Operation successes."
                 }
    path = BASE_URL + 'api/task?taskgroupId={}'.format(GROUP_ID)
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.GET, path,
                 json=RESP_DATA, status=200
                 )
        tasks = octoparse.list_all_tasks_in_group(group_id=GROUP_ID)
        assert tasks == TASKS


# @pytest.mark.skip(reason="no way of currently testing this")
def test_get_task_data(octoparse):
    """
        Test get_task_data
    """
    TASK_ID = "a08f6125-e2b5-3878-5690-ded1ed971349"
    dataList = [
      {
        "state": "Texas",
        "city": "Plano"
      },
      {
        "state": "Texas",
        "city": "Houston"
      },
      {
        "state": "Texas",
        "city": "Austin"
      },
      {
        "state": "Texas",
        "city": "Arlington"
      }
    ]
    RESP_DATA = {"data": {"offset": 0, "total": 4, "restTotal": 0,
                          "dataList": dataList}, 'error': 'success', 'error_Description': 'Operation successes.'}
    path = BASE_URL + 'api/alldata/GetDataOfTaskByOffset?taskId={}&offset=0&size=1000'.format(TASK_ID)
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.GET, path,
                 json=RESP_DATA, status=200
                 )
        data = octoparse.get_task_data(task_id=TASK_ID)
        assert data == dataList


# @pytest.mark.skip(reason="no way of currently testing this")
def test_get_task_data_df(octoparse):
    """
        Test get_task_data
    """
    TASK_ID = "a08f6125-e2b5-3878-5690-ded1ed971349"
    dataList = [
      {
        "state": "Texas",
        "city": "Plano"
      },
      {
        "state": "Texas",
        "city": "Houston"
      },
      {
        "state": "Texas",
        "city": "Austin"
      },
      {
        "state": "Texas",
        "city": "Arlington"
      }
    ]
    RESP_DATA = {"data": {"offset": 0, "total": 4, "restTotal": 0,
                          "dataList": dataList}, 'error': 'success', 'error_Description': 'Operation successes.'}
    path = BASE_URL + 'api/alldata/GetDataOfTaskByOffset?taskId={}&offset=0&size=1000'.format(TASK_ID)
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.GET, path,
                 json=RESP_DATA, status=200
                )
        data_df = octoparse.get_task_data_df(task_id=TASK_ID)
        df = pd.DataFrame.from_dict(dataList)
        assert df.equals(data_df)


def test_get_data_by_offset(octoparse):
    """
        Test get_data_by_offset
    """
    TASK_ID = "a08f6125-e2b5-3878-5690-ded1ed971349"
    dataList = [
        {
            "state": "Texas",
            "city": "Plano"
        },
        {
            "state": "Texas",
            "city": "Houston"
        },
        {
            "state": "Texas",
            "city": "Austin"
        },
        {
            "state": "Texas",
            "city": "Arlington"
        }
    ]
    RESP_DATA = {"data": {"offset": 2, "total": 4, "restTotal": 6,
                          "dataList": dataList}, 'error': 'success', 'error_Description': 'Operation successes.'}
    path = BASE_URL + 'api/alldata/GetDataOfTaskByOffset?taskId={}&offset=2&size=4'.format(TASK_ID)
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.GET, path,
                 json=RESP_DATA, status=200
                 )
        data = octoparse.get_data_by_offset(task_id=TASK_ID, offset=2, size=4)
        assert data == dataList


#@pytest.mark.skip(reason="no way of currently testing this")
def test_clear_task_data(octoparse):
    """
        Test clear_task_data
    """
    task_id = "a08f6125-e2b5-3878-5690-ded1ed971349"
    path = BASE_URL + 'api/task/removeDataByTaskId?taskId={}'.format(task_id)
    RESP_DATA = {'error': 'success', 'error_Description': 'Data of the task has been cleared!'}
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.POST, path,
                 json=RESP_DATA, status=200
                 )
        resp = octoparse.clear_task_data(task_id=task_id)
        assert resp == RESP_DATA


# @pytest.mark.skip(reason="no way of currently testing this")
def test_is_task_running(octoparse):
    """
    Test is_task_running
    """
    TASK_ID = "a08f6125-e2b5-3878-5690-ded1ed971349"
    dataList = [
      {
        "state": "Texas",
        "city": "Plano"
      },
      {
        "state": "Texas",
        "city": "Houston"
      },
      {
        "state": "Texas",
        "city": "Austin"
      },
      {
        "state": "Texas",
        "city": "Arlington"
      }
    ]
    RESP_DATA = {"data": {"offset": 0, "total": 4, "restTotal": 0,
                          "dataList": dataList}, 'error': 'success', 'error_Description': 'Operation successes.'}
    path = BASE_URL + 'api/alldata/GetDataOfTaskByOffset?taskId={}&offset=0&size=10'.format(TASK_ID)
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.GET, path,
                 json=RESP_DATA, status=200,
                 )
        running = octoparse.is_task_running(task_id=TASK_ID)
        assert running is False


# @pytest.mark.skip(reason="no way of currently testing this")
def test_get_not_exported_data(octoparse):
    """
    Test get_not_exported_data
    """
    TASK_ID = "a08f6125-e2b5-3878-5690-ded1ed971349"
    dataList = [
      {
        "state": "Texas",
        "city": "Plano"
      },
      {
        "state": "Texas",
        "city": "Houston"
      },
      {
        "state": "Texas",
        "city": "Austin"
      },
      {
        "state": "Texas",
        "city": "Arlington"
      }
    ]
    RESP_DATA = {"data": {"total": 4, "currentTotal": 4,
                          "dataList": dataList}, 'error': 'success', 'error_Description': 'Operation successes.'}
    path = BASE_URL + 'api/notexportdata/gettop?taskId={}&size=1000'.format(TASK_ID)
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.GET, path,
                 json=RESP_DATA, status=200,
                 )
        data = octoparse.get_not_exported_data(task_id=TASK_ID)
        assert data == RESP_DATA['data']


# @pytest.mark.skip(reason="no way of currently testing this")
def test_update_data_status(octoparse):
    """
    Test update_data_status
    :return:
    """
    task_id = "a08f6125-e2b5-3878-5690-ded1ed971349"
    resp_data = {'error': 'success', 'error_Description': 'Operation successes.'}
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:
        rsps.add(responses.POST, BASE_URL + 'api/notexportdata/update?taskId={}'.format(task_id),
                 json=resp_data, status=200
                 )
        resp = octoparse.update_data_status(task_id=task_id)
        assert resp == resp_data
