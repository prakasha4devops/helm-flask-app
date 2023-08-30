#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec=dict(
            value=dict(type='str', required=True)
        )
    )

    value = module.params['value']
    result = {'original_value': value}
    
    module.exit_json(**result)

if __name__ == '__main__':
    main()

#pip install pytest

import my_module
from ansible.module_utils.basic import AnsibleModule
import pytest

# Mock AnsibleModule class
class MockModule(AnsibleModule):
    def exit_json(self, **kwargs):
        self.result = kwargs

def test_my_module():
    test_value = "test123"
    mock_module = MockModule(argument_spec={'value': {'type': 'str', 'required': True}})
    mock_module.params = {'value': test_value}

    my_module.main()

    assert mock_module.result['original_value'] == test_value

if __name__ == '__main__':
    pytest.main([__file__])
