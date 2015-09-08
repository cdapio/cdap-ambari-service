#!/usr/bin/env bash

SUPPORTED_AMBARI_VERSIONS=${SUPPORTED_AMBARI_VERSIONS:-2.0 2.1}
SERVICE_VERSION=${SERVICE_VERSION:-3.0.0}
PACKAGE_FORMATS=${PACKAGE_FORMATS:-deb rpm}

rm -rf var
mkdir -p var/lib/ambari-server/resources/stacks/HDP
for i in ${SUPPORTED_AMBARI_VERSIONS} ; do
  __target=var/lib/ambari-server/resources/stacks/HDP/${i}/services/CDAP
  mkdir -p ${__target}
  cp -a *.json *.xml configuration package themes ${__target}
done

LICENSE="Copyright © 2015 Cask Data, Inc. Licensed under the Apache License, Version 2.0."
RPM_FPM_ARGS="-t rpm --rpm-os linux"
DEB_FPM_ARGS="-t deb"

for p in ${PACKAGE_FORMATS} ; do
  case ${p} in
    deb)
      fpm \
        --name cdap-ambari-service \
        --license "${LICENSE}" \
        --vendor "Cask Data, Inc." \
        --maintainer support@cask.co \
        --description "Ambari service for Cask Data Application Platform (CDAP)" \
        -s dir \
        -a all \
        --url "http://cask.co" \
        --category misc \
        --depends "python > 2.6" \
        --depends "ambari-server > 2.0" \
        --version ${SERVICE_VERSION} \
        --iteration 1 \
        ${DEB_FPM_ARGS} \
        var
      __ret=$?
      ;;
    rpm)
      fpm \
        --name cdap-ambari-service \
        --license "${LICENSE}" \
        --vendor "Cask Data, Inc." \
        --maintainer support@cask.co \
        --description "Ambari service for Cask Data Application Platform (CDAP)" \
        -s dir \
        -a all \
        --url "http://cask.co" \
        --category misc \
        --depends "python > 2.6" \
        --depends "ambari-server > 2.0" \
        --version ${SERVICE_VERSION} \
        --iteration 1 \
        ${RPM_FPM_ARGS} \
        var
      __ret=$?
     ;;
    *)
      echo "Unsupported format! ${p}"
      exit 1
      ;;
  esac
  [[ ${__ret} -ne 0 ]] && __failed=1
done

exit ${__failed} # It's okay if this is empty
