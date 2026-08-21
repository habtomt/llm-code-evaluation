`python

from google.cloud import videointelligence



def transcode_video(input_uri, output_uri, output_format, encoding_settings):

    client = videointelligence.TranscoderServiceClient()

    

    parent = client.common_location_path('[PROJECT]', '[LOCATION]')

    

    job = videointelligence.TranscodeVideoRequest.Job()

    job.output_uri = output_uri

    

    elementary_stream = videointelligence.ElementaryStream()

    elementary_stream.key = "video_stream"

    elementary_stream.video_stream = videointelligence.VideoStream()

    elementary_stream.video_stream.allow_open_gop = True

    elementary_stream.video_stream.h264 = videointelligence.VideoStream.H264CodecSettings()

    elementary_stream.video_stream.h264.bitrate_bps = encoding_settings['video_bitrate']

    

    audio_stream.key = "audio_stream"

    audio_stream.audio_stream = videointelligence.AudioStream()

    audio_stream.audio_stream.bitrate_bps = encoding_settings['audio_bitrate']

    

    job.elementary_streams = [elementary_stream, audio_stream]

    

    edit_list = videointelligence.EditList()

    edit_list.key = "list_1"

    edit_list.tracks = ["video_stream", "audio_stream"]

    edit_list.edits = [videointelligence.Edit()]

    

    job.edit_lists = [edit_list]

    

    response = client.transcode_video(parent=parent, job=job)

    print("Transcoding job created:", response)