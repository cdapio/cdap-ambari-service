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
import math
import traceback

from resource_management.core.logger import Logger

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STACKS_DIR = os.path.join(SCRIPT_DIR, '../../../stacks/')
PARENT_FILE = os.path.join(STACKS_DIR, 'service_advisor.py')

try:
    with open(PARENT_FILE, 'rb') as fp:
        service_advisor = imp.load_module('service_advisor', fp, PARENT_FILE, ('.py', 'rb', imp.PY_SOURCE))
except Exception as e:
    traceback.print_exc()
    print 'Failed to load parent'


class CDAP400ServiceAdvisor(service_advisor.ServiceAdvisor):

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
        # check Zookeeper configuration
        if "zoo.cfg" in services["configurations"]:
            zoo_cfg = services["configurations"]["zoo.cfg"]["properties"]
            putZooCfgProperty = self.putProperty(configurations, "zoo.cfg", services)

        for property, desired_value in self.getZooCfgDesiredValues().iteritems():
            if property not in zoo_cfg or zoo_cfg[property] != desired_value:
                putZooCfgProperty(property, desired_value)

    def getZooCfgDesiredValues(self):
        yarn_site_desired_values = {
            "maxClientCnxns": "0"
            }
        return yarn_site_desired_values

    def getServiceComponentLayoutValidations(self, services, hosts):
        return []

    def getServiceConfigurationsValidationItems(self, configurations, recommendedDefaults, services, hosts):
        # validate recommended properties in yarn-site
        siteName = "yarn-site"
        method = self.validateYarnSiteConfigurations
        items = self.validateConfigurationsForSite(configurations, recommendedDefaults, services, hosts, siteName, method)

        return items

    def validateYarnSiteConfigurations(self, properties, recommendedDefaults, configurations, services, hosts):
        yarn_site = properties
        validationItems = []

        # Calculate yarn available resources
        nodeManagerHost = self.getHostsWithComponent("YARN", "NODEMANAGER", services, hosts)
        nodeManagerCpu = int(len(nodeManagerHost)) * int(configurations["yarn-site"]["properties"]["yarn.nodemanager.resource.cpu-vcores"])
        nodeManagerMem = int(len(nodeManagerHost)) * int(configurations["yarn-site"]["properties"]["yarn.nodemanager.resource.memory-mb"])

        # calculate cdap resources
        cdapProperties = configurations["cdap-site"]["properties"]
        cdapCpu = int((int(cdapProperties["dataset.executor.container.num.cores"]) +
                       int(cdapProperties["messaging.container.num.cores"]) +
                       int(cdapProperties["stream.container.num.cores"]) +
                       int(cdapProperties["metrics.num.cores"]) +
                       int(cdapProperties["log.saver.container.num.cores"]) +
                       int(cdapProperties["explore.executor.container.num.cores"]) +
                       int(cdapProperties["metrics.processor.num.cores"]) +
                       int(cdapProperties["data.tx.num.cores"]) +
                       int(cdapProperties["master.service.num.cores"])))

        cdapMem = int((int(configurations["cdap-site"]["properties"]["dataset.executor.container.memory.mb"]) +
                       int(cdapProperties["messaging.container.memory.mb"]) +
                       int(cdapProperties["stream.container.memory.mb"]) +
                       int(cdapProperties["metrics.memory.mb"]) +
                       int(cdapProperties["log.saver.container.memory.mb"]) +
                       int(cdapProperties["explore.executor.container.memory.mb"]) +
                       int(cdapProperties["metrics.processor.memory.mb"]) +
                       int(cdapProperties["data.tx.memory.mb"]) +
                       int(cdapProperties["master.service.memory.mb"])))

        # log values
        Logger.info('nodeManagerCpu: ' + str(nodeManagerCpu))
        Logger.info('cdapCpu: ' + str(cdapCpu))
        Logger.info('nodeManagerMem: ' + str(nodeManagerMem))
        Logger.info('cdapMem: ' + str(cdapMem))

        # throw error if CDAP uses more core than available in YARN
        if (int(cdapCpu) > int(nodeManagerCpu)):
            mimimumValue = str(int(cdapCpu) / int(len(nodeManagerHost)) + 1)
            message = "CDAP will use " + str(cdapCpu) + " cores and requires this property to be set to a value greater than " + mimimumValue
            validationItems.append({"config-name": "yarn.nodemanager.resource.cpu-vcores", "item": self.getErrorItem(message)})

        # throw error if CDAP uses more memory than available in YARN
        if (int(cdapMem) > int(nodeManagerMem)):
            mimimumValue = str(int(cdapMem) / int(len(nodeManagerHost)))
            message = "CDAP will use " + str(cdapMem) + "mb and requires this property to be set to a value greater than " + mimimumValue + "mb"
            validationItems.append({"config-name": "yarn.nodemanager.resource.memory-mb", "item": self.getErrorItem(message)})

        return self.toConfigurationValidationProblems(validationItems, "yarn-site")

    def getHostsWithComponent(self, serviceName, componentName, services, hosts):
        if services is not None and hosts is not None and serviceName in [service["StackServices"]["service_name"] for service in services["services"]]:
            service = [serviceEntry for serviceEntry in services["services"] if serviceEntry["StackServices"]["service_name"] == serviceName][0]
            components = [componentEntry for componentEntry in service["components"]
                          if componentEntry["StackServiceComponents"]["component_name"] == componentName]
            if (len(components) > 0 and len(components[0]["StackServiceComponents"]["hostnames"]) > 0):
                componentHostnames = components[0]["StackServiceComponents"]["hostnames"]
                componentHosts = [host for host in hosts["items"] if host["Hosts"]["host_name"] in componentHostnames]
                return componentHosts
        return []
