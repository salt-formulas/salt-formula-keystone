==================
OpenStack Keystone
==================

Keystone provides authentication, authorization and service discovery
mechanisms via HTTP primarily for use by projects in the OpenStack family. It
is most commonly deployed as an HTTP interface to existing identity systems,
such as LDAP.

From Kilo release Keystone v3 endpoint has definition without version in url

.. code-block:: bash

  +----------------------------------+-----------+--------------------------+--------------------------+---------------------------+----------------------------------+
  |                id                |   region  |        publicurl         |       internalurl        |          adminurl         |            service_id            |
  +----------------------------------+-----------+--------------------------+--------------------------+---------------------------+----------------------------------+
  | 91663a8db11c487c9253c8c456863494 | RegionOne | http://10.0.150.37:5000/ | http://10.0.150.37:5000/ | http://10.0.150.37:35357/ | 0fd2dba3153d45a1ba7f709cfc2d69c9 |
  +----------------------------------+-----------+--------------------------+--------------------------+---------------------------+----------------------------------+


Sample pillars
==============

.. caution::

    When you use localhost as your database host (keystone:server:
    atabase:host), sqlalchemy will try to connect to /var/run/mysql/
    mysqld.sock, may cause issues if you located your mysql socket elsewhere

Full stacked keystone

.. code-block:: yaml

    keystone:
      server:
        enabled: true
        version: juno
        service_token: 'service_tokeen'
        service_tenant: service
        service_password: 'servicepwd'
        admin_tenant: admin
        admin_name: admin
        admin_password: 'adminpwd'
        admin_email: stackmaster@domain.com
        roles:
          - admin
          - Member
          - image_manager
        bind:
          address: 0.0.0.0
          private_address: 127.0.0.1
          private_port: 35357
          public_address: 127.0.0.1
          public_port: 5000
        api_version: 2.0
        region: RegionOne
        database:
          engine: mysql
          host: '127.0.0.1'
          name: 'keystone'
          password: 'LfTno5mYdZmRfoPV'
          user: 'keystone'

Keystone public HTTPS API

.. code-block:: yaml

    keystone:
      server:
        enabled: true
        version: juno
        ...
        services:
        - name: nova
          type: compute
          description: OpenStack Compute Service
          user:
            name: nova
            password: password
          bind:
            public_address: cloud.domain.com
            public_protocol: https
            public_port: 8774
            internal_address: 10.0.0.20
            internal_port: 8774
            admin_address: 10.0.0.20
            admin_port: 8774

Keystone with custom policies. Keys with specified rules are created or set to this value if they already exists. Keys with no value (like our "existing_rule") are deleted from the policy file.

.. code-block:: yaml

    keystone:
      server:
        enabled: true
        policy:
          new_rule: "rule:admin_required"
          existing_rule:

Keystone memcached storage for tokens

.. code-block:: yaml

    keystone:
      server:
        enabled: true
        version: juno
        ...
        token_store: cache
        cache:
          engine: memcached
          host: 127.0.0.1
          port: 11211
        services:
        ...

Keystone clustered memcached storage for tokens

.. code-block:: yaml

    keystone:
      server:
        enabled: true
        version: juno
        ...
        token_store: cache
        cache:
          engine: memcached
          members:
          - host: 192.160.0.1
            port: 11211
          - host: 192.160.0.2
            port: 11211
        services:
        ...

Keystone client

.. code-block:: yaml

    keystone:
      client:
        enabled: true
        server:
          host: 10.0.0.2
          public_port: 5000
          private_port: 35357
          service_token: 'token'
          admin_tenant: admin
          admin_name: admin
          admin_password: 'passwd'

Keystone cluster

.. code-block:: yaml

    keystone:
      control:
        enabled: true
        provider:
          os15_token:
            host: 10.0.0.2
            port: 35357
            token: token
          os15_tcp_core_stg:
            host: 10.0.0.5
            port: 5000
            tenant: admin
            name: admin
            password: password

Keystone fernet tokens for OpenStack Kilo release

.. code-block:: yaml

    keystone:
      server:
        ...
        tokens:
          engine: fernet
          max_active_keys: 3
        ...

