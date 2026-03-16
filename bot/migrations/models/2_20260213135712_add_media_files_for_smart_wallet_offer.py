from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
           INSERT INTO media (id, code, file_id, offer_id)
           VALUES 
                  (1, 'тест-лид-магнит.mp4', 'BAACAgIAAxkBAAIHQWmHoPpWJqCaD88jMuzjB38SukuZAAJsgAACOg1hS6W3p8hD8EfHOgQ', 1),
                  (2, 'тест-Чек-лист_20_мест_утечки_денег.pdf', 'BQACAgIAAxkBAAIHVWmHojUXuAqybz2H1_e-n2GJecnbAAKBnQACO085SG9SOgtFOEsZOgQ', 1),
                  (3, 'тест-V1_krujok_jadnost.mp4', 'DQACAgIAAxkBAAIHXWmHol1E93Pr0dQBHbwoA3OTN15rAAKZqAAC-ZoISLKMBnQ5TztZOgQ', 1),
                  (4, 'тест-V2_krujok_metod.mp4', 'DQACAgIAAxkBAAIHZWmHon-7gZquVjCxxBN6_ju8cqEaAAL3qAAC-ZoISBPLQNRva6pAOgQ', 1),
                  (5, 'otzyv_1.jpg', 'AgACAgIAAxkBAAIHbWmHoqx5mDBqFonY02_KWFWDc9KIAALTC2sbeDghSKgkD42Y93pZAQADAgADeQADOgQ', 1),
                  (6, 'otzyv_2.jpg', 'AgACAgIAAxkBAAIHdWmHosDCcJ1VbiWP0n70XvA2T6KoAALUC2sbeDghSAS1L97x7b5LAQADAgADeQADOgQ', 1),
                  (7, 'otzyv_3.jpg', 'AgACAgIAAxkBAAIHeWmHos_ReY2bFbDSXk7T6hb-QbBKAALVC2sbeDghSDh2jiQagFe1AQADAgADeQADOgQ', 1),
                  (8, 'otzyv_4.jpg', 'AgACAgIAAxkBAAIHhmmHoxO84J8Qj2lrWXL8rAtj4yM-AALXC2sbeDghSIuOGsyHjXmfAQADAgADeQADOgQ', 1),
                  (9, 'otzyv_5.jpg', 'AgACAgIAAxkBAAIHjmmHoyy6gAkWehILo_pNyehs8j2UAALYC2sbeDghSKcQxImjaJIeAQADAgADeQADOgQ', 1),
                  (10, 'лид-магнит.mp4', 'BAACAgIAAxkBAAINXGmre5yMcEVAg9XnO2qj83X6z06HAALCnAACYipYSSrj8mUhmONFOgQ', 1),
                  (11, 'Чек-лист_20_мест_утечки_денег.pdf', 'BQACAgIAAxkBAAINYGmre8-AlS08xy1UOnkO7YdHTHnaAALDnAACYipYSe2eC7GNzuI7OgQ', 1),
                  (12, 'V1_krujok_jadnost.mp4', 'BAACAgIAAxkBAAINZGmrfBBX8_cOPhgGpmDvd5po-jB2AALFnAACYipYSa6-I_QmGdJ1OgQ', 1),
                  (13, 'V2_krujok_metod.mp4', 'BAACAgIAAxkBAAINaGmrfEB3Au2Av33muo2CnReV2pMEAALGnAACYipYSf4ro8IEHfliOgQ', 1),
                  (14, 'lesson_01_module_1_video', 'BAACAgIAAxkBAAMMaauS1YdrM9CQBges6JMPF2enQcQAAkSLAAL5A2FJSSX-lPMXW1M6BA', 1),
                  (15, 'lesson_01_module_1_calculator', 'BQACAgIAAxkBAAMQaauS5uXwZsYKXecPnPc5pgJaZrEAAkWLAAL5A2FJTz1izoahqnk6BA', 1),
                  (16, 'lesson_01_module_1_check_list', 'BQACAgIAAxkBAAMUaauS-6cJdEkKdeq8ttACBnp2Y3kAAkaLAAL5A2FJTbBlc0grM5E6BA', 1),
                  (17, 'lesson_02_module_1_video', 'BAACAgIAAxkBAANmaayNjskdVkyIEDWAQd__ZRCzlEIAAl6VAALbgWlJEiTT5NV9iZ86BA', 1),
                  (18, 'lesson_02_module_1_red_flags', 'BQACAgIAAxkBAANqaayNp1WA-mswuh8tveLSvv5nlI0AAmCVAALbgWlJS45CsUV_JaY6BA', 1),
                  (19, 'lesson_03_module_1_video', 'BAACAgIAAxkBAANuaayO_6CmlDweKoFoc8RjMXg30OYAAm-VAALbgWlJ3eltgFUXwM86BA', 1),
                  (20, 'lesson_04_module_1_video', 'BAACAgIAAxkBAANyaaySK82TgeAM5g-Asjd473bI0OAAAq6VAALbgWlJU1IMQd5OOa46BA', 1),
                  (21, 'lesson_07_module_3_video', 'BAACAgIAAxkBAAN2aayWKRMAAcdGuSQdE-Ue0kAfsTHrAALmlQAC24FpSfPpcdxzB2GPOgQ', 1),
                  (22, 'lesson_08_module_3_video', 'BAACAgIAAxkBAAORaa5E3ySpZpuck9wQW2QmzV811XYAApHAAALCOnBJXM3vTSbRPQs6BA', 1),
                  (23, 'lesson_09_module_3_video', 'BAACAgIAAxkBAAN6aaycEq45ZOd8qOVni4ijSlrR_ugAAjyWAALbgWlJjar5S_5ieeA6BA', 1),
                  (24, 'lesson_10_module_4_video', 'BAACAgIAAxkBAAN-aayfyEmwprnz_aumGYNtN9V2rX8AAlSWAALbgWlJdJ57QOfSv3I6BA', 1),
                  (25, 'lesson_11_module_4_video', 'BAACAgIAAxkBAAOCaayiqcVK5j1n-t3PLSYh4Iui2roAAmuWAALbgWlJMZJMs5Xjklc6BA', 1),
                  (26, 'lesson_12_module_4_video', 'BAACAgIAAxkBAAOGaaymLGJz-eXaWnIVR74F_qrKRK4AAoKWAALbgWlJTmcYy58X6_g6BA', 1),
                  (27, 'course_final_checklist', 'BQACAgIAAxkBAAIBPGmuV5FYdM8hmuiQCwtZ6Em4SQPnAAL8kAAC6XpwSfa88MRJ0V4tOgQ', 1),
                  (28, 'otzyv_den2_1.jpg', 'AgACAgIAAxkBAAIHbWmHoqx5mDBqFonY02_KWFWDc9KIAALTC2sbeDghSKgkD42Y93pZAQADAgADeQADOgQ', 1),
                  (29, 'otzyv_den2_2.jpg', 'AgACAgIAAxkBAAIHdWmHosDCcJ1VbiWP0n70XvA2T6KoAALUC2sbeDghSAS1L97x7b5LAQADAgADeQADOgQ', 1),
                  (30, 'otzyv_den2_3.jpg', 'AgACAgIAAxkBAAIHeWmHos_ReY2bFbDSXk7T6hb-QbBKAALVC2sbeDghSDh2jiQagFe1AQADAgADeQADOgQ', 1),
                  (31, 'lesson_05_module_2_video_1', 'BAACAgIAAxkBAAICU2m3ujkJDB7WV_oWESKinZvAD4EAA5mcAAJoL7hJcdCQQDxnigQ6BA', 1),
                  (32, 'lesson_05_module_2_video_2', 'BAACAgIAAxkBAAICV2m3unEGkIOJYOOR2WquSW6jupN5AAKfnAACaC-4SWYMfDW2Kga6OgQ', 1),
                  (33, 'lesson_06_module_2_video_1', 'BAACAgIAAxkBAAICW2m3uxqqUxY0xLBIzNjyWcUQRfV6AALCigACaC_ASVHlWXgby8eeOgQ', 1),
                  (34, 'lesson_06_module_2_video_2', 'BAACAgIAAxkBAAICX2m3uz-ADDQQ1Ws11qHBBpk7xqDYAAI0nwACaC-4SaEDYq0Na-5TOgQ', 1),
                  (35, 'lesson_06_module_2_video_3', 'BAACAgIAAxkBAAICY2m3u2JIXSz2JxtXYbL0kXBHkuJKAALFigACaC_ASZT-wsjT_n5nOgQ', 1),
                  (36, 'C_krujok_tsena_promedleniya.mp4', 'BAACAgIAAxkBAAIOuWm3vr_fvO7CuWZrifeF85k03pInAAKumAACGWvBSVjuwchFCZQAAToE', 1)
           ON CONFLICT (id) DO NOTHING;

           SELECT setval('media_id_seq', COALESCE((SELECT MAX(id) FROM media),1));
           """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
           DELETE FROM media WHERE id <= 36;

           SELECT setval('media_id_seq', (SELECT MAX(id) FROM media));
           """

MODELS_STATE = (
    "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"
)
