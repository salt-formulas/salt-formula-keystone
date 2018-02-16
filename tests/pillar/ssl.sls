# Test case with enabled SSL of the following communication paths:
# - messaging (rabbitmq)

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
      ssl:
        enabled: True
    tokens:
      engine: cache
      expiration: 86400
      location: /etc/keystone/fernet-keys/
    notification: true
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
      port: 5671
      user: openstack
      password: passw0rd
      virtual_host: '/openstack'
      ha_queues: true
      ssl:
        enabled: True
    cache:
      engine: memcached
      members:
      - host: 127.0.0.1
        port: 11211
      - host: 127.0.0.1
        port: 11211
      - host: 127.0.0.1
        port: 11211
