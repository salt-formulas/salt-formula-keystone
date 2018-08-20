{%- from "keystone/map.jinja" import client with context %}

keystone_upgrade_verify_api:
  test.show_notification:
    - text: "Running keystone.upgrade.verify.api"

{%- if client.enabled and client.get('os_client_config', {}).get('enabled', False)  %}

{%- set Keystone_Test_Project = 'TestProject' %}
{%- set Keystone_Test_User = 'TestKeystoneUser' %}

keystonev3_project_present:
  keystonev3.project_present:
  - name: {{ Keystone_Test_Project }}
  - cloud_name: admin_identity
  - domain_id: default

keystonev3_user_present:
  keystonev3.user_present:
  - name: {{ Keystone_Test_User }}
  - cloud_name: admin_identity
  - default_project_id: {{ Keystone_Test_Project }}
  - require:
    - keystonev3_project_present

keystonev3_project_absent:
  keystonev3.project_absent:
  - name: {{ Keystone_Test_Project }}
  - cloud_name: admin_identity
  - require:
    - keystonev3_user_present

keystonev3_user_absent:
  keystonev3.user_absent:
  - name: {{ Keystone_Test_User }}
  - cloud_name: admin_identity
  - require:
    - keystonev3_project_absent
{%- endif %}
