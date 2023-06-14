class FlowStatus(object):
    IN_QUEUE = 'in_queue'
    AUDIO_VIDEO_SEPARATION_IN_PROGRESS = 'audio_video_separation_in_progress'
    AUDIO_VIDEO_SEPARATION_COMPLETED = 'audio_video_separation_completed'
    TRANSCRIPTION_IN_PROCESS = 'transcription_in_process'
    TRANSCRIPTION_COMPLETED = 'transcription_completed'
    TEXT_TO_SPEECH_IN_PROCESS = 'text_to_speech_in_process'
    TEXT_TO_SPEECH_COMPLETED = 'text_to_speech_completed'
    MERGING_AUDIO_VIDEO_IN_PROCESS = 'merging_audio_video_in_process'
    MERGING_AUDIO_VIDEO_COMPLETED = 'merging_audio_video_completed'
    UPLOADING_VIDEO = 'uploading_video'
    COMPLETED = 'completed'


FLOW_STATUS = FlowStatus()


class TempLocalPath(object):
    TEMP_INPUT_AUDIO = 'temp_audio/input_audio_{}.m4a'
    TEMP_OUTPUT_AUDIO = 'temp_audio/output_audio_{}.m4a'
    TEMP_INPUT_VIDEO = 'temp_video/input_video_{}.mp4'
    TEMP_OUTPUT_VIDEO = 'temp_video/output_video_{}.mp4'


TEMP_LOCAL_PATH = TempLocalPath()
