# Copyright © 2015 Cask Data, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

from resource_management import *
from resource_management.libraries.functions.version import format_hdp_stack_version, compare_versions
import os
import ambari_helpers as helpers

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

hdp_version = helpers.get_hdp_version()
hadoop_lib_home = helpers.get_hadoop_lib()

if distribution in ['centos', 'redhat']:
    os_repo_dir = '/etc/yum.repos.d/'
    repo_file = 'cdap-3.1.repo'
    package_mgr = 'yum'
    key_cmd = "rpm --import %s/pubkey.gpg" % (files_dir)
    cache_cmd = 'yum makecache'
else:
    os_repo_dir = '/etc/apt/sources.list.d/'
    repo_file = 'cdap-3.1.list'
    package_mgr = 'apt-get'
    key_cmd = "apt-key add %s/pubkey.gpg" % (files_dir)
    cache_cmd = 'apt-get update'

cdap_user = config['configurations']['cdap-env']['cdap_user']
log_dir = config['configurations']['cdap-env']['cdap_log_dir']
pid_dir = config['configurations']['cdap-env']['cdap_pid_dir']
cdap_kafka_heapsize = config['configurations']['cdap-env']['cdap_kafka_heapsize']
cdap_master_heapsize = config['configurations']['cdap-env']['cdap_master_heapsize']
cdap_router_heapsize = config['configurations']['cdap-env']['cdap_router_heapsize']

etc_prefix_dir = "/etc/cdap"
cdap_conf_dir = "/etc/cdap/conf.ambari"
dfs = config['configurations']['core-site']['fs.defaultFS']

cdap_env_sh_template = config['configurations']['cdap-env']['content']

security_enabled = config['configurations']['cluster-env']['security_enabled']
map_cdap_site = config['configurations']['cdap-site'];

# Example: root.namespace
root_namespace = map_cdap_site['root.namespace']
if map_cdap_site['hdfs.namespace'] == '/${root.namespace}':
    hdfs_namespace = '/' + root_namespace
else:
    hdfs_namespace = map_cdap_site['hdfs.namespace']
hdfs_user = map_cdap_site['hdfs.user']
### TODO: Fix this hack -- check if we're still cdap_user
hdfs_user = cdap_user
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
    if (i + 1) < len(kafka_hosts):
        tmp_kafka_hosts += ','
cdap_kafka_brokers = tmp_kafka_hosts

router_hosts = config['clusterHostInfo']['cdap_router_hosts']
router_hosts.sort()
cdap_router_host = router_hosts[0]

# Get some of our hosts
hive_metastore_host = config['clusterHostInfo']['hive_metastore_host']
hive_server_host = config['clusterHostInfo']['hive_server_host']
if len(hive_server_host) > 0 and hive_server_host == cdap_router_host:
    cdap_router_port = '11015'
else:
    cdap_router_port = '10000'

### TODO: cdap_auth_server_hosts cdap_ui_hosts
