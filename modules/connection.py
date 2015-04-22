#!/usr/bin/env python
#
# This file is part of lava-ci.  lava-ci is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# Copyright Tyler Baker 2015

import xmlrpclib
import urlparse


def handle_connection(func):
    """
    Decorator used to handle XMLRPC errors.
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except xmlrpclib.ProtocolError as e:
            if e.errcode == 502:
                print 'Protocol Error: 502 Bad Gateway, retrying...'
            elif e.errcode == 401:
                print 'Server authentication error.'
                print e
                exit(1)
            else:
                print 'Unknown XMLRPC error.'
                print e
                return None
        except xmlrpclib.Fault as e:
            if e.faultCode == 404 and e.faultString == \
                    'Job output not found.':
                pass
        except (IOError, Exception) as e:
            print 'Function %s raised an exception, exiting...' % func.__name__
            print e
            exit(1)
    return inner


class Connection(object):

    def __init__(self, user, token, server):
        """
        Abstracts a LAVA server connection.
        :string : user
        :string : token
        :string : server
        """
        self._user = user
        self._token = token
        self._server = server
        self._url = self.validate_input(self._user, self._token, self._server)
        self._connection = None

    @handle_connection
    def validate(self):
        """
        Validates the connection by calling a simple method.
        :self : object
        """
        print "Validating connection..."
        self._connection.system.listMethods()

    @handle_connection
    def connect(self):
        """
        Creates a connection to a LAVA server.
        """
        print 'Connecting to Server...'
        self._connection = xmlrpclib.ServerProxy(self._url)
        self.validate()
        print 'Connection Successful.'
        print 'connect-to-server : pass'

    @handle_connection
    def get_job_details(self, job_id):
        """
        Returns the job details from a LAVA server in JSON format.
        :int : job_id
        """
        return self._connection.scheduler.job_details(job_id)

    @handle_connection
    def get_job_log(self, job_id):
        """
        Returns the job output from a LAVA server as a string.
        :int : job_id
        """
        return str(self._connection.scheduler.job_output(job_id))

    @handle_connection
    def get_bundle(self, bundle_id):
        """
        Returns the bundle from a LAVA server in JSON format.
        :int : bundle_id
        """
        return self._connection.dashboard.get(bundle_id)

    @staticmethod
    def validate_input(user, token, server):
        url = urlparse.urlparse(server)
        if url.path.find('RPC2') == -1:
            print "LAVA Server URL must end with /RPC2"
            exit(1)
        return url.scheme + '://' + user + ':' + token + '@' + url.netloc + url.path
