# Copyright (c) 2013 Martin Abente Lahaye. - martin.abente.lahaye@gmail.com
# Arturo Volpe Torres. - arturovolpe@gmail.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

import json
import urllib
import urllib2
import urlparse

from setting import Setting
import datetime



class TimeEntry(object):

    DATE_FORMAT = '%Y-%m-%d'
    TIME_ENTRY_GET_URL = 'time_entries/%s.json'
    TIME_ENTRY_GET_ALL_URL = 'time_entries.json'
    TIME_ENTRY_POST_URL = 'time_entries.json'


    def __init__(self, issue):
        self.issue= issue
        self._setting = Setting()
        


    def add(self, date, hours, activity_id, comment):
        if not activity_id:
            activity_id = self._setting.get_default_activity()
        if not date:
            now = datetime.datetime.now()
            date = now.strftime(self.DATE_FORMAT)
        data = {
            "time_entry[issue_id]" : self.issue,
            "time_entry[spent_on]" : date,
            "time_entry[hours]" : str(hours),
            "time_entry[activity_id]" : int(activity_id),
            "time_entry[comments]" : str(comment)
        }

        try:
            response = json.loads(self._post(data))
            response['code'] = 201
            return response
        except  urllib2.HTTPError as err:
            response = {"code" :  err.code}
            if err.code == 422:
                response['messages'] = json.loads(err.read())['errors']
            else:
                response['messages'] = err.read()
            return response


    def _post(self, data):
        url = self._get_full_post_url()
        headers = {
            'X-Redmine-API-Key' : self._setting.get_key()
            }
        #headers['Content-Type'] = 'application/json'
        req = urllib2.Request(url, urllib.urlencode(data, False), headers)

        try:
            response = urllib2.urlopen(req)
        except urllib2.HTTPError as err:
            raise err
        else:
            return response.read()


    def _get_full_post_url(self):
        return urlparse.urljoin(self._setting.get_host(),
                                self.TIME_ENTRY_POST_URL)
