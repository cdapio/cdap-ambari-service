from resource_management import *
import os

def create_hdfs_dir(path, owner, perms):
  Execute('hadoop fs -mkdir -p '+path, user='hdfs')
  Execute('hadoop fs -chown ' + owner + ' ' + path, user='hdfs')
  Execute('hadoop fs -chmod ' + perms + ' ' + path, user='hdfs')

def package(name):
  Execute(package_mgr + ' install -y ' + name, user='root')

def add_repo(source, dest):
  if not os.path.isfile(dest + repo_file):
    Execute('cp ' + source + ' ' + dest)
