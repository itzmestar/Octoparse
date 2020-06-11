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

# get data for a task with task id: 'abcd-1234-djfsd-dfdf'
data = octo.get_task_data(task_id='abcd-1234-djfsd-dfdf')

# get task data as a pandas.DataFrame for a task with task id: 'abcd-1234-djfsd-dfdf'
df = octo.get_task_data_df(task_id='abcd-1234-djfsd-dfdf')

# clear data for a task with task id: 'abcd-1234-djfsd-dfdf'
octo.clear_task_data(task_id='abcd-1234-djfsd-dfdf')
```