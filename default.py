#     Copyright (C) 2012 Team-XBMC
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#    This script is based on service.data.provider & service.skin.widgets
#    Thanks to the original authors

import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

__addon__        = xbmcaddon.Addon()
__addonversion__ = __addon__.getAddonInfo('version')
__addonid__      = __addon__.getAddonInfo('id')
__addonname__    = __addon__.getAddonInfo('name')
__localize__    = __addon__.getLocalizedString

full_liz = list()

def log(txt):
    message = '%s: %s' % (__addonname__, txt.encode('ascii', 'ignore'))
    xbmc.log(msg=message, level=xbmc.LOGDEBUG)


def fetch_episodes():
    if not xbmc.abortRequested:
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"properties": ["title", "studio", "mpaa", "file", "art"], "sort": {"order": "descending", "method": "lastplayed"}, "filter": {"field": "inprogress", "operator": "true", "value": ""}, "limits": {"end": 24}}, "id": 1}')
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        json_query = simplejson.loads(json_query)
        print json_query
        if json_query.has_key('result') and json_query['result'].has_key('tvshows'):

            for item in json_query['result']['tvshows']:
                json_query2 = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"tvshowid": %d, "properties": ["title", "season", "episode", "showtitle", "file", "lastplayed", "rating", "resume", "art", "dateadded"], "sort": {"method": "episode"}, "filter": {"field": "playcount", "operator": "is", "value": "0"}, "limits": {"end": 1}}, "id": 1}' %item['tvshowid'])
                json_query2 = unicode(json_query2, 'utf-8', errors='ignore')
                json_query2 = simplejson.loads(json_query2)
                if json_query2.has_key('result') and json_query2['result'].has_key('episodes'):
                    for item2 in json_query2['result']['episodes']:
                        # create a list item
                        liz = xbmcgui.ListItem(item2['title'])
                        liz.setInfo( type="Video", infoLabels={ "Title": item2['title'] })
                        liz.setInfo( type="Video", infoLabels={ "Episode": item2['episode'] })
                        liz.setInfo( type="Video", infoLabels={ "Season": item2['season'] })
                        liz.setInfo( type="Video", infoLabels={ "TVshowTitle": item2['showtitle'] })
                        liz.setInfo( type="Video", infoLabels={ "Rating": str(round(float(item2['rating']),1)) })
                        liz.setInfo( type="Video", infoLabels={ "MPAA": item['mpaa'] })

                        liz.setProperty("resumetime", str(item2['resume']['position']))
                        liz.setProperty("totaltime", str(item2['resume']['total']))
                        liz.setArt(item2['art'])
                        liz.setThumbnailImage(item2['art'].get('thumb',''))
                        liz.setIconImage('DefaultTVShows.png')

                        full_liz.append((item2['file'], liz, False))
                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=item2['file'],listitem=liz,isFolder=False)
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))
        del json_query

log('script version %s started' % __addonversion__)
fetch_episodes()
log('script version %s stopped' % __addonversion__)