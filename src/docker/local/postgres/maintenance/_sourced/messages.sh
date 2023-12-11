#!/usr/bin/env bash

message_newline(){
    echo
}

# function which outputs debug message with all arguments provided
message_debug(){
    echo -e "DEBUG: ${@}"
}

# Displays the messages passed in as bold
message_welcome(){
    echo -e "\e[1m${@}\e[0m"
}

# Displays warning messages in yellow color after the WARNING prefix 
message_warning(){
    echo -e "\e[33mWARNING\e[0m: ${@}"
}

# Displays error messages in red after the ERROR prefix
message_error(){
    echo -e "\e[31mERROR\e[0m: ${@}"
}

# Displays info messages in light gray after INFO prefix
message_info(){
    echo -e "\e[37mINFO\e[0m: ${@}"
}

# Displays suggestion messages in yellow after SUGGESTION prefix
message_suggestion(){
    echo -e "\e[33mSUGGESTION\e[0m: ${@}"
}

# Displays success messages in green after SUCCESS prefix
message_success(){
    echo -e "\e[32mSUCCESS\e[0m: ${@}"
}
