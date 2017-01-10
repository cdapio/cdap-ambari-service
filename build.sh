#!/usr/bin/env bash

PACKAGE_VERSION=${PACKAGE_VERSION:-4.0.1-SNAPSHOT}
PACKAGE_ITERATION=${PACKAGE_ITERATION:-1}
PACKAGE_FORMATS=${PACKAGE_FORMATS:-deb rpm}

LICENSE="Copyright © 2015-2016 Cask Data, Inc. Licensed under the Apache License, Version 2.0."
RPM_FPM_ARGS="-t rpm --rpm-os linux"
DEB_FPM_ARGS="-t deb"

if [[ ${PACKAGE_VERSION} =~ "-SNAPSHOT" ]] ; then
  PACKAGE_VERSION=${PACKAGE_VERSION/-SNAPSHOT/.$(date +%s)}
fi

clean() { rm -rf var cdap-ambari-service*.{rpm,deb}; };
setup() { mkdir -p var/lib/ambari-server/resources/common-services/CDAP/${PACKAGE_VERSION}; };

install() {
  cp -a *.json *.xml configuration package quicklinks themes \
    var/lib/ambari-server/resources/common-services/CDAP/${PACKAGE_VERSION} 2>/dev/null
  cp -a stacks var/lib/ambari-server/resources 2>/dev/null
  sed -i'' -e "s/3.6.0-SNAPSHOT/${PACKAGE_VERSION}/g" \
    var/lib/ambari-server/resources/stacks/*/*/services/CDAP/metainfo.xml \
    var/lib/ambari-server/resources/common-services/CDAP/${PACKAGE_VERSION}/alerts.json \
    var/lib/ambari-server/resources/common-services/CDAP/${PACKAGE_VERSION}/metainfo.xml
}

clean && setup && install

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
        --depends "ambari-server > 2.2" \
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
        --depends "ambari-server > 2.2" \
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
