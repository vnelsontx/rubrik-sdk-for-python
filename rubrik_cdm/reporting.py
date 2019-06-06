# Copyright 2018 Rubrik, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

"""
This module contains the Rubrik SDK Reporting class.
"""

from .api import Api
from .exceptions import InvalidParameterException, CDMVersionException, InvalidTypeException


class Reporting(Api):
    """This class contains methods related to the managment of the reporting functionality of the Rubrik cluster.
    """

    def create_common_reports(self, name, timeout=15):
        """Creates commonly used reports for a Rubrik cluster.
        
        Arguments:
            name {str} -- The type of common report that is being created. (choices: {average job duration, INCLUDE OTHERS HERE})
        
        Keyword Arguments:
            timeout {int} -- The number of seconds to wait to establish a connection the Rubrik cluster before returning a timeout error. (default: {15})
        
        Returns:
            dict -- The full API response from `POST /internal/report/'
        """

        valid_name = ['average job duration', 'INCLUDE OTHER REPORT NAMES']

        name = name.lower()

        if name not in valid_name:
            raise InvalidParameterException("The create_common_reports() name argument must be one of the following: {}.".format(
                valid_name))


        # self.log('cluster_version: Getting the software version of the Rubrik cluster.')



        # return self.get('v1', '/cluster/me/version', timeout=timeout)['version']

        if name == 'average job duration':
            config = {}
            config['name'] = "Average Job Duration - Last 7 Days"
            config['reportTemplate'] = "ProtectionTasksDetails"

            config['filters'] = {}
            config['filters']['dateConfig'] = {}
            config['filters']['dateConfig']['period'] = "PastWeek"

            config['chart0'] = {}
            config['chart0']['id'] = "chart0"
            config['chart0']['name'] = "Failed Tasks by SLA Domain"
            config['chart0']['chartType['] = "Donut"
            config['chart0']['attribute'] = "SlaDomain"
            config['chart0']['measure'] = "FailedTaskCount"

            config['chart1'] = {}
            config['chart1']['id'] = "chart1"
            config['chart1']['name'] = "Failed Tasks by Object Type"
            config['chart1']['chartType'] = "VerticalBar"
            config['chart1']['attribute'] = "ObjectName"
            config['chart1']['measure'] = "FailedTaskCount"

            config['table'] = {}
            config['table']['columns'] = ["TaskStatus", "TaskType", "ObjectName", "ObjectType", "Location", "SlaDomain", "StartTime", "EndTime", "Duration", "DataTransferred", "DataStored"]

            return self.post('internal', '/report', config)