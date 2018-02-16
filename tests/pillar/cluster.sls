keystone:
  server:
    enabled: true
    version: liberty
    service_token: token
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
      host: 127.0.0.1
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
    message_queue:
      engine: rabbitmq
      host: 127.0.0.1
      port: 5672
      user: openstack
      password: passw0rd
      virtual_host: '/openstack'
      ha_queues: true
    cache:
      engine: memcached
      members:
      - host: 127.0.0.1
        port: 11211
      - host: 127.0.0.1
        port: 11211
      - host: 127.0.0.1
        port: 11211
    domain:
      test:
        description: "Test domain"
        identity:
          list_limit: 20
    extra_config:
      federation:
        cache_group_membership_in_db: true
