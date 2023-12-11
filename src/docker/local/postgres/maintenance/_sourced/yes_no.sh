#!/usr/bin/env bash

yes_no(){
    declare desc="Prompt for confirmation. \$\"\{1\}\": confirmation message"

    local arg1="${1}"
    # reads reponse with prompt and -r stops / from being interpreted
    local reponse= read -r -p "${arg1} (y/[n])? " response

    # Checks if reponse if lowercase y or uppercase Y
    if [[ "${response}" =~ ^[Yy]$ ]]

    then
        exit 0
    else
        exit 1
    fi
}