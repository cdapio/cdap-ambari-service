#!/usr/bin/env bash

SUPPORTED_HDP_VERSIONS=${SUPPORTED_HDP_VERSIONS:-2.0.6}
PACKAGE_VERSION=${PACKAGE_VERSION:-3.5.0-SNAPSHOT}
PACKAGE_ITERATION=${PACKAGE_ITERATION:-1}
PACKAGE_FORMATS=${PACKAGE_FORMATS:-deb rpm}

rm -rf var
mkdir -p var/lib/ambari-server/resources/stacks/HDP
for i in ${SUPPORTED_HDP_VERSIONS} ; do
  __target=var/lib/ambari-server/resources/stacks/HDP/${i}/services/CDAP
  mkdir -p ${__target}
  cp -a *.json *.xml configuration package themes ${__target} 2>/dev/null
done

LICENSE="Copyright © 2015-2016 Cask Data, Inc. Licensed under the Apache License, Version 2.0."
RPM_FPM_ARGS="-t rpm --rpm-os linux"
DEB_FPM_ARGS="-t deb"

if [[ ${PACKAGE_VERSION} =~ "-SNAPSHOT" ]] ; then
  PACKAGE_VERSION=${PACKAGE_VERSION/-SNAPSHOT/$(date +%s)}
fi

__failed=0
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
        --version ${PACKAGE_VERSION} \
        --iteration ${PACKAGE_ITERATION} \
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
        --version ${PACKAGE_VERSION} \
        --iteration ${PACKAGE_ITERATION} \
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
