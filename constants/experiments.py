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
    LONG_LENGTH_ERROR = 'long_length_error'


FLOW_STATUS = FlowStatus()


class TempLocalPath(object):
    TEMP_INPUT_AUDIO = 'temp_audio/input_audio_{}.m4a'
    TEMP_OUTPUT_AUDIO = 'temp_audio/output_audio_{}.m4a'
    TEMP_INPUT_VIDEO = 'temp_video/input_video_{}.mp4'
    TEMP_OUTPUT_VIDEO = 'temp_video/output_video_{}.mp4'


TEMP_LOCAL_PATH = TempLocalPath()

YOUTUBE_VIDEO_DURATION_LIMIT = 90

PROMPT_INPUT_LANG_MAPPING = {
    "default": "please try match speed and transcribe",
    "en": "Please try match speed and transcribe in english",
    "hi": "please try match speed and transcribe in hinglish",
    "mr": "please try match speed and transcribe in Marathi-English",
    "ta": "please try match speed and transcribe in Tanglish",
    "te": "please try match speed and transcribe in Telglish",
    "bn": "please try match speed and transcribe in Benglish",
}

ELEVENLABS_VOICE_ID_MAP = {
    "M": {
        'shah-rukh-khan': '2uIMnkULEb8HIcIhWtLF',
        'harsha-bhogle': 'tzc0mnukskitnp0xJrm8',
        'arnold': 'VR6AewLTigWG4xSOukaG',
        'antoni': 'ErXwobaYiN019PkySvjV',
        'bipin': 'pe8c86EFjKXrXlinhJbs',
        'male-hindi': 'yqfm2OSa0ihGWSEHH1yz',
    },
    "F": {
        'nissa': 'IBuG3Ez0yncjGriOosVn',
        'elli': 'MF3mGyEYCl7XYWbV9V6O',
        'ritu-female-indian': 'j37UtXn8QvFRVJWVDofA',
    },
    "default": 'IBuG3Ez0yncjGriOosVn'
}

PROMPT_OUTPUT_LANG_MAPPING = {
    ("default", "M"): "translate from english to {} as male",
    ("en", "M"): "translate script to english as male",
    ("hi", "M"): "Below text is transcribed from a youtube video please translate this to hinglish in hindi text as "
                 "male",
    ("mr", "M"): "translate text to Marathi & write in english script as male",
    ("ta", "M"): "Convert to Tanglish written in English script as male",
    ("te", "M"): "Translate to Telglish and return in English script as male accent",
    # ("bn", "M"): "",

    ("default", "F"): "translate from english to {} as female",
    ("en", "F"): "translate script to english as female",
    ("hi", "F"): "Below text is transcribed from a youtube video please translate this to hinglish in hindi text as "
                 "female",
    ("mr", "F"): "translate text to Marathi & write in english script as female",
    ("ta", "F"): "Convert to Tanglish written in English script as female tone",
    ("te", "F"): "Translate to Telglish and return in English script as female accent",
    # ("bn", "F"): "",

}

