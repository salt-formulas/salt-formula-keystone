{%- from "keystone/map.jinja" import server with context %}

keystone_task_service_running:
  test.show_notification:
    - text: "Running keystone.upgrade.service_running"

{%- if server.enabled %}

keystone_service:
  service.running:
  - enable: True
  - name: {{ server.service_name }}
{%- endif %}
