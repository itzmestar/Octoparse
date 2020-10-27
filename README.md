# Octoparse

## Unofficial Octoparse API client in python

Now with support for Advanced API and China as well
-----------

### Installation:
use pip to install:
``` 
pip install octoparse
```
-----------

### Example usage:
```
from octoparse import Octoparse

# initialize api client
# it will try to log in & ask for credentials if required
octo = Octoparse()

# if using advanced API:
octo = Octoparse(advanced_api=True)

# if using from China:
octo = Octoparse(china=True)

# List all task groups
groups = octo.list_all_task_groups()

# List all tasks in a group
tasks = octo.list_all_tasks_in_group(group_id='xxxx-ssdsd-1212')

# Export the not exported data
data = octo.get_not_exported_data(task_id='abcd-1234-djfsd-dfdf', size=100)

# Update data status
resp = octo.update_data_status(task_id='abcd-1234-djfsd-dfdf')

# get data for a task with task id: 'abcd-1234-djfsd-dfdf'
data = octo.get_task_data(task_id='abcd-1234-djfsd-dfdf')

# get task data as a pandas.DataFrame for a task with task id: 'abcd-1234-djfsd-dfdf'
df = octo.get_task_data_df(task_id='abcd-1234-djfsd-dfdf')

# clear data for a task with task id: 'abcd-1234-djfsd-dfdf'
octo.clear_task_data(task_id='abcd-1234-djfsd-dfdf')

```

### Following are supported for Advanced API
```
# Get Tasks' status
task_list = ['abcd-1234-djfsd-dfdf', 'ab23-5677-djfsd-dfdf']
resp = octo.get_task_status(task_list)

# Get Task's parameter
resp = octo.get_task_param(task_id='abcd-1234-djfsd-dfdf', name='loopAction1.Url')

# Update Task's parameter
resp = octo.update_task_param(task_id='abcd-1234-djfsd-dfdf', name='loopAction1.Url', value='http://xyz.abc')

# Add new URLs/text to an existing loop
resp = octo.add_url_text_to_loop(task_id='abcd-1234-djfsd-dfdf', name='loopAction1.Url', value='http://xyz.abc')

# Start running task
resp = octo.start_task(task_id='abcd-1234-djfsd-dfdf')

# Stop running task
resp = octo.stop_task(task_id='abcd-1234-djfsd-dfdf')
```