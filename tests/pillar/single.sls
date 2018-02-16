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
    extra_config:
      federation:
        cache_group_membership_in_db: true
    #message_queue:
      #engine: rabbitmq
      #host: 127.0.0.1
      #port: 5672
      #user: openstack
      #password: password
      #virtual_host: '/openstack'
      #ha_queues: true
# Client state
  client:
    enabled: false
    server:
      identity:
        admin:
          host: localhost
          port: 35357
          token: RANDOMSTRINGTOKEN
        roles:
        - admin
        - Member
        project:
          service:
            description: "OpenStack Service tenant"
          admin:
            description: "OpenStack Admin tenant"
            user:
              admin:
                is_admin: true
                password: passw0rd
                email: admin@localhost
        service:
          keystone3:
            type: identity
            description: OpenStack Identity Service v3
            endpoints:
            - region: RegionOne
              public_address: keystone
              public_protocol: http
              public_port: 5000
              public_path: '/v3'
              internal_address: keystone
              internal_port: 5000
              internal_path: '/v3'
              admin_address: keystone
              admin_port: 35357
              admin_path: '/v3'
          keystone:
            type: identity
            description: OpenStack Identity Service
            endpoints:
            - region: RegionOne
              public_address: keystone
              public_protocol: http
              public_port: 5000
              public_path: '/v2.0'
              internal_address: keystone
              internal_port: 5000
              internal_path: '/v2.0'
              admin_address: keystone
              admin_port: 35357
              admin_path: '/v2.0'
          # TODO: enable once salt keystone module/states are fixed
          #keystoneR2:
            #service: keystone
            #type: identity
            #description: OpenStack Identity Service
            #endpoints:
            #- region: RegionTwo
              #public_address: keystone
              #public_protocol: http
              #public_port: 5000
              #public_path: '/v2.0'
              #internal_address: keystone
              #internal_port: 5000
              #internal_path: '/v2.0'
              #admin_address: keystone
              #admin_port: 35357
              #admin_path: '/v2.0'
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
