from resource_management import *
import os

def create_hdfs_dir(path, owner, perms):
  Execute('hadoop fs -mkdir -p '+path, user='hdfs')
  Execute('hadoop fs -chown ' + owner + ' ' + path, user='hdfs')
  Execute('hadoop fs -chmod ' + str(perms) + ' ' + path, user='hdfs')

def package(name):
  import params
  Execute(params.package_mgr + ' install -y ' + name, user='root')

def add_repo(source, dest):
  import params
  if not os.path.isfile(dest + params.repo_file):
    Execute('cp ' + source + ' ' + dest)
    Execute(params.key_cmd)
    Execute(params.cache_cmd)

def cdap_config(name=None):
  import params
  print 'Setting up CDAP configuration for ' + name
  # We're only setup for *NIX, for now
  Directory(params.etc_prefix_dir,
            mode=0755
  )

  Directory(params.cdap_conf_dir,
            owner = params.cdap_user,
            group = params.user_group,
            recursive = True
  )

  XmlConfig("cdap-site.xml",
            conf_dir = params.cdap_conf_dir,
            configurations = params.config['configurations']['cdap-site'],
            owner = params.cdap_user,
            group = params.user_group
  )

  File(format("{params.cdap_conf_dir}/cdap-env.sh"),
       owner = params.cdap_user,
       content=InlineTemplate(params.cdap_env_sh_template)
  )

  cleanup_opts()

  # Copy logback.xml and logback-container.xml
  for i in 'logback.xml', 'logback-container.xml':
    no_op_test = 'ls ' + params.cdap_conf_dir + '/' + i + ' 2>/dev/null'
    Execute('cp -f /etc/cdap/conf.dist/' + i + ' ' + params.cdap_conf_dir, not_if=no_op_test)

  Execute('update-alternatives --install /etc/cdap/conf cdap-conf ' + params.cdap_conf_dir + ' 50')

def has_hive():
  import params
  if len(params.hive_metastore_host) > 0:
    return true
  else:
    return false

def get_hdp_version():
  command = 'hadoop version | head -n 1 | cut -d. -f4-'
  return_code, hdp_output = shell.call(command, timeout=20)

  if return_code != 0:
    raise Fail(
      'Unable to determine the current version because of a non-zero return code of {0}'.format(str(return_code)))

  hdp_version = hdp_output.rstrip()
  match = re.match('[0-9]+.[0-9]+.[0-9]+.[0-9]+-[0-9]+', hdp_version)

  if match is None:
    raise Fail('Failed to get extracted version')

  return hdp_version

def cleanup_opts():
  Execute('sed -i \'s/"$OPTS"/$OPTS/g\' /opt/cdap/*/bin/service')
