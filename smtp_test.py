#!/usr/bin/env python

from smtplib import SMTP
from smtplib import SMTP_SSL
from smtplib import SMTPConnectError
from smtplib import SMTPAuthenticationError
from smtplib import SMTPServerDisconnected
from smtplib import SMTPException
from ssl import SSLError
from socket import gaierror
from termcolor import colored
from time import sleep

import argparse
from tabulate import tabulate

def smtp_quit(smtp):
    '''   
    Quiting SMTP Connection regardless if the smtp has been connected or not
    :param smtp: 
    :return: 
    '''
    try:
        smtp.quit()
    except SMTPServerDisconnected:
        pass

def check_smtp_no_ssl(hostname, port, username=None, password=None):
        '''
        Test the SMTP Connection if can connect and auth
        :param hostname: The smtp hostname
        :param port:  The smtp port
        :param username: The smtp username (Optional)
        :param password: The smtp passworf (Optional)
        
        :return: A dictionary with the results
        '''
        smtp = SMTP()
        connection_report=test_connection(smtp,hostname,port,username,password)
        smtp_quit(smtp)
        return connection_report

def check_smtp_ssl(hostname, port, username="", password=""):
    '''
    Test the SMTP Connection if can connect and auth using SSL
    :param hostname: The smtp hostname
    :param port:  The smtp port
    :param username: The smtp username (Optional)
    :param password: The smtp passworf (Optional)
    
    :return: A dictionary with the results
    '''
    smtp=SMTP_SSL()
    connection_report = test_connection(smtp, hostname, port, username, password)

    smtp_quit(smtp)

    return connection_report


def check_smtp_star_tls(hostname, port, username=None, password=None):
    '''
    Test the SMTP Connection if can connect and auth
    :param hostname: The smtp hostname
    :param port:  The smtp port
    :param username: The smtp username (Optional)
    :param password: The smtp passworf (Optional)

    :return: A dictionary with the results
    '''
    smtp = SMTP()
    connection_report = test_connection(smtp, hostname, port, username, password,True)
    smtp_quit(smtp)
    return connection_report

def test_if_can_connect (smtp, hostname, port, tls=False):

    try:
        smtp.connect(hostname, port)
        smtp.ehlo()
        if (tls == True):
            smtp.starttls()
            smtp.ehlo()
        return True
    except :
        return False


def test_if_can_auth(smtp,username,password):
    try:
        smtp.login(username,password)
        return True
    except:
        return False

def test_connection(smtp,hostname,port,username=None,password=None,tls=False):

    '''
    A generic wat to test the SMTP Connection
    :param smtp: The smtp Object
    :param hostname: The smtp hostname
    :param port:  The smtp port
    :param username: The smtp username (Optional)
    :param password: The smtp passworf (Optional) 
    
    :return: A dictionary with the results
    '''

    tests={'connection':False,'auth':False}
    tests['connection']=test_if_can_connect(smtp,hostname,port,tls)

    if[tests['connection'] == True and username is not None and password is not None]:
        tests['auth']=test_if_can_auth(smtp,username,password)

    return tests

def getArguments():
    '''
    Parsing Command line Arguments
    :return: 
    '''
    parser=argparse.ArgumentParser(description="An SMTP Reporting Tool")
    parser.add_argument('smtp_server',metavar="SMTP_SERVER",type=str,help="The smtp server url")
    parser.add_argument('--username',metavar="SMTP_USERNAME",type=str, default=None,help="The smtp username")
    parser.add_argument('--password', metavar="SMTP_USERNAME", type=str, default=None, help="The smtp username")
    parser.add_argument('--ports',nargs="*",metavar="SMTP_PORT",type=int,default=None,help="The smtp port. Appnd values in order to append values to standart port test")

    return parser.parse_args()

def print_full_report(report,host):
    '''
    Prints the Report fir the connection tests
    :param report: 
    :param host: 
    :return: 
    '''
    print "Testing SMTP Connection on: %s\n" % (colored(host,'cyan'))
    print "No SSL Connection:"
    print_report(report,'no_ssl')
    print "\nSSL Connection"
    print_report(report, 'ssl')
    print "\n Star TLS Tests"
    print_report(report, 'startls')

def print_report(report,what_to_print):
    strings=[]
    header=["Port","Connection Status","Login Status"]

    for key,value in report.iteritems():
        output=[str(key)]
        value=value[what_to_print]
        output.append(get_ok_or_fail_colored(value['connection']))
        output.append(get_ok_or_fail_colored(value['auth']))
        strings.append(output)

    print tabulate(strings,headers=header,tablefmt="simple")

def get_ok_or_fail_colored(bool):
    if(bool== True):
        return colored('OK','green')
    else:
        return colored('FAIL','red')

#Common smtp ports
smtp_ports=[25,2525,587,465,2526]

args=getArguments()

if(args.ports is not None):
    smtp_ports=args.ports

#Storing the reports into seperate arrays
reports={}

for port in smtp_ports:
    report = {'ssl':None,'no_ssl':None}
    report['no_ssl'] = check_smtp_no_ssl(args.smtp_server, port, args.username, args.password)
    report['ssl'] = check_smtp_ssl(args.smtp_server, port, args.username, args.password)
    report['startls'] = check_smtp_star_tls(args.smtp_server, port, args.username, args.password)
    reports[port]=report

print_full_report(reports,args.smtp_server)