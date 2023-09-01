my_module.py

#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True)
        )
    )

    name = module.params['name']
    message = f"Hello, {name}!"

    result = dict(
        message=message
    )

    module.exit_json(changed=False, meta=result)

if __name__ == '__main__':
    main()

#test_my_module.py


import unittest
import sys
import os
from unittest.mock import patch

# Add the directory containing your Ansible module to sys.path
module_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(module_dir)

from my_module import main

class TestMyModule(unittest.TestCase):
    def test_hello_world(self):
        test_name = "World"

        with patch.object(main, 'AnsibleModule', autospec=True) as mock_module:
            mock_instance = mock_module.return_value
            mock_instance.params = {'name': test_name}

            main.main()

            mock_instance.exit_json.assert_called_once_with(
                changed=False,
                meta={'message': f"Hello, {test_name}!"}
            )

if __name__ == '__main__':
    unittest.main()
