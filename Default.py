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
#    This script is based on script.randomitems & script.wacthlist
#    Thanks to their original authors

import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import random
import urllib

if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

line = sys.argv[0]
title = line.replace("plugin://plugin.populate.set/,", "", 1);

print '----------------------'
print '----------------------'

print line
print title

print '----------------------'
print '----------------------'

__addon__        = xbmcaddon.Addon()
__addonversion__ = __addon__.getAddonInfo('version')
__addonid__      = __addon__.getAddonInfo('id')
__addonname__    = __addon__.getAddonInfo('name')
__localize__    = __addon__.getLocalizedString

def log(txt):
    message = '%s: %s' % (__addonname__, txt.encode('ascii', 'ignore'))
    xbmc.log(msg=message, level=xbmc.LOGDEBUG)


def fetch_movies():
    if not xbmc.abortRequested:
        json_string = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": { "filter": {"field": "set", "operator": "is", "value": "'+title+'"}, "limits": { "start" : 0, "end": 2147483647 },  "properties" : ["title", "fanart", "originaltitle", "studio", "trailer", "director", "year", "genre", "country", "tagline", "plot", "runtime", "file", "plotoutline", "rating", "resume", "art", "streamdetails", "set", "setid", "mpaa", "playcount", "lastplayed"], "sort": { "order": "ascending", "method": "title"} }, "id": "1"}'
        json_query = xbmc.executeJSONRPC('%s' %json_string )
        json_query = unicode(json_query, 'utf-8', errors='ignore')
 
        json_query = simplejson.loads(json_query)
        if json_query.has_key('result') and json_query['result'].has_key('movies'):
            for item in json_query['result']['movies']:
                if (item['resume']['position'] and item['resume']['total'])> 0:
                    resume = "true"
                    played = '%s%%'%int((float(item['resume']['position']) / float(item['resume']['total'])) * 100)
                else:
                    resume = "false"
                    played = '0%'
                if item['playcount'] >= 1:
                    watched = "true"
                else:
                    watched = "false"
                plot = item['plot']
                art = item['art']
                path = media_path(item['file'])

                play = 'XBMC.RunScript(' + __addonid__ + ',movieid=' + str(item.get('movieid')) + ')'
                streaminfo = media_streamdetails(item['file'].encode('utf-8').lower(), item['streamdetails'])


                # create a list item
                liz = xbmcgui.ListItem(item['title'])
                liz.setInfo( type="Video", infoLabels={ "Title": item['title'] })
                liz.setInfo( type="Video", infoLabels={ "OriginalTitle": item['originaltitle'] })
                liz.setInfo( type="Video", infoLabels={ "Year": item['year'] })
                liz.setInfo( type="Video", infoLabels={"Duration": item['runtime']/60})
                liz.setInfo( type="Video", infoLabels={ "Genre": " / ".join(item['genre']) })
                liz.setInfo( type="Video", infoLabels={ "Studio": item['studio'][0] })
                liz.setInfo( type="Video", infoLabels={ "Plot": plot })
                liz.setInfo( type="Video", infoLabels={ "PlotOutline": item['plotoutline'] })
                liz.setInfo( type="Video", infoLabels={ "Tagline": item['tagline'] })
                liz.setInfo( type="Video", infoLabels={ "Rating": str(float(item['rating'])) })
                liz.setInfo( type="Video", infoLabels={ "MPAA": item['mpaa'] })
                liz.setInfo( type="Video", infoLabels={ "Director": " / ".join(item['director']) })
                liz.setInfo( type="Video", infoLabels={ "Trailer": item['trailer'] })
                liz.setInfo( type="Video", infoLabels={ "Playcount": item['playcount'] })
                liz.setInfo( type="Video", infoLabels={ "LastPlayed": item['lastplayed'] })
                liz.setProperty("resumetime", str(item['resume']['position']))
                liz.setProperty("totaltime", str(item['resume']['total']))

                liz.setThumbnailImage(art.get('poster', ''))
                
                liz.setProperty("Country", item['country'][0])
                liz.setProperty("fanart_image", art.get('fanart', ''))
                
                liz.setProperty("VideoCodec", streaminfo['videocodec'])
                liz.setProperty("VideoResolution", streaminfo['videoresolution'])
                liz.setProperty("AudioCodec", streaminfo['audiocodec'])
                liz.setProperty("AudioChannels", str(streaminfo['audiochannels']))

                xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=item['file'],listitem=liz,isFolder=False)
        del json_query
        xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))
        
def media_path(path):
    # Check for stacked movies
    try:
        path = os.path.split(path)[0].rsplit(' , ', 1)[1].replace(",,",",")
    except:
        path = os.path.split(path)[0]
    # Fixes problems with rared movies and multipath
    if path.startswith("rar://"):
        path = [os.path.split(urllib.url2pathname(path.replace("rar://","")))[0]]
    elif path.startswith("multipath://"):
        temp_path = path.replace("multipath://","").split('%2f/')
        path = []
        for item in temp_path:
            path.append(urllib.url2pathname(item))
    else:
        path = [path]
    return path[0]

def media_streamdetails(filename, streamdetails):
    info = {}
    video = streamdetails['video']
    if '3d' in filename:
        info['videoresolution'] = '3d'
    elif video:
        videowidth = video[0]['width']
        videoheight = video[0]['height']
        if (video[0]['width'] <= 720 and video[0]['height'] <= 480):
            info['videoresolution'] = "480"
        elif (video[0]['width'] <= 768 and video[0]['height'] <= 576):
            info['videoresolution'] = "576"
        elif (video[0]['width'] <= 960 and video[0]['height'] <= 544):
            info['videoresolution'] = "540"
        elif (video[0]['width'] <= 1280 and video[0]['height'] <= 720):
            info['videoresolution'] = "720"
        elif (video[0]['width'] >= 1281 or video[0]['height'] >= 721):
            info['videoresolution'] = "1080"
        else:
            info['videoresolution'] = ""
    elif (('dvd') in filename and not ('hddvd' or 'hd-dvd') in filename) or (filename.endswith('.vob' or '.ifo')):
        info['videoresolution'] = '576'
    elif (('bluray' or 'blu-ray' or 'brrip' or 'bdrip' or 'hddvd' or 'hd-dvd') in filename):
        info['videoresolution'] = '1080'
    else:
        info['videoresolution'] = '1080'
    
    info['videocodec'] = video[0]['codec']
    info['audiocodec'] = ''
    info['audiochannels'] = ''
    return info

    
log('script version %s started' % __addonversion__)
fetch_movies()
log('script version %s stopped' % __addonversion__)