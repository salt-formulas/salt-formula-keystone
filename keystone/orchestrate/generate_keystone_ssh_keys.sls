{%- from "keystone/map.jinja" import server with context %}
applying_generate_keystone_ssh_keys_state:
  test.succeed_without_changes
{% if server.tokens.get('fernet_rotation_driver', 'shared_filesystem') == 'rsync' %}
keystone_fernet_keys:
  file.directory:
  - name: {{ server.tokens.location }}
  - mode: 750
  - user: keystone
  - group: keystone

generate_keystone_ssh_keys:
  cmd.run:
    - name: ssh-keygen -q -N '' -f /var/lib/keystone/.ssh/id_rsa
    - runas: keystone
    - creates: /var/lib/keystone/.ssh/id_rsa
    - require:
      - file: {{ server.tokens.location }}
{%- endif %}
