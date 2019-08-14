# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

"質問の回答をbool型で保存"
ans_level = 0
"セッション（会話）の種類を定数で定義"
"何もない最初の状態"
_NORMAL_ = 0
"診断モード"
_DIAGNOSIS_ = 1
"自由会話モード"
_FREE_ = 0

"ルーチンの種類を示すフラグ"
"最初はノーマル"
sessionFlag =_NORMAL_

class CounselingIntentHandler(AbstractRequestHandler):
    """
    診断インテントが呼ばれた時のハンドラ
    ex: 「アレクサ、＜＞で診断して」
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CounselingIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_atr = handler_input.attributes_manager.session_attributes
        if not 'level' in session_atr.keys():
            session_atr['level'] = 0
        print(handler_input)
        print(session_atr)
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
            CatchAllExceptionHandler.handle(handler_input)
            return
        
        level = session_atr['level']
        if level == 0:
            # 風邪に対する解答
            SessionEndedRequestHandler.handle(handler_input)
        elif level == 1:
            # 食欲増進
            SessionEndedRequestHandler.handle(handler_input)
        else:
            # もう一度いう
            CounselingIntentHandler.handle(handler_input)

class NoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_atr = handler_input.attributes_manager.session_attributes
        if not 'level' in session_atr.keys():
            # 何も診断していないので不正なリクエストとして処理
            CatchAllExceptionHandler.handle(handler_input)
            return
        
        session_atr['level'] += 1
        
        return CounselingIntentHandler.handle(self, handler_input)

class HelpIntentHandler(AbstractRequestHandler):
    """
    Alexa組み込みインテントHelpインテントが呼ばれた時のハンドラ
    ex: 「アレクサ、＜＞でヘルプ」
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """
    Alexa組み込みインテントのキャンセルインテントまたはストップインテントが呼ばれた時のハンドラ
    ex: 「アレクサ、＜＞をやめる」
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "ありがとうございました．お大事に!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class SessionEndedRequestHandler(AbstractRequestHandler):
    """
    セッションを終了する際に呼ばれるハンドラ
    クリーンアップする類の処理を行う
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """
    インテントが呼び出されたかを確認できるデバッグ用のハンドラ

    The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class CatchAllExceptionHandler(AbstractExceptionHandler):
    """
    エラーが発生した場合に呼び出されるハンドラ

    Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

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
sb.add_request_handler(CounselingIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_request_handler(IntentReflectorHandler())
# error handler
sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()