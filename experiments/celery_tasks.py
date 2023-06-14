from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def separate_audio_from_file(video_id):
    import os
    from yt_dlp import YoutubeDL
    from experiments.models import Video
    from constants import TEMP_LOCAL_PATH, FLOW_STATUS
    try:
        video = Video.objects.get(pk=video_id)
    except Video.DoesNotExist:
        return
    video.status = FLOW_STATUS.AUDIO_VIDEO_SEPARATION_IN_PROGRESS
    video.save()

    output_file = TEMP_LOCAL_PATH.TEMP_INPUT_AUDIO.format(video_id)
    if os.path.isfile(output_file):
        return
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'paths': {'home': output_file.split('/')[0]},
        'outtmpl': {'default': output_file.split('/')[1]},
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }
    with YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download([video.youtube_url])
        if error_code != 0:
            raise Exception('Failed to download video')

    video.status = FLOW_STATUS.AUDIO_VIDEO_SEPARATION_COMPLETED
    video.save()
    create_transcription(video_id=video_id)
    extract_title(video_id=video_id)


@shared_task
def create_transcription(video_id):
    from django.conf import settings
    import openai
    from experiments.models import Video
    from constants import TEMP_LOCAL_PATH, FLOW_STATUS

    try:
        video = Video.objects.get(pk=video_id, transcription__isnull=True)
    except Video.DoesNotExist:
        return
    video.status = FLOW_STATUS.TRANSCRIPTION_IN_PROCESS
    video.save()
    openai.api_key = settings.OPEN_AI_TOKEN
    audio_file = open(TEMP_LOCAL_PATH.TEMP_AUDIO.format(video.id), "rb")
    transcript = openai.Audio.transcribe(
        model="whisper-1",
        file=audio_file,
        response_format='text',
        language=video.output_language,
        temperature=0.2
    )
    video.status = FLOW_STATUS.TRANSCRIPTION_COMPLETED
    video.transcription = transcript
    video.save()


@shared_task
def extract_title(video_id):
    import requests
    from bs4 import BeautifulSoup
    from experiments.models import Video

    try:
        video = Video.objects.get(pk=video_id)
    except Video.DoesNotExist:
        return
    try:
        response = requests.get(video.youtube_url)
        soup = BeautifulSoup(response.text, "html.parser")
        title_element = soup.find("meta", property="og:title")
    except Exception:
        return
    title = title_element["content"]
    if title:
        video.title = title
        video.slug = video.get_unique_slug()
        video.save()


