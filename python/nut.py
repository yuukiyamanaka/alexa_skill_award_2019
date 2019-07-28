import json
"120行目付近にTODO　診断アルゴリズム挿入があります．"

"質問の回答をbool型で保存"
anslist = []
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

'最初の質問'
welcom_mes = 'こんにちは．診断と言っていただければ，あなたにオススメの食べ物を考えてみます．'
"診断でバグ，例外が怒った時のメッセージ"
miss_mes = 'すみません．診断に失敗しました'
"中断，キャンセルと言われた時のメッセージ"
bye_mes = "ありがとうございました．お大事に"

"Yes or Noの質問"
question1 = '風邪っぽいですか'
question2 = '体の疲れ，筋肉痛やだるさはありますか'
question3 = '食欲はありますか'


"今のルーチンはどんな種類の会話なのか"
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



def diagnosis():
    """ハローと言っておわり"""
    global sessionFlag
    if len(anslist) == 0 :
        return QuestionSpeech(question1).reprompt('よく聞こえませんでした').build()
    elif len(anslist) == 1 :
        return QuestionSpeech(question2).reprompt('よく聞こえませんでした').build()
    elif len(anslist) == 2 :
        return QuestionSpeech(question3).reprompt('よく聞こえませんでした').build()
    elif len(anslist) == 3 :
        
        "resultに演算結果を入れてください．今は何を聞いてもカレーと答えます．このコードを書いたときにカレーが食べたかったからです．"
        result = 'カレー'
        "TODO******診断アルゴリズム*******"
        
        "*********************************"
        "診断結果配列の初期化"
        anslist.clear()
        "セッションの状態を初期の状態に"
        sessionFlag = _NORMAL_
        return OneSpeech('診断ができました．'+result +'がオススメです').simple_card('遊んでくれてありがとう!').build()
    return QuestionSpeech(miss_mes).reprompt('よく聞こえませんでした').build()



def yescount():
    "anslistにtrueを追加することではいを回答したことを設定"
    anslist.append(True)
    return diagnosis()

def nocount():
    "anslistにfalse を追加することでいいえと回答したことを設定"
    anslist.append(False)
    return diagnosis()

def welcome():
    """ようこそと言って、ユーザーの返事を待つ"""
    return QuestionSpeech(welcom_mes).reprompt('よく聞こえませんでした').build()

def repeat():
    """ようこそと言って、ユーザーの返事を待つ"""
    return QuestionSpeech('ごめんなさい．もう一度言ってください．').reprompt('よく聞こえませんでした').build()

def bye():
    """グッバーイといって終わる"""
    return OneSpeech(bye_mes).simple_card('遊んでくれてありがとう!').build()

def lambda_handler(event, context):
    """最初に呼び出される関数"""
    # リクエストの種類を取得
    request = event['request']
    request_type = request['type']
    "グローバル変数のフラグを使うことを宣言"
    global sessionFlag
    # LaunchRequestは、特定のインテントを提供することなく、ユーザーがスキルを呼び出すときに送信される...
    # つまり、「アレクサ、ハローワールドを開いて」のようなメッセージ
    # 「アレクサ、ハローワールドで挨拶しろ」と言うとこれはインテントを含むので、IntentRequestになる
    if request_type == 'LaunchRequest':
        return welcome()

    # 何らかのインテントだった場合
    elif request_type == 'IntentRequest':
        intent_name = request['intent']['name']
        
        # 「診断」「聞かせて」等で呼ばれる。サンプル発話に書いた部分
        if intent_name == 'ChoseNutIntent':
            
            sessionFlag = _DIAGNOSIS_
            return diagnosis()
        elif (intent_name == 'YesIntent') and sessionFlag == _DIAGNOSIS_:
            return yescount()
elif intent_name == 'NoIntent' and sessionFlag == _DIAGNOSIS_:
    return nocount()
        # 「ヘルプ」「どうすればいいの」「使い方を教えて」で呼ばれる、組み込みインテント
        elif intent_name == 'AMAZON.HelpIntent':
            return welcome()

    # 「キャンセル」「取り消し」「やっぱりやめる」等で呼び出される。組み込みのインテント
    elif intent_name == 'AMAZON.CancelIntent' or intent_name == 'AMAZON.StopIntent':
        return bye()

return repeat()