Keystone auth methods

.. code-block:: yaml

    keystone:
      server:
        ...
        auth_methods:
        - external
        - password
        - token
        - oauth1
        ...

Keystone domain with LDAP backend, using SQL for role/project assignment

.. code-block:: yaml

    keystone:
      server:
        domain:
          external:
            description: "Testing domain"
            backend: ldap
            assignment:
              backend: sql
            ldap:
              url: "ldaps://idm.domain.com"
              suffix: "dc=cloud,dc=domain,dc=com"
              # Will bind as uid=keystone,cn=users,cn=accounts,dc=cloud,dc=domain,dc=com
              uid: keystone
              password: password

Using LDAP backend for default domain

.. code-block:: yaml

    keystone:
      server:
        backend: ldap
        assignment:
          backend: sql
        ldap:
          url: "ldaps://idm.domain.com"
          suffix: "dc=cloud,dc=domain,dc=com"
          # Will bind as uid=keystone,cn=users,cn=accounts,dc=cloud,dc=domain,dc=com
          uid: keystone
          password: password

Simple service endpoint definition (defaults to RegionOne)

.. code-block:: yaml

    keystone:
      server:
        service:
          ceilometer:
            type: metering
            description: OpenStack Telemetry Service
            user:
              name: ceilometer
              password: password
            bind:
              ...

Region-aware service endpoints definition

.. code-block:: yaml

    keystone:
      server:
        service:
          ceilometer_region01:
            service: ceilometer
            type: metering
            region: region01
            description: OpenStack Telemetry Service
            user:
              name: ceilometer
              password: password
            bind:
              ...
          ceilometer_region02:
            service: ceilometer
            type: metering
            region: region02
            description: OpenStack Telemetry Service
            bind:
              ...

Enable ceilometer notifications

.. code-block:: yaml

    keystone:
      server:
        notification: true
        message_queue:
          engine: rabbitmq
          host: 127.0.0.1
          port: 5672
          user: openstack
          password: password
          virtual_host: '/openstack'
          ha_queues: true

Client-side RabbitMQ HA setup

.. code-block:: yaml

    keystone:
      server:
        ....
        message_queue:
          engine: rabbitmq
          members:
            - host: 10.0.16.1
            - host: 10.0.16.2
            - host: 10.0.16.3
          user: openstack
          password: pwd
          virtual_host: '/openstack'
        ....

Client-side RabbitMQ TLS configuration:

|

By default system-wide CA certs are used. Nothing should be specified except `ssl.enabled`.

.. code-block:: yaml

  keystone:
    server:
      ....
      message_queue:
        ssl:
          enabled: True

Use `cacert_file` option to specify the CA-cert file path explicitly:

.. code-block:: yaml

  keystone:
    server:
      ....
      message_queue:
        ssl:
          enabled: True
          cacert_file: /etc/ssl/rabbitmq-ca.pem

To manage content of the `cacert_file` use the `cacert` option:

.. code-block:: yaml

  keystone:
    server:
      ....
      message_queue:
        ssl:
          enabled: True
          cacert: |

          -----BEGIN CERTIFICATE-----
                    ...
          -----END CERTIFICATE-------

          cacert_file: /etc/openstack/rabbitmq-ca.pem


Notice:
 * The `message_queue.port` is set to **5671** (AMQPS) by default if `ssl.enabled=True`.
 * Use `message_queue.ssl.version` if you need to specify protocol version. By default is TLSv1 for python < 2.7.9 and TLSv1_2 for version above.

Enable CADF audit notification

.. code-block:: yaml

    keystone:
      server:
        notification: true
        notification_format: cadf

Run keystone under Apache

.. code-block:: yaml

    keystone:
      server:
        service_name: apache2
    apache:
      server:
        enabled: true
        default_mpm: event
        site:
          keystone:
            enabled: true
            type: keystone
            name: wsgi
            host:
              name: ${linux:network:fqdn}
        modules:
          - wsgi

Enable SAML2 Federated keystone

