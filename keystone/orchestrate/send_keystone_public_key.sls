{%- from "keystone/map.jinja" import server with context %}
applying_send_keystone_public_key_state:
  test.succeed_without_changes
{% if server.tokens.get('fernet_rotation_driver', 'shared_filesystem') == 'rsync' %}
mine_send_keystone_public_key:
   module.run:
    - name: mine.send
    - func: keystone_public_key
    - args:
      - 'cat /var/lib/keystone/.ssh/id_rsa.pub'
    - kwargs:
       mine_function: cmd.run
{%- endif %}
