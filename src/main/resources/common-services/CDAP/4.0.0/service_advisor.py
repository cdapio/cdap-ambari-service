#!/usr/bin/env ambari-python-wrap
# coding=utf8
# Copyright © 2016-2017 Cask Data, Inc.
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
import imp
import traceback

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STACKS_DIR = os.path.join(SCRIPT_DIR, '../../../stacks/')
PARENT_FILE = os.path.join(STACKS_DIR, 'service_advisor.py')

try:
    with open(PARENT_FILE, 'rb') as fp:
        service_advisor = imp.load_module('service_advisor', fp, PARENT_FILE, ('.py', 'rb', imp.PY_SOURCE))
except Exception as e:
    traceback.print_exc()
    print 'Failed to load parent'


class CDAP42xServiceAdvisor(service_advisor.ServiceAdvisor):

    def colocateService(self, hostsComponentsMap, serviceComponents):
        # colocate CDAP_MASTER with NAMENODE, if no hosts have been allocated for CDAP_MASTER
        cdap = [component for component in serviceComponents
                if component["StackServiceComponents"]["component_name"] == "CDAP_MASTER"][0]
        if not self.isComponentHostsPopulated(cdap):
            for hostName in hostsComponentsMap.keys():
                hostComponents = hostsComponentsMap[hostName]
                if {"name": "NAMENODE"} in hostComponents and {"name": "CDAP_MASTER"} not in hostComponents:
                    hostsComponentsMap[hostName].append({"name": "CDAP_MASTER"})
                if {"name": "NAMENODE"} not in hostComponents and {"name": "CDAP_MASTER"} in hostComponents:
                    hostComponents.remove({"name": "CDAP_MASTER"})

    def getServiceConfigurationRecommendations(self, configurations, clusterSummary, services, hosts):
        pass

    def getServiceComponentLayoutValidations(self, services, hosts):
        return []

    def getServiceConfigurationsValidationItems(self, configurations, recommendedDefaults, services, hosts):
        return []
