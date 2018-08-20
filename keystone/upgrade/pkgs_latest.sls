{%- from "keystone/map.jinja" import server,client with context %}

keystone_task_pkg_latest:
  test.show_notification:
    - text: "Running keystone.upgrade.pkg_latest"

policy-rc.d_present:
  file.managed:
    - name: /usr/sbin/policy-rc.d
    - mode: 755
    - contents: |
        #!/bin/sh
        exit 101

{%- set pkgs = [] %}
{%- if server.enabled %}
  {%- do pkgs.extend(server.pkgs) %}
{%- endif %}
{%- if client.get('enabled', false) %}
  {%- do pkgs.extend(client.pkgs) %}
{%- endif %}

{%- for kpkg in pkgs|unique %}
keystone_package_{{ kpkg }}:
  pkg.latest:
  - name: {{ kpkg }}
  - require:
    - file: policy-rc.d_present
  - require_in:
    - file: policy-rc.d_absent
{%- endfor %}

policy-rc.d_absent:
  file.absent:
    - name: /usr/sbin/policy-rc.d
