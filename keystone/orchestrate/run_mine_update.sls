{%- from "keystone/map.jinja" import server with context %}
applying_run_mine_update_state:
  test.succeed_without_changes
{% if server.tokens.get('fernet_rotation_driver', 'shared_filesystem') == 'rsync' %}
execute_mine_update:
  module.run:
    - name: mine.update
{%- endif %}