LANGUAGE_MAPPING = {
    'aa': 'Afar',
    'ab': 'Abkhazian',
    'ae': 'Avestan',
    'af': 'Afrikaans',
    'ak': 'Akan',
    'am': 'Amharic',
    'an': 'Aragonese',
    'ar': 'Arabic',
    'as': 'Assamese',
    'av': 'Avaric',
    'ay': 'Aymara',
    'az': 'Azerbaijani',
    'ba': 'Bashkir',
    'be': 'Belarusian',
    'bg': 'Bulgarian',
    'bh': 'Bihari languages',
    'bi': 'Bislama',
    'bm': 'Bambara',
    'bn': 'Bengali',
    'bo': 'Tibetan',
    'br': 'Breton',
    'bs': 'Bosnian',
    'ca': 'Catalan; Valencian',
    'ce': 'Chechen',
    'ch': 'Chamorro',
    'co': 'Corsican',
    'cr': 'Cree',
    'cs': 'Czech',
    'cu': 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic',
    'cv': 'Chuvash',
    'cy': 'Welsh',
    'da': 'Danish',
    'de': 'German',
    'dv': 'Divehi; Dhivehi; Maldivian',
    'dz': 'Dzongkha',
    'ee': 'Ewe',
    'el': 'Greek, Modern (1453-)',
    'en': 'English',
    'eo': 'Esperanto',
    'es': 'Spanish; Castilian',
    'et': 'Estonian',
    'eu': 'Basque',
    'fa': 'Persian',
    'ff': 'Fulah',
    'fi': 'Finnish',
    'fj': 'Fijian',
    'fo': 'Faroese',
    'fr': 'French',
    'fy': 'Western Frisian',
    'ga': 'Irish',
    'gd': 'Gaelic; Scomttish Gaelic',
    'gl': 'Galician',
    'gn': 'Guarani',
    'gu': 'Gujarati',
    'gv': 'Manx',
    'ha': 'Hausa',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'ho': 'Hiri Motu',
    'hr': 'Croatian',
    'ht': 'Haitian; Haitian Creole',
    'hu': 'Hungarian',
    'hy': 'Armenian',
    'hz': 'Herero',
    'ia': 'Interlingua (International Auxiliary Language Association)',
    'id': 'Indonesian',
    'ie': 'Interlingue; Occidental',
    'ig': 'Igbo',
    'ii': 'Sichuan Yi; Nuosu',
    'ik': 'Inupiaq',
    'io': 'Ido',
    'is': 'Icelandic',
    'it': 'Italian',
    'iu': 'Inuktitut',
    'ja': 'Japanese',
    'jv': 'Javanese',
    'ka': 'Georgian',
    'kg': 'Kongo',
    'ki': 'Kikuyu; Gikuyu',
    'kj': 'Kuanyama; Kwanyama',
    'kk': 'Kazakh',
    'kl': 'Kalaallisut; Greenlandic',
    'km': 'Central Khmer',
    'kn': 'Kannada',
    'ko': 'Korean',
    'kr': 'Kanuri',
    'ks': 'Kashmiri',
    'ku': 'Kurdish',
    'kv': 'Komi',
    'kw': 'Cornish',
    'ky': 'Kirghiz; Kyrgyz',
    'la': 'Latin',
    'lb': 'Luxembourgish; Letzeburgesch',
    'lg': 'Ganda',
    'li': 'Limburgan; Limburger; Limburgish',
    'ln': 'Lingala',
    'lo': 'Lao',
    'lt': 'Lithuanian',
    'lu': 'Luba-Katanga',
    'lv': 'Latvian',
    'mg': 'Malagasy',
    'mh': 'Marshallese',
    'mi': 'Maori',
    'mk': 'Macedonian',
    'ml': 'Malayalam',
    'mn': 'Mongolian',
    'mr': 'Marathi',
    'ms': 'Malay',
    'mt': 'Maltese',
    'my': 'Burmese',
    'na': 'Nauru',
    'nb': 'Bokmål, Norwegian; Norwegian Bokmål',
    'nd': 'Ndebele, North; North Ndebele',
    'ne': 'Nepali',
    'ng': 'Ndonga',
    'nl': 'Dutch; Flemish',
    'nn': 'Norwegian Nynorsk; Nynorsk, Norwegian',
    'no': 'Norwegian',
    'nr': 'Ndebele, South; South Ndebele',
    'nv': 'Navajo; Navaho',
    'ny': 'Chichewa; Chewa; Nyanja',
    'oc': 'Occitan (post 1500)',
    'oj': 'Ojibwa',
    'om': 'Oromo',
    'or': 'Oriya',
    'os': 'Ossetian; Ossetic',
    'pa': 'Panjabi; Punjabi',
    'pi': 'Pali',
    'pl': 'Polish',
    'ps': 'Pushto; Pashto',
    'pt': 'Portuguese',
    'qu': 'Quechua',
    'rm': 'Romansh',
    'rn': 'Rundi',
    'ro': 'Romanian; Moldavian; Moldovan',
    'ru': 'Russian',
    'rw': 'Kinyarwanda',
    'sa': 'Sanskrit',
    'sc': 'Sardinian',
    'sd': 'Sindhi',
    'se': 'Northern Sami',
    'sg': 'Sango',
    'si': 'Sinhala; Sinhalese',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'sm': 'Samoan',
    'sn': 'Shona',
    'so': 'Somali',
    'sq': 'Albanian',
    'sr': 'Serbian',
    'ss': 'Swati',
    'st': 'Sotho, Southern',
    'su': 'Sundanese',
    'sv': 'Swedish',
    'sw': 'Swahili',
    'ta': 'Tamil',
    'te': 'Telugu',
    'tg': 'Tajik',
    'th': 'Thai',
    'ti': 'Tigrinya',
    'tk': 'Turkmen',
    'tl': 'Tagalog',
    'tn': 'Tswana',
    'to': 'Tonga (Tonga Islands)',
    'tr': 'Turkish',
    'ts': 'Tsonga',
    'tt': 'Tatar',
    'tw': 'Twi',
    'ty': 'Tahitian',
    'ug': 'Uighur; Uyghur',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'uz': 'Uzbek',
    've': 'Venda',
    'vi': 'Vietlabelse',
    'vo': 'Volapük',
    'wa': 'Walloon',
    'wo': 'Wolof',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'za': 'Zhuang; Chuang',
    'zh': 'Chinese',
    'zu': 'Zulu'
}
