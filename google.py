import os
import time

file_path = 'data/trash_db.json'
last_modified_time = os.path.getmtime(file_path)
readable_time = time.ctime(last_modified_time)
print(f"Last modified time of '{file_path}': {readable_time}")
