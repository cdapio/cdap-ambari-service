from resource_management import *

class CdapServiceCheck(Script):
  def service_check(self, env):
    import params
    env.set_params(params)

    status_url = 'http://' + cdap_router_host + ':' + cdap_router_port + '/v3/system/services'

    ### TODO: do something useful here

if __name__ == "__main__":
  CdapServiceCheck().execute()
