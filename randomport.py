#!/usr/bin/env python

'''
# Random non listening port finder
# Copyright (C) 2016-2017 Dimitrios Desyllas
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


from __future__ import print_function
import socket
import sys
import getopt
import random

#Print to stderr as defined in:
#http://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# List all network ports that don't listen to a network connection.
#
# @param string host The host to detect all available ports
# @param int from_port Minimum port value to the port range we want to scan. Default value 1024
# @param int to_port Maximum port value that we want to scan. Default value
#
# @return array
#
# @thrown Exception
def non_listening_ports(host,from_port,to_port):

    remoteServerIP  = socket.gethostbyname(host)

    #Try not to list system defined port
    if from_port == 0 :
        from_port=1024

    #Set to maximum
    if to_port == 0 :
        to_port=49151

    if from_port>to_port:
        raise Exception('Range is incorrectly given');

    #Store all closed ports
    available_ports=[]

    for port in range(from_port,to_port+1):
        #Open a network connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, port))
        if result != 0:
            available_ports.append(port)
        sock.close()

    return available_ports

# Exception that is used when an Invalid parameter is given
class InvalidParam(Exception):
    pass

#Exception that is used when a port has an incorrect value
class InvalidNetworkPort(Exception):
    pass

#Convert all input parameters as a dictionary
#@param array params The input parameters
#@return dictionary
def params_as_dictionary(params):

    final_params={}

    #Interating short parameters
    for params_ in params:
        for param in params_:
            key=param[0].lstrip('-')
            value=param[1].lstrip("=")
            final_params[key]=value

    return final_params

#Check if a value if a valid network port
#@param numeric string | int value
#@return boolean
def validate_port(value):
    value=int(value)
    if value>=1 and value<=49151:
        return value
    else:
        raise InvalidNetworkPort("This is not a valid port")


def get_atleast_one_int(param_dictionary,keys):

    for key in keys:
        value=param_dictionary.get(key,False)
        if  value!= False :
            return value

    return False

#Method that checks the input parameters
#@param  dictionart param_dictionary The dictionary of parameters
#@return dictionary containing theese keys:
#{
#   'localhost': Booelean that indicates if it will search on localhost or on 0.0.0.0
#   'from_port': The inclusive bottom start of the port range that we will scan
#   'to_port': The inclusive top end of the port range that we will scan
#}
def validate_params(param_dictionary):

    keys=param_dictionary.keys();

    return_params={}

    if('f' in keys and "from_port" in keys):
        raise InvalidParam("You cannot pass both -f and --from_port parameters")
    elif('t' in keys and "to_port" in keys):
        raise InvalidParam("You cannot pass both -t and --to_port parameters")
    else:
        return_params['localhost']=('l' in keys or "localhost" in keys)

        # Frox from_port
        try:
            from_port=get_atleast_one_int(param_dictionary,['f','from_port'])
            if from_port==False:
                from_port=0
            else:
                from_port=validate_port(from_port)

            return_params['from_port']=from_port
        except InvalidNetworkPort:
            raise InvalidParam('The -f or the --from_port does not contain a valid port number. It must be between 1 and 49151 inclusive')

        try:
            to_port=get_atleast_one_int(param_dictionary,['t','to_port'])
            if to_port==False:
                to_port=0
            else:
                to_port=validate_port(to_port)

            return_params['to_port']=to_port
        except InvalidNetworkPort:
            raise InvalidParam('The -t or the --to_port does not contain a valid port number. It must be between '+return_params['from_port']+' and 49151 inclusive')

        return return_params

#Get All Command Line parameters and sanitize them
def get_params():
    options=getopt.getopt(sys.argv[1:], "f:t:l", ["localhost","from_port=","to_port="])
    options=params_as_dictionary(options)
    options=validate_params(options)

    return options

#Main Calling function that runs as  an antrypoint
def main_function():

    host='0.0.0.0'

    try:
        params=get_params()
        if params['localhost']:
            host='localhost'

        ports_to_listen=non_listening_ports(host,params['from_port'],params['to_port'])
        print(random.choice(ports_to_listen))

    except InvalidParam,e:
        eprint(str(e))

main_function()
