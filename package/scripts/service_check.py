from resource_management import *

class CdapServiceCheck(Script):
    def service_check(self, env):
        import params
        env.set_params(params)

        status_url = "http://%s:%s/v3/system/services/status" % (params.cdap_router_host, params.cdap_router_port)

        ### TODO: do something useful here

if __name__ == "__main__":
    CdapServiceCheck().execute()
