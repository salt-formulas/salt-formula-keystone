{%- from "keystone/map.jinja" import server with context %}

keystone_render_config:
  test.show_notification:
    - text: "Running keystone.upgrade.render_config"

{%- if server.enabled %}
/etc/keystone/keystone.conf:
  file.managed:
  - source: salt://keystone/files/{{ server.version }}/keystone.conf.{{ grains.os_family }}
  - template: jinja

/etc/keystone/keystone-paste.ini:
  file.managed:
  - source: salt://keystone/files/{{ server.version }}/keystone-paste.ini.{{ grains.os_family }}
  - user: keystone
  - group: keystone
  - template: jinja
{%- endif %}
