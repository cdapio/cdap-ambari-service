from resource_management import *
from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
import os

# config object that holds the configurations declared in the -config.xml file
config = Script.get_config()

stack_dir = os.path.realpath(__file__).split('/scripts')[0]
package_dir = os.path.realpath(__file__).split('/package')[0] + '/package/'
files_dir = package_dir + 'files/'
scripts_dir = package_dir + 'scripts/'
distribution = platform.linux_distribution()[0].lower()
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

cdap_zookeeper_quorum = config['configurations']['cdap-site']['zookeeper.quorum']

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
