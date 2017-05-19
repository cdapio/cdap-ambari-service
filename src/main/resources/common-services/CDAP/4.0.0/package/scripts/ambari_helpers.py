# coding=utf8
# Copyright © 2015-2017 Cask Data, Inc.
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

import os
from resource_management import *


def create_hdfs_dir(path, owner, perms):
    import params
    kinit_cmd = params.kinit_cmd_hdfs
    mkdir_cmd = format("{kinit_cmd} hadoop fs -mkdir -p {path}")
    chown_cmd = format("{kinit_cmd} hadoop fs -chown {owner} {path}")
    chmod_cmd = format("{kinit_cmd} hadoop fs -chmod {perms} {path}")
    Execute(mkdir_cmd, user='hdfs')
    Execute(chown_cmd, user='hdfs')
    Execute(chmod_cmd, user='hdfs')


def package(name):
    import params
    Execute("%s install -y %s" % (params.package_mgr, name), user='root')


def add_repo(source, dest):
    import params
    dest_file = dest + params.repo_file
    # Remove previous dest_file always
    Execute("rm -f %s" % (dest_file))
    # Skip sed if CDAP repos exist, we're on a newer Ambari... yay!
    no_op_test = format('ls {dest} 2>/dev/null | grep CDAP >/dev/null 2>&1')
    Execute(
        "sed -e 's#REPO_URL#%s#' %s > %s" % (params.repo_url, source, dest_file),
        not_if=no_op_test
    )
    Execute(params.key_cmd)
    Execute(params.cache_cmd)


def cdap_config(name=None):
    import params
    print('Setting up CDAP configuration for ' + name)
    # We're only setup for *NIX, for now
    Directory(
        params.etc_prefix_dir,
        mode=755
    )

    # Why don't we use Directory here? A: parameters changed between Ambari minor versions
    for i in params.cdap_conf_dir, params.log_dir, params.pid_dir:
        Execute(
            "mkdir -p %s && chown %s:%s %s" % (
                i,
                params.cdap_user,
                params.user_group,
                i
            )
        )

    for i in 'security', 'site':
        XmlConfig(
            "cdap-%s.xml" % (i),
            conf_dir=params.cdap_conf_dir,
            configurations=params.config['configurations']["cdap-%s" % (i)],
            owner=params.cdap_user,
            group=params.user_group
        )

    File(
        format("{params.cdap_conf_dir}/cdap-env.sh"),
        owner=params.cdap_user,
        content=InlineTemplate(params.cdap_env_sh_template)
    )

    File(
        format("{params.cdap_conf_dir}/logback.xml"),
        owner=params.cdap_user,
        content=InlineTemplate(params.cdap_logback_xml_template)
    )

    File(
        format("{params.cdap_conf_dir}/logback-container.xml"),
        owner=params.cdap_user,
        content=InlineTemplate(params.cdap_logback_container_xml_template)
    )

    if params.cdap_security_enabled:
        XmlConfig(
            'cdap-security.xml',
            conf_dir=params.cdap_conf_dir,
            configurations=params.config['configurations']['cdap-security'],
            owner=params.cdap_user,
            group=params.user_group
        )

    if params.kerberos_enabled:
        File(
            format(params.client_jaas_config_file),
            owner=params.cdap_user,
            content=Template("cdap_client_jaas.conf.j2")
        )

        File(
            format(params.master_jaas_config_file),
            owner=params.cdap_user,
            content=Template("cdap_master_jaas.conf.j2")
        )

    Execute("update-alternatives --install /etc/cdap/conf cdap-conf %s 50" % (params.cdap_conf_dir))


def has_hive():
    import params
    if len(params.hive_metastore_host) > 0:
        return true
    else:
        return false


def generate_quorum(hosts, port):
    p = ':' + port
    return (p + ',').join(hosts) + p


def get_hdp_version():
    command = 'hadoop version'
    return_code, hdp_output = shell.call(command, timeout=20)

    if return_code != 0:
        raise Fail("Unable to determine the current hadoop version: %s" % (hdp_output))

    line = hdp_output.rstrip().split('\n')[0]
    arr = line.split('.')
    hdp_version = "%s.%s.%s.%s" % (arr[3], arr[4], arr[5], arr[6])
    match = re.match('[0-9]+.[0-9]+.[0-9]+.[0-9]+-[0-9]+', hdp_version)
    if match is None:
        raise Fail('Failed to get extracted version')
    return hdp_version


def get_hadoop_lib():
    v = get_hdp_version()
    arr = v.split('.')
    maj_min = float("%s.%s" % (arr[0], arr[1]))
    if maj_min >= 2.2:
        hadoop_lib = "/usr/hdp/%s/hadoop/lib" % (v)
    else:
        hadoop_lib = '/usr/lib/hadoop/lib'
    return hadoop_lib
