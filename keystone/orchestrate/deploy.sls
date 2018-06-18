{%- set minions = ((salt['cmd.shell']("salt '*' match.pillar 'keystone:server:role:primary' --out=json --static"))|load_json).values() %}
keystone_ssh_keys:
  salt.state:
    - tgt: 'I@keystone:server:role:primary'
    - tgt_type: compound
    - sls: keystone.orchestrate.generate_keystone_ssh_keys
    - onlyif: {% if True in minions %}/bin/true{% else %}/bin/false{% endif %}

send_keystone_public_key:
  salt.state:
    - tgt: 'I@keystone:server:role:primary'
    - tgt_type: compound
    - sls: keystone.orchestrate.send_keystone_public_key
    - require:
      - salt: keystone_ssh_keys
    - onlyif: {% if True in minions %}/bin/true{% else %}/bin/false{% endif %}

{%- set minions = ((salt['cmd.shell']("salt '*' match.pillar 'keystone:server' --out=json --static"))|load_json).values() %}
salt_mine_update:
  salt.state:
    - tgt: 'I@keystone:server'
    - tgt_type: compound
    - sls: keystone.orchestrate.run_mine_update
    - require:
      - salt: send_keystone_public_key
    - onlyif: {% if True in minions %}/bin/true{% else %}/bin/false{% endif %}

{%- set minions = ((salt['cmd.shell']("salt '*' match.pillar 'keystone:server:role:secondary' --out=json --static"))|load_json).values() %}
get_keystone_public_key:
  salt.state:
    - tgt: 'I@keystone:server:role:secondary'
    - tgt_type: compound
    - sls: keystone.orchestrate.get_keystone_public_key
    - require:
      - salt: salt_mine_update
    - onlyif: {% if True in minions %}/bin/true{% else %}/bin/false{% endif %}
