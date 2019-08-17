# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.

import random

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

from handlers import HelpIntentHandler, CancelOrStopIntentHandler, SessionEndedRequestHandler, IntentReflectorHandler, CatchAllExceptionHandler, FallbackIntentHandler
from answers import ANSWER

class AnsweringIntentHandler(AbstractRequestHandler):
    """
    ユーザーが症状を回答したときに呼び出されるハンドラ
    ex: 「頭が痛い」
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name("AnsweringIntent")(handler_input)

    def handle(self, handler_input, answer_category=None):
        # type: (HandlerInput) -> Response

        # TODO スロット値を見てasnwerを判断する
        slot = ask_utils.get_slot(handler_input, "symptom")

        if slot:
            # TODO
            """
            適当な単語をいれた時にstatus = ER_SUCCESS_NO_MATCHになるのをチェックしてfallbackする
            """

            slot_id = slot.resolutions.resolutions_per_authority[0].values[0].value.id
            answer_category = slot_id

        if not answer_category:
            # TODO
            answer_category = 'G'
        
        # セッション変数に答えをいれておく
        handler_input.attributes_manager.session_attributes['answer_category'] = answer_category
        
        print("疲労の種類は%sです" % answer_category)

        food = random.choice(ANSWER[answer_category])
        # 回答済みの答えもいれておく
        handler_input.attributes_manager.session_attributes['answered_foods'] = [food]
        speak_output = 'あなたにオススメの食べ物は%sです。他の候補が知りたいときは、他には、と聞いてください' % food

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class AdditionalIntentHandler(AbstractRequestHandler):
    """
    ユーザーがそのほかの食べ物を要求した場合
    ex: 「他には？」
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name("AdditionalIntent")(handler_input)

    def handle(self, handler_input, answer=None):
        # type: (HandlerInput) -> Response

        answer_category = handler_input.attributes_manager.session_attributes['answer_category']
        answered_foods = handler_input.attributes_manager.session_attributes['answered_foods']

        if not answer_category:
            return CounselingIntentHandler.handle(self, handler_input)

        speak_output = 'すみません。ほかの候補がもうありません。'

        answers = ANSWER[answer_category]

        if len(answered_foods) != len(answers):
            answer = random.choice(answers)

            i = 0
            while (answer in answered_foods) and i < 10:
                answer = random.choice(answers)
                i += 1
            
            handler_input.attributes_manager.session_attributes['answered_foods'].append(answer)

            speak_output = 'あなたにオススメの食べ物は%sです。他の候補が知りたいときは、他には、と聞いてください' % answer

            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(speak_output)
                    .response
            )
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class CounselingIntentHandler(AbstractRequestHandler):
    """
    診断インテントが呼ばれた時のハンドラ
    ex: 「診断」
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CounselingIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_atr = handler_input.attributes_manager.session_attributes

        """ 
        lambda側で変数定義するとコンテナ内部で使い回されるので、色々問題が生じる
        セッション中の変数はsession_attributessが保持する
        """

        if not 'level' in session_atr.keys():
            handler_input.attributes_manager.session_attributes['level'] = 0

        level = session_atr['level']
        speak_output = ""

        if level == 0:
            speak_output = "風邪っぽいですか"
        elif level == 1:
            speak_output = "食欲はありますか"
        else:
            speak_output = "症状を教えてください"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class LaunchRequestHandler(AbstractRequestHandler):
    """
    起動時に呼ばれるハンドラ
    ex: 「アレクサ、＜＞を開いて」
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = 'こんにちは．診断と言っていただければ，あなたにオススメの食べ物を考えてみます．'

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class YesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_atr = handler_input.attributes_manager.session_attributes
        if not 'level' in session_atr.keys():
            # 何も診断していないので不正なリクエストとして処理
            print("セッション変数が存在していません. YesIntent")
            FallbackIntentHandler.handle(self, handler_input)
            return
        
        level = session_atr['level']
        if level == 0:
            # 風邪に対する解答
            return AnsweringIntentHandler.handle(self, handler_input, 'E')
        if level == 1:
            # 食欲不振
            return AnsweringIntentHandler.handle(self, handler_input, 'B')
        else:
            # もう一度いう
            return CounselingIntentHandler.handle(self, handler_input)

class NoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_atr = handler_input.attributes_manager.session_attributes
        if not 'level' in session_atr.keys():
            # 何も診断していないので不正なリクエストとして処理
            print("セッション変数が存在していません. NoIntent")
            FallbackIntentHandler.handle(self, handler_input)
            return
        
        session_atr['level'] += 1
        
        return CounselingIntentHandler.handle(self, handler_input)

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CounselingIntentHandler())
sb.add_request_handler(AnsweringIntentHandler())
sb.add_request_handler(AdditionalIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_request_handler(IntentReflectorHandler())
# error handler
sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()