.. code-block:: yaml

    keystone:
      server:
        auth_methods:
        - password
        - token
        - saml2
        federation:
          saml2:
            protocol: saml2
            remote_id_attribute: Shib-Identity-Provider
            shib_url_scheme: https
            shib_compat_valid_user: 'on'
          federation_driver: keystone.contrib.federation.backends.sql.Federation
          federated_domain_name: Federated
          trusted_dashboard:
            - https://${_param:cluster_public_host}/horizon/auth/websso/
    apache:
      server:
        pkgs:
          - apache2
          - libapache2-mod-shib2
        modules:
          - wsgi
          - shib2

Enable OIDC Federated keystone

.. code-block:: yaml

    keystone:
      server:
        auth_methods:
        - password
        - token
        - oidc
        federation:
        oidc:
            protocol: oidc
            remote_id_attribute: HTTP_OIDC_ISS
            remote_id_attribute_value: https://accounts.google.com
            oidc_claim_prefix: "OIDC-"
            oidc_response_type: id_token
            oidc_scope: "openid email profile"
            oidc_provider_metadata_url: https://accounts.google.com/.well-known/openid-configuration
            oidc_client_id: <openid_client_id>
            oidc_client_secret: <openid_client_secret>
            oidc_crypto_passphrase: openstack
            oidc_redirect_uri: https://key.example.com:5000/v3/auth/OS-FEDERATION/websso/oidc/redirect
            oidc_oauth_introspection_endpoint: https://www.googleapis.com/oauth2/v1/tokeninfo
            oidc_oauth_introspection_token_param_name: access_token
            oidc_oauth_remote_user_claim: user_id
            oidc_ssl_validate_server: 'off'
        federated_domain_name: Federated
        federation_driver: keystone.contrib.federation.backends.sql.Federation
        trusted_dashboard:
          - https://${_param:cluster_public_host}/auth/websso/
    apache:
      server:
        pkgs:
          - apache2
          - libapache2-mod-auth-openidc
        modules:
          - wsgi
          - auth_openidc

Notes: Ubuntu Trusty repository doesn't contain libapache2-mod-auth-openidc package. Additonal repository should be added to source list.

Use a custom identity driver with custom options

.. code-block:: yaml

    keystone:
      server:
        backend: k2k
        k2k:
          auth_url: 'https://keystone.example.com/v2.0'
          read_user: 'example_user'
          read_pass: 'password'
          read_tenant_id: 'admin'
          identity_driver: 'sql'
          id_prefix: 'k2k:'
          domain: 'default'
          caching: true
          cache_time: 600

Enable CORS parameters

.. code-block:: yaml

    keystone:
      server:
        cors:
          allowed_origin: https:localhost.local,http:localhost.local
          expose_headers: X-Auth-Token,X-Openstack-Request-Id,X-Subject-Token
          allow_methods: GET,PUT,POST,DELETE,PATCH
          allow_headers: X-Auth-Token,X-Openstack-Request-Id,X-Subject-Token
          allow_credentials: True
          max_age: 86400



Keystone client
---------------

Service endpoints enforcement with service token

.. code-block:: yaml

    keystone:
      client:
        enabled: true
        server:
          keystone01:
            admin:
              host: 10.0.0.2
              port: 35357
              token: 'service_token'
            service:
              nova:
                type: compute
                description: OpenStack Compute Service
                endpoints:
                - region: region01
                  public_address: 172.16.10.1
                  public_port: 8773
                  public_path: '/v2'
                  internal_address: 172.16.10.1
                  internal_port: 8773
                  internal_path: '/v2'
                  admin_address: 172.16.10.1
                  admin_port: 8773
                  admin_path: '/v2'

Project, users, roles enforcement with admin user

