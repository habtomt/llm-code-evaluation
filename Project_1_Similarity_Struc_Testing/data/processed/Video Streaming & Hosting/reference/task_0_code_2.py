`python

import vimeo_ott

live_stream =vimeo_ott .create_live_stream (title ="Live Stream Title",description ="Live Stream Description",max_concurrent_streams =10 ,adaptable_resolution =True )

broadcast_url =vimeo_ott .start_broadcast (live_stream_id =live_stream .id )

live_stream_details =vimeo_ott .get_live_stream_details (live_stream_id =live_stream .id )

vimeo_ott .stop_broadcast (live_stream_id =live_stream .id )