{%- from "keystone/map.jinja" import server with context %}
applying_get_keystone_public_key_state:
  test.succeed_without_changes
{% if server.tokens.get('fernet_rotation_driver', 'shared_filesystem') == 'rsync' %}
{%- set authorized_keys = salt['mine.get']('I@keystone:server:role:primary', 'keystone_public_key', 'compound') %}

keystone_fernet_keys:
  file.directory:
  - name: {{ server.tokens.location }}
  - mode: 650
  - user: keystone
  - group: keystone

/var/lib/keystone/.ssh:
  file.directory:
    - user: keystone
    - group: keystone
    - file_mode: 600
    - dir_mode: 600
    - makedirs: True
    - recurse:
      - user
      - group
      - mode

  {% if authorized_keys is defined and authorized_keys|length > 0 %}
put_keystone_file:
  file.managed:
    - name: /var/lib/keystone/.ssh/authorized_keys
    - contents: '{{ authorized_keys.values()[0] }}'
    - user: keystone
    - group: keystone
    - mode: 600
    - require:
      - file: /var/lib/keystone/.ssh
  {%- endif %}
{%- endif %}
