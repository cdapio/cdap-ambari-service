from resource_management import *

# config object that holds the configurations declared in the -config.xml file
config = Script.get_config()

cdap_user = config['configurations']['cdap-env']['cdap_user']
pid_dir = config['configurations']['cdap-env']['cdap_pid_dir']

cdap_auth_pid_file = pid_dir + '/auth-server-' + cdap_user + '.pid'
cdap_kafka_pid_file = pid_dir + '/kafka-server-' + cdap_user + '.pid'
cdap_master_pid_file = pid_dir + '/master-' + cdap_user + '.pid'
cdap_router_pid_file = pid_dir + '/router-' + cdap_user + '.pid'
cdap_ui_pid_file = pid_dir + '/ui-' + cdap_user + '.pid'
