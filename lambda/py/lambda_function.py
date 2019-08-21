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
from ask_sdk_model.slu.entityresolution.status_code import StatusCode

from handlers import HelpIntentHandler, CancelOrStopIntentHandler, SessionEndedRequestHandler, IntentReflectorHandler, CatchAllExceptionHandler, FallbackIntentHandler
from answers import ANSWER, VITAMIN, RANKING

class AnsweringIntentHandler(AbstractRequestHandler):
    """
    ユーザーが食べ物を言ったときに呼び出されるハンドラ
    ex: 「きゃべつ」
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name("AnsweringIntent")(handler_input)

    def handle(self, handler_input, query_food_id=None):
        # type: (HandlerInput) -> Response

        slot = ask_utils.get_slot(handler_input, "food")

        if slot:
            # スロット値がマッチしてないとき
            if slot.resolutions.resolutions_per_authority[0].status.code != StatusCode.ER_SUCCESS_MATCH:
                print("マッチしませんでした")
                return FallbackIntentHandler.handle(self, handler_input)

            query_food_id = slot.resolutions.resolutions_per_authority[0].values[0].value.id
            query_food_name = slot.resolutions.resolutions_per_authority[0].values[0].value.name

        if not query_food_id:
            # エラーハンドリング
            print("カテゴリが見つかりませんでした")
            return CatchAllExceptionHandler.handle(self, handler_input)
        
        # セッション変数に答えをいれておく
        handler_input.attributes_manager.session_attributes['query_food_id'] = query_food_id
        
        print("クエリの食べ物は%sです" % query_food_id)

        ranking = RANKING[str(query_food_id)]

        vitamin = sorted(ranking.items(), key=lambda x: x[1])[-1][0]
        handler_input.attributes_manager.session_attributes['answer_vitamin'] = vitamin
        print("足りないビタミンは%s" % vitamin)

        food = random.choice(ANSWER[vitamin])
        # 回答済みの答えもいれておく
        handler_input.attributes_manager.session_attributes['answered_foods'] = [food]
        print("おすすめの食材は%s" % food)

        speak_output = vitamin + "を追加で摂取するとよいかもしれません。オススメの食材は" + food + "です。ほかの候補が知りたいときは、ほかには、と聞いてください"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class AdditionalIntentHandler(AbstractRequestHandler):
    """
    ユーザーがそのほかの食べ物を要求した場合
    ex: 「ほかには？」
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name("AdditionalIntent")(handler_input)

    def handle(self, handler_input, answer=None):
        # type: (HandlerInput) -> Response

        vitamin = handler_input.attributes_manager.session_attributes['answer_vitamin']
        answered_foods = handler_input.attributes_manager.session_attributes['answered_foods']

        # vitamin or answerd_foodがない時
        if not vitamin or not answered_foods:
            speak_output = 'まだ組み合わせる食材を聞いていませんね。組み合わせたい食材を言ってもらえれば、おすすめの組み合わせを考えてみます。'
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    .ask(speak_output)
                    .response
            )

        speak_output = 'すみません。ほかの候補がもうありません。'

        answers = ANSWER[vitamin]

        if len(answered_foods) != len(answers):
            answer = random.choice(answers)

            i = 0
            while (answer in answered_foods) and i < 20:
                answer = random.choice(answers)
                i += 1
            
            handler_input.attributes_manager.session_attributes['answered_foods'].append(answer)

            speak_output = '%sはどうでしょう。さらに知りたいときは、ほかには、と聞いてください' % answer

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
        speak_output = 'こんにちは。食材の名前を言ってもらえれば、おすすめの組み合わせを考えてみます。'

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(AnsweringIntentHandler())
sb.add_request_handler(AdditionalIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(FallbackIntentHandler())
# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
# sb.add_request_handler(IntentReflectorHandler())
# error handler
sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()