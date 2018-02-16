keystone:
# Server state
  server:
    enabled: true
    version: liberty
    service_token: RANDOMSTRINGTOKEN
    service_tenant: service
    admin_tenant: admin
    admin_name: admin
    admin_password: passw0rd
    admin_email: root@localhost
    bind:
      address: 0.0.0.0
      private_address: 127.0.0.1
      private_port: 35357
      public_address: 127.0.0.1
      public_port: 5000
    region: RegionOne
    database:
      engine: mysql
      host: localhost
      name: keystone
      password: passw0rd
      user: keystone
    tokens:
      engine: cache
      expiration: 86400
      location: /etc/keystone/fernet-keys/
    notification: false
    notification_format: cadf
    logging:
      log_appender: false
      log_handlers:
        watchedfile:
          enabled: true
        fluentd:
          enabled: false
        ossyslog:
          enabled: false
    domain:
      testing:
        description: "Testing domain"
        backend: ldap
        assignment:
          backend: sql
        ldap:
          url: "ldaps://idm.domain.com"
          suffix: "dc=cloud,dc=domain,dc=com"
          uid: keystone
          password: password
# CI related dependencies
mysql:
  client:
    enabled: true
    version: '5.7'
    admin:
      host: localhost
      port: 3306
      user: admin
      password: password
      encoding: utf8
  server:
    enabled: true
    version: "5.7"
    force_encoding: utf8
    bind:
      address: 0.0.0.0
      port: 3306
      protocol: tcp
    database:
      keystone:
        encoding: utf8
        users:
        - host: '%'
          name: keystone
          password: passw0rd
          rights: all
        - host: 127.0.0.1
          name: keystone
          password: passw0rd
          rights: all
