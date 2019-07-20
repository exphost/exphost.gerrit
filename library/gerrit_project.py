#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import json
import requests

def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        username=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        url=dict(type='str', required=True),
        replications=dict(type='list', required=False, default=None),
        init_from=dict(type='str', required=False, default=None),
    )

    result = dict(
        changed=False,
        original_message='',
        message='',
        created=False,
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    s = requests.Session()
    s.auth = (module.params['username'],
              module.params['password'])
    #TODO sprawdzic czy zalogowano
    url = "{url}/a/projects/{name}".format(url=module.params['url'], name=module.params['name'])
    r = s.get(url)
    if r.status_code == 200:
        result['message'] = "repository exists"
    else:
        data = {}
        r = s.put(url, json=data)
        result['changed'] = True
        result['created'] = True

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
