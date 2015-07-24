from resource_management import *

class CdapServiceCheck(Script):
  def service_check(self, env):
    import params
    env.set_params(params)

if __name__ == "__main__":
  CdapServiceCheck().execute()
