{%- from "keystone/map.jinja" import server with context %}

keystone_task_service_stopped:
  test.show_notification:
    - text: "Running keystone.upgrade.service_stopped"

{%- if server.enabled %}
keystone_service_stopped:
  service.dead:
  - name: {{ server.service_name }}
  - enable: False
{%- endif %}