@shared_task
def convert_text_to_speech(video_id):
    import requests

    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "<xi-api-key>"
    }

    data = {
        "text": "'नमस्ते। मैं आपको 10 पुस्तकों का सुझाव देने जा रहा हूँ और ये सभी विभिन्न श्रेणियों के आधार पर क्रमबद्ध हैं। ठीक है, और मुझे प्रत्येक पुस्तक पर कुछ टिप्पणियाँ करनी हैं। तो चलिए शुरू करते हैं किताब नंबर एक के साथ जो पहले साइंस फिक्शन पर है। डार्क मैटर बाय ब्लेक क्राउच यह एक बहुत ही रचनात्मक किताब है। हो सकता है कि क्रिस्टोफर नोलन इससे बाहर एक फिल्म बना सके। अगला। एक कठिन विज्ञान आधारित विज्ञान विज्ञान पर है, और यह एंडी बर्र द्वारा प्रोजेक्ट हेल मैरी है। यदि आप अंतरिक्ष में हैं और आपको विज्ञान पसंद है और आप दोनों के संयोजन को पसंद करते हैं, तो यह पुस्तक आप मिस नहीं कर सकते, यह आश्चर्यजनक है। पढ़ना। यह सर्वश्रेष्ठ में से एक है। मुझ पर विश्वास करें अगला एक आध्यात्मिकता पर है। सैम हैरिस द्वारा वेकिंग अप यह मेरे निजी पसंदीदा में से एक है। मुझे यह किताब बहुत पसंद है। आप इस पुस्तक को पढ़ सकते हैं यदि आप स्वयं को प्रबुद्ध करना चाहते हैं और आप आध्यात्मिकता और धर्म के बारे में अधिक जानना चाहते हैं, और आपको बहुत सी चीजों को अनलकी करने का मौका भी मिल सकता है। कुछ अनावश्यक चीजें जो शायद अभी आपके दिमाग में हैं जिनके बारे में आपको पता भी नहीं है। आप इस पुस्तक का उपयोग करके उस चीज को भूल सकते हैं। यह एक महान पठन है। सबसे अच्छे में से एक। मैंने इस पुस्तक के उन अनुच्छेदों पर बहुत सारे अंक रखे हैं जो मुझे पसंद आए हैं। और हाइलाइट करने के लिए बहुत कुछ है क्योंकि इस पुस्तक के अंदर रत्नों के कुछ असली टुकड़े हैं और आप इसे पसंद करने वाले हैं। अगला प्रकृति और शून्य होने पर है। हाँ, शून्यता। तो इस श्रेणी में दो पुस्तकें हैं जो मैंने आपके लिए रखी हैं। पहला यह है कि कैसे कुछ न करें। और अगला मौन है। अद्भुत किताब। ये दोनों पुस्तकें आपको अपने और प्रकृति के साथ और अधिक जोड़ने वाली हैं, और वे वैराग्य और शांति पैदा करने में आपकी मदद करने वाली हैं। यह आपको शांति देने वाला है। अगला दर्शनशास्त्र पर है। आप में से बहुत से लोग इस विषय को पसंद करते हैं। मुझे पता है। और यदि आप अभी इस क्षेत्र में शुरुआत कर रहे हैं, तो यह वह पुस्तक है जिसे आप दर्शन का प्रवेश द्वार कह सकते हैं। किताब का नाम सुअर है जो खाना चाहता है। इसमें 100 विचार प्रयोग हैं, और प्रत्येक प्रयोग में कुछ वास्तविक मोड़ और मोड़ हैं। आप प्यार को पसंद करने वाले हैं, जिस तरह से लेखक आपको एक तरफ से दूसरी तरफ शिफ्ट करने जा रहा है और आप जैसे होंगे, आप इतने उछालभरी होंगे। आप जैसे होंगे, हां, मैं हां, मैंने सुना है कि यह ऐसा है, आप जानते हैं? अब कल्पना आती है। हाँ। हमें फिक्शन भी पसंद है, ठीक है, सिडनी? शेल्डन, उससे बेहतर क्या होगा. तो, सिडनी शेल्डन, क्या इस पर कई किताबें हैं, उम, इस लेखक द्वारा, और, उह, वे ज्यादातर नाटक और बहुत सारे और बहुत सारे विश्वासघात और बहुत सारी भावनाओं से भरे हुए हैं। और वे पेज टर्नर हैं। जैसे मैंने अभी-अभी फरिश्तों के इस एक क्रोध को पढ़ा। मैंने इसे अभी पिछले तीन या चार महीनों में पूरा किया है, और यह बहुत दिलचस्प था। तो आप सचमुच सिडनी शेल्डन की हर किताब से एक फिल्म बना सकते हैं। ये किताबें कितनी नाटकीय हैं। टोटल पेज टर्नर, टोटल पेज टर्नर। अगला अजीब, विचित्र पर है। और किताब का नाम है डाइस मैन। यह एक ऐसे व्यक्ति के बारे में है जो जीवन के हर फैसले को पासा पलट कर लेता है। हाँ, पूरी तरह पागल किताब। पुस्तक का आनंद लें। पढ़कर आनंद लें। कई ऐसे फैसले होते हैं जहां हम भ्रमित हो जाते हैं। तो इस शख्स ने अपनी इस समस्या का हल ढूंढ लिया है। वह पासा फेंकेगा, और हर बार, पासा जो भी जवाब देगा, वह अपने जवाब पर इसी तरह की प्रतिक्रिया देगा। मेरा मतलब है, उसके लिए यही चुनाव होने वाला है। इसी तरह वह जीवन जी रहा है, और किताब इसी के बारे में है। अगली श्रेणी नॉनफिक्शन है, और इस श्रेणी में दो पुस्तकें हैं। पहला है चेकलिस्ट घोषणापत्र हाँ, अतुल काडे द्वारा और अगला अनुमानित रूप से तर्कहीन है। तो यह पुस्तक जीवन और कार्य में सूची के महत्व के बारे में बात करती है, और दूसरी मानव सोच की कमियों, उन नीतियों और पूर्वाग्रहों के बारे में बात करती है जिनके आगे हम झुक जाते हैं। एक स्टार्ट अप व्यापार दक्षता और स्पष्टता पर है, और पुस्तक का नाम लड़की है। हाँ, यह किताब है। यह एक घाटे में चल रही निर्माण फैक्ट्री के बारे में है, जो चीजों को एक जीनियस की मदद से घुमाती है, जो फैक्ट्री के प्रबंधक को दिखाती है कि पहली जगह में क्या स्पष्ट होना चाहिए था। और आखिरी वाला आत्म विकास पर है, और किताब का नाम है एटॉमिक हैबिट्स। मुझे पता है कि आप में से कई लोग इसके बारे में पहले ही सुन चुके हैं। हाँ, यह एक बहुत प्रसिद्ध किताब है। यह, उम, विकासशील आदतों की अवधारणा के बारे में है, और लेखक ने इस निर्माण की आदतों को हमारे लिए बहुत सुलभ और बहुत आसान बनाकर वास्तव में एक अच्छा काम किया है। इसलिए यदि आप किताब पढ़ते हैं, तो शायद अगली बार जब आप कोई आदत चुनना चाहें। आपके लिए यह आसान होने वाला है। तो आज के वीडियो में बस इतना ही। मुझे आशा है कि आपने इनमें से कम से कम एक या दो पुस्तकों के साथ शुरुआत की है जिनकी मैंने अनुशंसा की है। मुझे बताएं कि क्या आप इनमें से किसी एक को पहले ही टिप्पणियों में पढ़ चुके हैं, ठीक है? और वह भी जिसे आपने आगे पढ़ने के लिए चुना है। ठीक है, तो आगे बढ़ो। मैं तुम्हें फिर से देखूंगा और मैं अपनी किताबों पर वापस आऊंगा। अलविदा।",
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)
    with open('output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)


@shared_task
def replace_video_audio(video_id):
    import os
    from yt_dlp import YoutubeDL
    from experiments.models import Video
    from constants import TEMP_LOCAL_PATH

    try:
        video = Video.objects.get(pk=video_id)
    except Video.DoesNotExist:
        return

    # Step 1: Download the YouTube video
    output_file = TEMP_LOCAL_PATH.TEMP_INPUT_VIDEO.format(video_id)
    with YoutubeDL({
        'format': 'bestvideo[height<=480][ext=mp4]/best[ext=mp4][height<=480]',
        'outtmpl': output_file,
    }) as ydl:
        ydl.download([video.youtube_url])

    # Add audio to video
    ffmpeg_command = 'ffmpeg -i "{video_path}" -i "{audio_file}" -c:v copy -map 0:v:0 -map 1:a:0 -shortest "{output_path}"'.format(
        video_path=output_file,
        audio_file=TEMP_LOCAL_PATH.TEMP_OUTPUT_AUDIO.format(video_id),
        output_path=TEMP_LOCAL_PATH.TEMP_OUTPUT_VIDEO.format(video_id),
    )
    os.system(ffmpeg_command)

@shared_task
def upload_video_to_youtube():
    import os
    import googleapiclient.discovery
    from google.oauth2 import service_account

    # Set your API credentials file path
    api_credentials_file = 'path/to/credentials.json'

    # Set the path of the video file to be uploaded
    video_file_path = 'path/to/video.mp4'

    # Set the title, description, and tags for the uploaded video
    video_title = 'My Uploaded Video'
    video_description = 'Description of my video'
    video_tags = ['tag1', 'tag2', 'tag3']

    # Authenticate and create a YouTube Data API client
    credentials = service_account.Credentials.from_service_account_file(api_credentials_file, scopes=[
        'https://www.googleapis.com/auth/youtube.upload'])
    youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)

    # Create a request body with video details
    request_body = {
        'snippet': {
            'title': video_title,
            'description': video_description,
            'tags': video_tags
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    # Create the video insert request
    insert_request = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=googleapiclient.http.MediaFileUpload(video_file_path, chunksize=-1, resumable=True)
    )

    # Execute the video insert request
    response = None
    while response is None:
        status, response = insert_request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    # Print the uploaded video details
    print("Video uploaded! Video ID: {response['id']}")

# import boto3
# from django.conf import settings
#
# job_name = '84dc02e6-4bfe-4c2b-84c5-5572fa879dSSS536'
#
# client = boto3.client('transcribe', region_name=settings.AWS_SECRET_MANAGER_REGION)
# response = client.start_transcription_job(
#     TranscriptionJobName=job_name,
#     Media={
#         'MediaFileUri': 'https://kukufm.s3.ap-south-1.amazonaws.com/audio_2.m4a'
#     },
#     OutputBucketName='kukufm',
#     OutputKey='audio-transcripts/' + job_name + '.json',
#     IdentifyLanguage=True,
# )
#
# # Get job status
# client.get_transcription_job(TranscriptionJobName=job_name)
