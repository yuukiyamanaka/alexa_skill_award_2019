import json

class BaseSpeech:
    """シンプルな、発話するレスポンスのベース"""

    def __init__(self, speech_text, should_end_session, session_attributes=None):
        """初期化処理

        引数:
            speech_text: Alexaに喋らせたいテキスト
            should_end_session: このやり取りでスキルを終了させる場合はTrue, 続けるならFalse
            session_attributes: 引き継ぎたいデータが入った辞書
        """
        if session_attributes is None:
            session_attributes = {}

        # 最終的に返却するレスポンス内容。これを各メソッドで上書き・修正していく
        self._response = {
            'version': '1.0',
            'sessionAttributes': session_attributes,
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': speech_text
                },
                'shouldEndSession': should_end_session,
            },
        }

        # 取り出しやすいよう、インスタンスの属性に
        self.speech_text = speech_text
        self.should_end_session = should_end_session
        self.session_attributes = session_attributes

    def simple_card(self, title, text=None):
        """シンプルなカードを追加する"""
        if text is None:
            text = self.speech_text
        card = {
            'type': 'Simple',
            'title': title,
            'content': text,
        }
        self._response['response']['card'] = card
        return self

    def build(self):
        """最後にこのメソッドを呼んでください..."""
        return self._response


class OneSpeech(BaseSpeech):
    """1度だけ発話する(ユーザーの返事は待たず、スキル終了)"""

    def __init__(self, speech_text, session_attributes=None):
        super().__init__(speech_text, True, session_attributes)


class QuestionSpeech(BaseSpeech):
    """発話し、ユーザーの返事を待つ"""

    def __init__(self, speech_text, session_attributes=None):
        super().__init__(speech_text, False, session_attributes)

    def reprompt(self, text):
        """リプロンプトを追加する"""
        reprompt = {
            'outputSpeech': {
                'type': 'PlainText',
                'text': text
            }
        }
        self._response['response']['reprompt'] = reprompt
        return self


def explain_history():
    """ハローと言っておわり"""
    return OneSpeech('ようこそ．あなたの体調を教えてください．風邪っぽいですか？').build()


def welcome():
    """ようこそと言って、ユーザーの返事を待つ"""
    return QuestionSpeech('ようこそ!').reprompt('よく聞こえませんでした').build()


def bye():
    """グッバーイといって終わる"""
    return OneSpeech('グッバーイ').simple_card('遊んでくれてありがとう!').build()


def lambda_handler(event, context):
    """最初に呼び出される関数"""
    # リクエストの種類を取得
    request = event['request']
    request_type = request['type']

    # LaunchRequestは、特定のインテントを提供することなく、ユーザーがスキルを呼び出すときに送信される...
    # つまり、「アレクサ、ハローワールドを開いて」のようなメッセージ
    # 「アレクサ、ハローワールドで挨拶しろ」と言うとこれはインテントを含むので、IntentRequestになる
    if request_type == 'LaunchRequest':
        return welcome()

    # 何らかのインテントだった場合
    elif request_type == 'IntentRequest':
        intent_name = request['intent']['name']

        # 「会社の歴史を教えて」「聞かせて」等で呼ばれる。サンプル発話に書いた部分
        if intent_name == 'ChoseNutIntent':
            return explain_history()

        # 「ヘルプ」「どうすればいいの」「使い方を教えて」で呼ばれる、組み込みインテント
        elif intent_name == 'AMAZON.HelpIntent':
            return welcome()

        # 「キャンセル」「取り消し」「やっぱりやめる」等で呼び出される。組み込みのインテント
        elif intent_name == 'AMAZON.CancelIntent' or intent_name == 'AMAZON.StopIntent':
            return bye()
