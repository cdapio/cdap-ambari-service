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
  Directory( params.etc_prefix_dir,
      mode=0755
  )

  Directory( params.cdap_conf_dir,
      owner = params.cdap_user,
      group = params.user_group,
      recursive = True
  )

  XmlConfig( "cdap-site.xml",
            conf_dir = params.cdap_conf_dir,
            configurations = params.config['configurations']['cdap-site'],
            configuration_attributes=params.config['configuration_attributes']['cdap-site'],
            owner = params.cdap_user,
            group = params.user_group
  )

  File(format("{params.cdap_conf_dir}/cdap-env.sh"),
       owner = params.cdap_user,
       content=InlineTemplate(params.cdap_env_sh_template)
  )

  Execute('update-alternatives --install /etc/cdap/conf cdap-conf /etc/cdap/' + params.cdap_conf_dir + ' 50')
