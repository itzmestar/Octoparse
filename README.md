# Octoparse

## Unofficial Octoparse api client in python
-----------------------------------------

### Example usage:
```
from octoparse import Octoparse

octo = Octoparse()

# get data for a task with task id: 'abcd-1234-djfsd-dfdf'
data = octo.get_data('abcd-1234-djfsd-dfdf')

# get data as a pandas.DataFrame for a task with task id: 'abcd-1234-djfsd-dfdf'
df = octo.get_data_df('abcd-1234-djfsd-dfdf')

# clear data for a task with task id: 'abcd-1234-djfsd-dfdf'
octo.clear_data('abcd-1234-djfsd-dfdf')
```