.. code-block:: yaml

    keystone:
      client:
        enabled: true
        server:
          keystone01:
            admin:
              host: 10.0.0.2
              port: 5000
              project: admin
              user: admin
              password: 'passwd'
              region_name: RegionOne
              protocol: https
            roles:
            - admin
            - member
            project:
              tenant01:
                description: "test env"
                quota:
                  instances: 100
                  cores: 24
                  ram: 151200
                  floating_ips: 50
                  fixed_ips: -1
                  metadata_items: 128
                  injected_files: 5
                  injected_file_content_bytes: 10240
                  injected_file_path_bytes: 255
                  key_pairs: 100
                  security_groups: 20
                  security_group_rules: 40
                  server_groups: 20
                  server_group_members: 20
                user:
                  user01:
                    email: jdoe@domain.com
                    is_admin: true
                    password: some
                  user02:
                    email: jdoe2@domain.com
                    password: some
                    roles:
                    - custom-roles

Multiple servers example

.. code-block:: yaml

    keystone:
      client:
        enabled: true
        server:
          keystone01:
            admin:
              host: 10.0.0.2
              port: 5000
              project: 'admin'
              user: admin
              password: 'workshop'
              region_name: RegionOne
              protocol: https
          keystone02:
            admin:
              host: 10.0.0.3
              port: 5000
              project: 'admin'
              user: admin
              password: 'workshop'
              region_name: RegionOne


Tenant quotas

.. code-block:: yaml

    keystone:
      client:
        enabled: true
        server:
          keystone01:
            admin:
              host: 10.0.0.2
              port: 5000
              project: admin
              user: admin
              password: 'passwd'
              region_name: RegionOne
              protocol: https
            roles:
            - admin
            - member
            project:
              tenant01:
                description: "test env"
                quota:
                  instances: 100
                  cores: 24
                  ram: 151200
                  floating_ips: 50
                  fixed_ips: -1
                  metadata_items: 128
                  injected_files: 5
                  injected_file_content_bytes: 10240
                  injected_file_path_bytes: 255
                  key_pairs: 100
                  security_groups: 20
                  security_group_rules: 40
                  server_groups: 20
                  server_group_members: 20

Extra config params in keystone.conf (since Mitaka release)

.. code-block:: yaml

    keystone:
      server:
        ....
        extra_config:
          ini_section1:
            param1: value
            param2: value
          ini_section2:
            param1: value
            param2: value
        ....

Configuration of policy.json file

.. code-block:: yaml


    keystone:
      server:
        ....
        policy:
          admin_or_token_subject: 'rule:admin_required or rule:token_subject'

Setting up default admin project name and domain

.. code-block:: yaml


    keystone:
      server:
        ....
        admin_project:
          name: "admin"
          domain: "default"

Usage
=====

Apply state `keystone.client.service` first and then `keystone.client` state.


Documentation and Bugs
======================

To learn how to deploy OpenStack Salt, consult the documentation available
online at:

    https://wiki.openstack.org/wiki/OpenStackSalt

In the unfortunate event that bugs are discovered, they should be reported to
the appropriate bug tracker. If you obtained the software from a 3rd party
operating system vendor, it is often wise to use their own bug tracker for
reporting problems. In all other cases use the master OpenStack bug tracker,
available at:

    http://bugs.launchpad.net/openstack-salt

Developers wishing to work on the OpenStack Salt project should always base
their work on the latest formulas code, available from the master GIT
repository at:

    https://git.openstack.org/cgit/openstack/salt-formula-keystone

Developers should also join the discussion on the IRC list, at:

    https://wiki.openstack.org/wiki/Meetings/openstack-salt

Documentation and Bugs
======================

To learn how to install and update salt-formulas, consult the documentation
available online at:

    http://salt-formulas.readthedocs.io/

In the unfortunate event that bugs are discovered, they should be reported to
the appropriate issue tracker. Use Github issue tracker for specific salt
formula:

    https://github.com/salt-formulas/salt-formula-keystone/issues

For feature requests, bug reports or blueprints affecting entire ecosystem,
use Launchpad salt-formulas project:

    https://launchpad.net/salt-formulas

You can also join salt-formulas-users team and subscribe to mailing list:

    https://launchpad.net/~salt-formulas-users

Developers wishing to work on the salt-formulas projects should always base
their work on master branch and submit pull request against specific formula.

    https://github.com/salt-formulas/salt-formula-keystone

Any questions or feedback is always welcome so feel free to join our IRC
channel:

    #salt-formulas @ irc.freenode.net
