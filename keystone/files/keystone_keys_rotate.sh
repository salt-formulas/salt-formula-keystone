{%- from "keystone/map.jinja" import server with context -%}
#!/bin/bash
usage() {
cat <<EOF
Script for fernet and credential key rotation and sync
  For additional help please use: $0 -h or --help
  example: $0 -s -t fernet
  exit 1
EOF
}

if [ $# -lt "2" ]; then
  usage
  exit 1
fi

help_usage() {
cat <<EOF
Following options are supported:
  -s|--sync  Perform keys sync to secondary controller nodes only
  -r|--rotate  Perform keys rotation on primary controller only
  -t|--type Possible values are "fernet" or "credential"
EOF
exit 0
}

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -h|--help)
    help_usage
    shift # pass argument
    ;;
    -s|--sync)
    SYNC=true
    shift # pass argument
    ;;
    -r|--rotate)
    ROTATE=true
    shift
    ;;
    -t|--type)
    TYPE="$2"
    shift
    shift
    ;;
    *)    # unknown option
    echo "Unknown option. Please refer to help section by passing -h or --help option"
    exit 1
    shift # pass argument
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

#Setting variables
START_DATE=`date +%d_%m_%Y-%H_%M`
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
{%- if server.credential.credential_sync_nodes_list is defined %}
        {%- set _nodes = [] %}
          {%- for node_name, credential_sync_nodes_list in server.credential.get('credential_sync_nodes_list', {}).iteritems() %}
            {%- if credential_sync_nodes_list.get('enabled', False) %}
              {%- do _nodes.append(credential_sync_nodes_list.name) %}
            {%- endif %}
          {%- endfor %}
CRED_NODES="{{ ' '.join(_nodes) }}"
{%- else %}
CRED_NODES=""
{%- endif %}
FERNET_DIR="{{ server.get('tokens', {}).get('location', {}) }}/"
CRED_DIR="{{ server.get('credential', {}).get('location', {}) }}/"

run_rsync () {
  local sync_dir=$1
  local sync_node=$2
  rsync -e 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no' -avz --delete ${sync_dir} keystone@${sync_node}:${sync_dir}
}

run_keystone () {
  local keystone_cmd=$1
  ${KEYSTONE_MANAGE_CMD} --log-file /var/log/keystone/keystone-rotate.log ${keystone_cmd} --keystone-user keystone --keystone-group keystone
}
if !([[ ${TYPE} == "fernet" ]] || [[ ${TYPE} == "credential" ]]) ; then
  echo "Given type is not valid - exiting"
  exit 1
fi
echo "Script started at: ${START_DATE}"

if [[ "${ROTATE}" = true ]] ; then
  if [[ ${TYPE} == "fernet" ]] ; then
    echo "Running in Fernet ROTATE mode"
    run_keystone "fernet_rotate"
  else
    echo "Running in Credential ROTATE mode"
    if !(run_keystone "credential_rotate") ; then
      echo "Credential rotate exited with fail status, calling credential_migrate and then credential_rotate again"
      run_keystone "credential_migrate"
      sleep 5
      run_keystone "credential_rotate"
    fi
  fi
fi
if [[ "${SYNC}" = true ]] ; then
  if [[ ${TYPE} == "fernet" ]] ; then
    echo "Running in Fernet SYNC mode"
    if [[ ${NODES} != '' ]]; then
      for NODE in ${NODES}; do
        echo "${NODE}"
        run_rsync "${FERNET_DIR}" "${NODE}"
      done
    else
      echo "List of nodes is not specified, no need for sync, exiting"
      exit 0
    fi
  else
    echo "Running in Credential SYNC mode"
    if [[ ${CRED_NODES} != '' ]]; then
      for NODE in ${CRED_NODES}; do
        echo "${NODE}"
        run_rsync "${CRED_DIR}" "${NODE}"
      done
    else
      echo "List of nodes is not specified, no need for sync, exiting"
      exit 0
    fi
  fi
fi
