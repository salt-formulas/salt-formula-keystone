{%- from "keystone/map.jinja" import server with context %}

keystone_upgrade:
  test.show_notification:
    - text: "Running keystone.upgrade.upgrade"

include:
 - keystone.upgrade.service_stopped
 - keystone.upgrade.pkgs_latest
 - keystone.upgrade.render_config
 - keystone.db.offline_sync
 - keystone.upgrade.service_running
