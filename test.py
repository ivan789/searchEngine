#!/usr/bin/env python
import os
import shutil

#!/usr/bin/env python

import os
import shutil

BASE_DIR = os.path.abspath(__file__)
print(BASE_DIR)

for root, dirs, files in os.walk(BASE_DIR):
    for directory in dirs:
        if directory == '__pycache__':
            shutil.rmtree(os.path.join(root, directory))
