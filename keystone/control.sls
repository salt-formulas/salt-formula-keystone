{%- from "keystone/map.jinja" import control with context %}
{%- for provider_name, provider in control.get('provider', {}).items() %}

/root/keystonerc_{{ provider_name }}:
  file.managed:
  - source: salt://keystone/files/keystonerc_user
  - template: jinja
  - defaults:
      provider_name: "{{ provider_name }}"

{%- endfor %}
