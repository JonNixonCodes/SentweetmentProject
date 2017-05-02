# list all emojiis
from emoji import UNICODE_EMOJI, EMOJI_UNICODE

emojis = list(UNICODE_EMOJI.keys())
for e in emojis:
    print(UNICODE_EMOJI[e] + ' ' + e)

happy_emoji_codes = [':grinning_face:',
                ':grinning_face_with_smiling_eyes:',
                ':face_with_tears_of_joy:',
                ':rolling_on_the_floor_laughing:',
                ':smiling_face_with_open_mouth:',
                ':smiling_face_with_open_mouth_&_smiling_eyes:',
                ':smiling_face_with_open_mouth_&_cold_sweat:',
                ':smiling_face_with_open_mouth_&_closed_eyes:',
                ':winking_face:',
                ':smiling_face_with_smiling_eyes:',
                ':face_savouring_delicious_food:',
                ':smiling_face_with_sunglasses:',
                ':smiling_face_with_heart-eyes:',
                ':face_blowing_a_kiss:',
                ':kissing_face:',
                ':kissing_face_with_smiling_eyes:',
                ':smiling_face:',
                ':slightly_smiling_face:',
                ':hugging_face:']

neutral_emoji_codes = [":thinking_face:",
                  ":neutral_face:",
                  ":expressionless_face:",
                  ":face_without_mouth:",
                  ":face_with_rolling_eyes:",
                  ":smirking_face:",
                  ":persevering_face:",
                  ":disappointed_but_relieved_face:",
                  ":face_with_open_mouth:",
                  ":zipper-mouth_face:",
                  ":hushed_face:",
                  ":sleepy_face:",
                  ":tired_face:",
                  ":sleeping_face:",
                  ":relieved_face:",
                  ":face_with_stuck-out_tongue:",
                  ":face_with_stuck-out_tongue_&_winking_eye:",
                  ":face_with_stuck-out_tongue_&_closed_eyes:",
                  ":drooling_face:",
                  ":unamused_face:",
                  ":face_with_cold_sweat:",
                  ":pensive_face:",
                  ":confused_face:",
                  ":upside-down_face:",
                  ":money-mouth_face:",
                  ":astonished_face:"]

sad_emoji_codes = [":frowning_face:",
              ":slightly_frowning_face:",
              ":confounded_face:",
              ":disappointed_face:",
              ":worried_face:",
              ":face_with_steam_from_nose:",
              ":crying_face:",
              ":loudly_crying_face:",
              ":frowning_face_with_open_mouth:",
              ":anguished_face:",
              ":fearful_face:",
              ":weary_face:",
              ":grimacing_face:",
              ":face_with_open_mouth_&_cold_sweat:",
              ":face_screaming_in_fear:",
              ":flushed_face:",
              ":dizzy_face:",
              ":pouting_face:",
              ":angry_face:"]

happy_emoji = {}
for e in happy_emoji_codes:
    happy_emoji[e] = EMOJI_UNICODE[e]
    print(e + ' ' + EMOJI_UNICODE[e])

neutral_emoji = {}
for e in neutral_emoji_codes:
    neutral_emoji[e] = EMOJI_UNICODE[e]
    print(e + ' ' + EMOJI_UNICODE[e])

sad_emoji = {}
for e in sad_emoji_codes:
    sad_emoji[e] = EMOJI_UNICODE[e]
    print(e + ' ' + EMOJI_UNICODE[e])
    
