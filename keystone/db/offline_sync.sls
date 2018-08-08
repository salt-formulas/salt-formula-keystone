{%- from "keystone/map.jinja" import server with context %}

keystone_syncdb:
  cmd.run:
  - name: keystone-manage db_sync && sleep 1
  - timeout: 120
  {%- if grains.get('noservices') or server.get('role', 'primary') == 'secondary' %}
  - onlyif: /bin/false
  {%- endif %}
