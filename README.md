# Octoparse

## Unofficial Octoparse api client in python
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

# List all task groups
groups = octo.list_all_task_groups()

# List all tasks in a group
tasks = octo.list_all_tasks_in_group(group_id='xxxx-ssdsd-1212')

# Export the not exported data
data = octo.get_not_exported_data(task_id='abcd-1234-djfsd-dfdf', size=100)

# Update data status
res = octo.update_data_status(task_id='abcd-1234-djfsd-dfdf')

# get data for a task with task id: 'abcd-1234-djfsd-dfdf'
data = octo.get_task_data(task_id='abcd-1234-djfsd-dfdf')

# get task data as a pandas.DataFrame for a task with task id: 'abcd-1234-djfsd-dfdf'
df = octo.get_task_data_df(task_id='abcd-1234-djfsd-dfdf')

# clear data for a task with task id: 'abcd-1234-djfsd-dfdf'
octo.clear_task_data(task_id='abcd-1234-djfsd-dfdf')

```
