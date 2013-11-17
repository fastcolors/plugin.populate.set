
the plugin returns a list of items filter by the name of a Movie Set.

makes use of the new Gotham way of Filling a list from a directory/plugin
forum post: http://forum.xbmc.org/showthread.php?tid=176864

after creating the layout fill the content using

<content>plugin://plugin.populate.set/,$INFO[Container(%).ListItem.Label]</content>

the above example placed in MyVideoNav.xml fills the list up if item is a MovieSet when the content becomes visible.

So far seems to autoupdate with the selection of items in the main list.

Infolabels returned:

ListItem.Title
ListItem.OriginalTitle
ListItem.Year
ListItem.Duration
ListItem.Genre
ListItem.Studio
ListItem.Plot
ListItem.PlotOutline
ListItem.Tagline
ListItem.Rating
ListItem.MPAA
ListItem.Director
ListItem.Trailer
ListItem.Playcount
ListItem.LastPlayed
ListItem.Property(resumetime)
ListItem.Property(totaltime)
ListItem.Property(VideoCodec)
ListItem.Property(VideoResolution)
ListItem.Property(AudioCodec)
ListItem.Property(AudioChannels)

this is based on Skin.Widgets code so many thanks to the developers of that great service plugin!!

