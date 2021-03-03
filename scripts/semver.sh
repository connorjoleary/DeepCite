#!/bin/bash
unset ACTION SERVICE GITOPTS

usage()
{
    echo "Usage: $0 {ACTION,SERVICE} | {CMD} | [-h] ...
    ACTIONS:        [patch|minor|major]
    SERVICES:       [model|api|lambda|extension]
    GITOPTS:        [stage|commit]
    CMDS:           [show|version|backend|help]

    For more help try 'semver.sh backend -h' or 'semver.sh version -h'"
    exit 2
}

set_variable()
{
    local varname=$1
    shift
    if [ -z "${!varname}" ]; then
        eval "$varname=\"$@\""
    else
        echo "Error $varname already set"
        usage
    fi
}

backend()
{
    python3 backend_versions.py "$@" 
}

while [ "$#" -gt "0" ]
do
    case $1 in
        backend)
                shift
                backend $@
                break
                ;;
        show)
                backend $@
                break
                ;;
        version)
                backend $@
                break
                ;;
        patch)
                set_variable ACTION $1
                shift
                ;;
        minor)
                set_variable ACTION $1
                shift
                ;;
        major)
                set_variable ACTION $1
                shift
                ;;
        api)
                set_variable SERVICE $1
                shift
                ;;
        model)
                set_variable SERVICE $1
                shift
                ;;
        lambda)
                set_variable SERVICE $1
                shift
                ;;
        extension)
                set_variable SERVICE $1
                shift
                ;;
        stage)
                set_variable GITOPTS $1
                shift
                ;;
        commit)
                set_variable GITOPTS $1
                shift
                ;;
        help|'-h')
                usage
                ;;
        *)
                echo "Error unrecognized command $1"
                usage
                ;; esac
done

if [ "$SERVICE" = "extension" ]; then
    if [ -n "$ACTION" ]; then
        cd ../extension/
        VERSION=`npm version "$ACTION"`
        git tag -a "$VERSION" -m "$ACTION update $VERSION"
        [ -n "$GITOPTS" ] && git add package.json package-lock.json manifest.json
        cd ../scripts/
    else
        echo "Error must provide a action for $SERVICE"
        usage
    fi
fi

if [ -n "$ACTION" ]; then
    if [ -n "$SERVICE" ]; then
        python3 backend_versions.py version "$ACTION" "$SERVICE" -f
        if [ -n "$GITOPTS" ]; then
            git add ../backend/aws/lambda/defaults.json
            [ "$GITOPTS" =  "commit" ] && git commit -m "$SERVICE $ACTION update"
        fi
    else
        echo "Error must provide a service for $ACTION"
        usage
    fi
else
    if [ -n "$SERVICE" ]; then
        echo "Error must provide a action for $SERVICE"
        useage
    fi
fi
exit 0