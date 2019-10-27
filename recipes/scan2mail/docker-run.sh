#!/bin/bash
ikey="diy-scan-to-mail"
flog="docker-run.log"

# Parse command line
[ -z "$1" ] && {
    echo "Please provide one or more paths to your configuration files!"
    exit 1
}
# Generate docker arguments (darg) to mount local files to container and
# scan2mail arguments (sarg) to reference those files from within the container
pt=0
for arg in $@; do
    cfg_file=$( readlink -f $arg ) # abs path necessary for docker
    darg="${darg}-v ${cfg_file}:/config-${pt}.json "
    sarg="${sarg}-i /config-${pt}.json "
    pt=$(( $pt + 1 ))
done
cd "$( dirname "$( readlink -f "$0" )" )" # change to script dir

running=$( docker ps -q -f ancestor=$ikey )
[ ! -z "$running" ] && {
   echo "$( date ) - scan2mail is running." >> $flog
   exit 0
}

# Always build container first
docker build -t $ikey .
# check if there is a container from that image
container_id=$( docker ps -a --filter "ancestor=${ikey}:latest" -q | head -n1 )

if [ ! -z $container_id ]
then
    echo "$( date ) - restarting container $container_id" >> $flog
    docker start -i $container_id
else
    echo "$( date ) - creating new container" >> $flog
    set -x
    docker run $darg $ikey $sarg
    set +x
fi

