from resource_management import *
from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
import os

# config object that holds the configurations declared in the -config.xml file
config = Script.get_config()
tmp_dir = Script.get_tmp_dir()

stack_dir = os.path.realpath(__file__).split('/scripts')[0]
package_dir = os.path.realpath(__file__).split('/package')[0] + '/package/'
files_dir = package_dir + 'files/'
scripts_dir = package_dir + 'scripts/'
distribution = platform.linux_distribution()[0].lower()
hostname = config['hostname']
java64_home = config['hostLevelParams']['java_home']
user_group = config['configurations']['cluster-env']['user_group']

if distribution in ['centos', 'redhat'] :
  os_repo_dir = '/etc/yum.repos.d/'
  repo_file = 'cdap-3.0.repo'
  package_mgr = 'yum'
  key_cmd = 'rpm --import ' + files_dir + 'pubkey.gpg'
  cache_cmd = 'yum makecache'
else :
  os_repo_dir = '/etc/apt/sources.list.d/'
  repo_file = 'cdap-3.0.list'
  package_mgr = 'apt-get'
  key_cmd = 'apt-key add ' + files_dir + 'pubkey.gpg'
  cache_cmd = 'apt-get update'

cdap_user = "cdap"
etc_prefix_dir = "/etc/cdap"
cdap_conf_dir = "/etc/cdap/conf.ambari"
dfs = config['configurations']['core-site']['fs.defaultFS']

cdap_env_sh_template = config['configurations']['cdap-env']['content']

security_enabled = config['configurations']['cluster-env']['security_enabled']
map_cdap_site = config['configurations']['cdap-site'];

# Example: root.namespace
root_namespace = map_cdap_site['root.namespace']
if map_cdap_site['hdfs.namespace'] == '/${root.namespace}' :
  hdfs_namespace = '/' + root_namespace
else:
  hdfs_namespace = map_cdap_site['hdfs.namespace']
hdfs_user = map_cdap_site['hdfs.user']
kafka_log_dir = map_cdap_site['kafka.log.dir']

# Get ZooKeeper variables
zk_client_port = str(default('/configurations/zoo.cfg/clientPort', None))
zk_hosts = config['clusterHostInfo']['zookeeper_hosts']
zk_hosts.sort()
zookeeper_hosts = ''
# Evaluate and setup ZooKeeper quorum string
for i, val in enumerate(zk_hosts):
  zookeeper_hosts += val + ':' + zk_client_port
  if (i + 1) < len(zk_hosts):
    zookeeper_hosts += ','
cdap_zookeeper_quorum = zookeeper_hosts + '/' + root_namespace

kafka_bind_port = str(default('/configurations/cdap-site/kafka.bind.port', None))
kafka_hosts = config['clusterHostInfo']['cdap_kafka_hosts']
kafka_hosts.sort()
tmp_kafka_hosts = ''
for i, val in enumerate(kafka_hosts):
  tmp_kafka_hosts += val + ':' + kafka_bind_port
  if (i + 1) < len(tmp_kafka_hosts):
    tmp_kafka_hosts += ','
cdap_kafka_brokers = tmp_kafka_hosts

### TODO: cdap_auth_server_hosts cdap_router_hosts cdap_ui_hosts

# Get some of our hosts
hive_metastore_host = config['clusterHostInfo']['hive_metastore_host']

cdap_auth_pid_file = '/var/cdap/run/auth-server-' + cdap_user + '.pid'
cdap_kafka_pid_file = '/var/cdap/run/kafka-server-' + cdap_user + '.pid'
cdap_master_pid_file = '/var/cdap/run/master-' + cdap_user + '.pid'
cdap_router_pid_file = '/var/cdap/run/router-' + cdap_user + '.pid'
cdap_ui_pid_file = '/var/cdap/run/ui-' + cdap_user + '.pid'
