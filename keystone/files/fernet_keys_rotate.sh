{%- from "keystone/map.jinja" import server with context -%}
#!/bin/bash
usage() {
cat <<EOF
Script for Fernet key rotation and sync
    For additional help please use: $0 -h or --help
    example: $0 -s
EOF
}

if [ $# -lt "1" ]; then
        usage
        exit 1
fi

help_usage() {
cat <<EOF
Following options are supported:
    -s  Perform sync to secondary controller nodes only
    -r  Perform Fernet key rotation on primary controller only
    -rs  Perform Fernet key rotation on primary controller and sync to secondary controller nodes
EOF
}

if [ $# -lt "1" ]; then
        usage
        exit 1
fi

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -h|--help)
    help_usage
    shift # past argument
    ;;
    -s)
    MODE="SYNC"
    shift # past argument
    ;;
    -r)
    MODE="ROTATE"
    shift
    ;;
    -rs)
    MODE="ROTATE_AND_SYNC"
    shift
    ;;
    *)    # unknown option
    echo "Unknown option. Please refer to help section by passing -h or --help option"
    shift # past argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

#Setting variables
KEYSTONE_MANAGE_CMD="/usr/bin/keystone-manage"
{%- if server.tokens.fernet_sync_nodes_list is defined %}
        {%- set _nodes = [] %}
          {%- for node_name, fernet_sync_nodes_list in server.tokens.get('fernet_sync_nodes_list', {}).iteritems() %}
            {%- if fernet_sync_nodes_list.get('enabled', False) %}
              {%- do _nodes.append(fernet_sync_nodes_list.name) %}
            {%- endif %}
          {%- endfor %}
NODES="{{ ' '.join(_nodes) }}"
{%- else %}
NODES=""
{%- endif %}

if [[ ${MODE} == 'SYNC' ]]; then
  echo "Running in SYNC mode"
    if [[ ${NODES} != '' ]]; then
      for NODE in ${NODES}; do
        echo "${NODE}"
        rsync -e 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no' -avz --delete {{ server.tokens.location }}/ keystone@${NODE}:{{ server.tokens.location }}/
      done
    else
      echo "List of nodes is not specified, no need for sync, exiting"
      exit 0
    fi
elif [[ ${MODE} == 'ROTATE' ]]; then
  echo "Running in ROTATE mode"
  /usr/bin/keystone-manage --log-file /var/log/keystone/keystone-rotate.log fernet_rotate  --keystone-user keystone --keystone-group keystone
elif [[ ${MODE} == 'ROTATE_AND_SYNC' ]]; then
  echo "Running in ROTATE_AND_SYNC mode"
  /usr/bin/keystone-manage --log-file /var/log/keystone/keystone-rotate.log fernet_rotate  --keystone-user keystone --keystone-group keystone
  if [[ ${NODES} != '' ]]; then
    for NODE in ${NODES}; do
      echo "${NODE}"
      rsync -e 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no' -avz --delete {{ server.tokens.location }}/ keystone@${NODE}:{{ server.tokens.location }}/
    done
  else
    echo "List of nodes is not specified, no need for sync, exiting"
    exit 0
  fi
fi
