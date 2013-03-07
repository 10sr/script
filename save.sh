#!/bin/sh

help(){
    cat <<__EOC__ 2>&1
save: $1 [-h] [-d dst] file ...
    Very simple backup tool using rsync.
__EOC__
}

debug=

do_rsync(){
    # do_rsync dstdir files ...
    dstdir="$1"
    shift

    if expr "$dstdir" : '.*:' >/dev/null
    then
        host="$(expr "$dstdir" : '\(.*\):')"
        dir="$(expr "$dstdir" : '.*:\(.*\)$')"
        printf "Creating $dir in $host..."
        $debug ssh "$host" mkdir -p "$dir"
        echo "done"
    else
        $debug mkdir -p "$dstdir"
    fi

    # src=foo/ : copy the contents of this directory
    # src=foo : copy the directory by name
    # these two are same:
    #     rsync -av /src/foo  /dest
    #     rsync -av /src/foo/ /dest/foo

    # if $dstdir ends with /
    #     create dir $dstdir if not exists and copy files into $dstdir
    # if $dstdir already exists and it is a directory
    #     copy files into $dstdir
    # elif $@ is one file ($1)
    #     copy create file named $dstdir with contents of $1
    # else
    #     fail
    echo "Start copying files into \"$dstdir\"."
    $debug rsync -a --stats --progress --human-readable "$@" "$dstdir"
}

dst=
while getopts hd: opt
do
    case "$opt" in
        d) dst="$OPTARG";;
        h) help; exit 1;;
        *) help; exit 1;;
    esac
done

shift `expr $OPTIND - 1`

defdst=".my/saved"
if test -z "$dst"
then
    dstdir="$HOME/$defdst"
elif expr "$dst" : '.*:$' >/dev/null
then
    # only hostname is specified
    dstdir="$dst$defdst"        # host:.my/saved
else
    dstdir="$dst"
fi
timestr=`date +%Y%m%d-%H%M%S`
dstdir="$dstdir/$timestr/"

if test -z "$1"
then
    help "`basename "$0"`"
    exit 1
fi

do_rsync "$dstdir" "$@"