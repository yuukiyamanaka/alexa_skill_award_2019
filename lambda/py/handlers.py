import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
        # 解答済みかどうかでヘルプの内容を変更する
        session_atr = handler_input.attributes_manager.session_attributes

        speak_output = "食材の名前を一つ言ってみてください。その食材に足りないビタミンと、そのビタミンを多く含む食材を考えてみます。"
        if 'answer_vitamin' in session_atr.keys():
            speak_output ="すでに組み合わせを考えています。オススメの食べ物を知りたい場合は、ほかには、と聞いてみてください。"

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
        speak_output = "ありがとうございました。"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

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
        return ask_utils.is_intent_name("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = intent_name + "が呼び出されました"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class SessionEndedRequestHandler(AbstractRequestHandler):
    """
    セッションを終了する際に呼ばれるハンドラ
    クリーンアップする類の処理を行う
    ex: ユーザーがなにも返してこない時
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.
        # return handler_input.response_builder.response
        return CancelOrStopIntentHandler.handle(self, handler_input)
        
class FallbackIntentHandler(AbstractRequestHandler):
    """
    ユーザーの発話がどのインテントにも該当しない場合
    ex: 「今日の天気は？」
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_atr = handler_input.attributes_manager.session_attributes

        speak_output = "その言葉にはお答えできませんが、食材を教えてもらえれば、オススメの食材の組み合わせを考えてみます。"
        if 'answer_vitamin' in session_atr.keys():
            speak_output ="ほかには、と聞いてもらえれば、ほかのおすすめの食材を考えてみます。"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
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

        speak_output = "すみません。何かの問題が発生しました。最初からやり直してください。"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
