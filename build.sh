#!/usr/bin/env bash

PACKAGE_VERSION=${PACKAGE_VERSION:-5.0.0-SNAPSHOT}
PACKAGE_ITERATION=${PACKAGE_ITERATION:-1}
PACKAGE_FORMATS=${PACKAGE_FORMATS:-deb rpm tar}

LICENSE="Copyright © 2015-2017 Cask Data, Inc. Licensed under the Apache License, Version 2.0."
RPM_FPM_ARGS="-t rpm --rpm-os linux"
DEB_FPM_ARGS="-t deb"

if [[ ${PACKAGE_VERSION} =~ "-SNAPSHOT" ]] ; then
  PACKAGE_VERSION=${PACKAGE_VERSION/-SNAPSHOT/.$(date +%s)}
fi

clean() { rm -rf build target; };
setup() { mkdir -p build/var/lib/ambari-server/resources target; };

install() {
  cp -a src/main/resources/* build/var/lib/ambari-server/resources
  sed -i'' -e "s/REPLACE_ME/${PACKAGE_VERSION}/g" \
    build/var/lib/ambari-server/resources/stacks/*/*/services/CDAP/metainfo.xml \
    build/var/lib/ambari-server/resources/common-services/CDAP/*/alerts.json \
    build/var/lib/ambari-server/resources/common-services/CDAP/*/metainfo.xml
  mkdir build/cdap-ambari-service
  cp -R build/var/lib/ambari-server/resources build/cdap-ambari-service/
}

clean && setup && install

__failed=0
cd target
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
        -C ../build \
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
        -C ../build \
        var
      __ret=$?
     ;;
     tar)
      tar \
        -cvzf cdap-ambari-service-mpack-${PACKAGE_VERSION}-${PACKAGE_ITERATION}.tar.gz \
        -C ../build \
        ../build/cdap-ambari-service/resources/
     ;;
    *)
      echo "Unsupported format! ${p}"
      exit 1
      ;;
  esac
  [[ ${__ret} -ne 0 ]] && __failed=1
done

exit ${__failed} # It's okay if this is empty
