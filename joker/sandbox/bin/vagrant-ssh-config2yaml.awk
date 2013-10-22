#!/bin/sh

#controller: &controller
#       host:  
#            <<: *host
#            dst: 127.0.0.1
#            port: 2222
#       user:
#            <<: *user
#            name: 'vagrant'
#            private_key_path: '/home/ryabin/.vagrant.d/insecure_private_key'
#            l7_options: 
#                - 'LogLevel FATAL'
#                - 'IdentitiesOnly yes'
#                - 'PasswordAuthentication no'
#                - 'StrictHostKeyChecking no'
#                - 'UserKnownHostsFile /dev/null'

# vagrant ssh-config name |  awk -f this.script 
function ssh_template_yaml(env) {

        fmt = "%s_joker: &%s_joker\n"
        printf fmt, env["Host"], env["Host"];
        printf "  host:\n"
        printf "    <<: *host\n"
        fmt = "    %s: %s\n"
        printf fmt, "dst", env["HostName"] 
        if (env["Port"]) {
            printf fmt, "port", env["Port"] 
        }
        printf "  user:\n"
        printf "    <<: *user\n"
        printf fmt, "name", env["User"]
        printf fmt, "private_key_path", env["IdentityFile"]
        printf fmt, "l7_options", ""

        fmt = "      - \"%s\"\n"
        for (i in l7_options) {
            printf fmt, l7_options[i]
        }
        
        exit
} 

# ssh entry is 
# "^Host foobar"
#  Key value 
#  Key value
#  ....
#  Key value
# "^Host foobar2" -- we got start point of new host entry
#  Key value 
#  Key value
#  ....
#  Key value

BEGIN {
    # first ssh entry applies for all described after    
    env["Host"] = "default"
} 

# entry starts
/^Host /i {
    ssh_template_yaml(env); # dump entry
    delete env;             # reset env
} 

env[$1] = gensub(/.*[^ ] /, "", $0)  

END {
    # end of parsing, dumping last entry
    #ssh_template_yaml(env)
} 
