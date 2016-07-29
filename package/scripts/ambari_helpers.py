# coding=utf8
# Copyright © 2015-2016 Cask Data, Inc.
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
    Execute("sed -e 's#REPO_URL#%s#' %s > %s" % (params.repo_url, source, dest_file))
    Execute(params.key_cmd)
    Execute(params.cache_cmd)


def cdap_config(name=None):
    import params
    print 'Setting up CDAP configuration for ' + name
    # We're only setup for *NIX, for now
    Directory(
        params.etc_prefix_dir,
        mode=0755
    )

    Directory(
        params.cdap_conf_dir,
        owner=params.cdap_user,
        group=params.user_group,
        recursive=True
    )

    XmlConfig(
        'cdap-site.xml',
        conf_dir=params.cdap_conf_dir,
        configurations=params.config['configurations']['cdap-site'],
        owner=params.cdap_user,
        group=params.user_group
    )

    File(
        format("{params.cdap_conf_dir}/cdap-env.sh"),
        owner=params.cdap_user,
        content=InlineTemplate(params.cdap_env_sh_template)
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

    # Set dirname
    if name == 'auth':
        dirname = 'security'
    elif name == 'router':
        dirname = 'gateway'
    else:
        dirname = name

    cleanup_opts(dirname)

    # Copy logback.xml and logback-container.xml
    for i in 'logback.xml', 'logback-container.xml':
        no_op_test = "ls %s/%s 2>/dev/null" % (params.cdap_conf_dir, i)
        Execute(
            "cp -f /etc/cdap/conf.dist/%s %s" % (i, params.cdap_conf_dir),
            not_if=no_op_test
        )

    Execute("update-alternatives --install /etc/cdap/conf cdap-conf %s 50" % (params.cdap_conf_dir))


def has_hive():
    import params
    if len(params.hive_metastore_host) > 0:
        return true
    else:
        return false


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


def cleanup_opts(dirname):
    command = "sed -i 's/\"$OPTS\"/$OPTS/g' /opt/cdap/%s/bin/service" % (dirname)
    # We ignore errors here, in case we are called before package installation
    shell.call(command, timeout=20)
