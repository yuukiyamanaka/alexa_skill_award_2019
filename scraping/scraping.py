# -*- coding: utf-8 -*-

import requests
import ssl
import urllib3
import lxml
from lxml import html
from urllib import request
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

xpath_vitamin_d = "//*[@id='nut']/tbody/tr[30]/td[2]"
xpath_vitamin_k = "//*[@id='nut']/tbody/tr[35]/td[2]"
xpath_vitamin_b1 = "//*[@id='nut']/tbody/tr[36]/td[2]"
xpath_vitamin_b2 = "//*[@id='nut']/tbody/tr[37]/td[2]"
xpath_vitamin_ne = "//*[@id='nut']/tbody/tr[39]/td[2]"  # ナイアシン当量
xpath_vitamin_b6 = "//*[@id='nut']/tbody/tr[40]/td[2]"
xpath_vitamin_b12 = "//*[@id='nut']/tbody/tr[41]/td[2]"
xpath_vitamin_fa = "//*[@id='nut']/tbody/tr[42]/td[2]"  # 葉酸
xpath_vitamin_pa = "//*[@id='nut']/tbody/tr[43]/td[2]"  # パントテン酸
xpath_vitamin_biotin = "//*[@id='nut']/tbody/tr[44]/td[2]"
xpath_vitamin_c = "//*[@id='nut']/tbody/tr[45]/td[2]"

vitamin_list = ["ビタミンD", "ビタミンK", "ビタミンB1", "ビタミンB2", "ナイアシン当量",
                "ビタミンB6", "ビタミンB12", "葉酸", "パントテン酸", "ビオチン", "ビタミンC"]

xpath = [xpath_vitamin_d, xpath_vitamin_k, xpath_vitamin_b1, xpath_vitamin_b2, xpath_vitamin_ne,
         xpath_vitamin_b6, xpath_vitamin_b12, xpath_vitamin_fa, xpath_vitamin_pa, xpath_vitamin_biotin, xpath_vitamin_c]
URL = ["https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=11_11172_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=11_11004_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=11_11237_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=12_12004_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10345_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10199_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10252_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10234_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10192_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10144_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10411_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10407_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10042_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10154_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10246_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10086_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10241_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10003_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=13_13003_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10067_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=4_04052_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=7_07040_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=7_07148_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=7_07155_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=17_17051_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=2_02022_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=2_02017_7&MODE=1",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=6_06182_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=6_06214_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=6_06061_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=6_06312_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=8_08039_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=8_08016_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=6_06367_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=6_06015_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=7_07077_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=7_07006_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=6_06245_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=7_07116_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=6_06226_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=6_06191_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=6_06153_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=8_08020_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=8_08025_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=6_06065_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=6_06007_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=6_06263_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=6_06128_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=6_06084_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=6_06207_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=5_05001_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=9_09039_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=7_07107_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=9_09004_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=13_13040_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=5_05034_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=6_06267_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10297_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10365_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10285_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10141_7",
       "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=6_06071_7"]

foods_list = ["豚肉",
              "牛肉",
              "鶏肉",
              "卵",
              "いか",
              "白身魚（たら）",
              "赤身魚（マグロ）",
              "ヒラメ",
              "たい",
              "サーモン",
              "ハマチ",
              "秋刀魚",
              "イワシ",
              "さば",
              "ホッケ",
              "カツヲ",
              "ぶり",
              "アジ",
              "牛乳",
              "うなぎ",
              "豆乳",
              "オレンジ",
              "りんご",
              "レモン",
              "カレー（ルー）",
              "長芋",
              "じゃがいも",
              "トマト",
              "人参",
              "キャベツ",
              "レタス",
              "しいたけ",
              "ふなしめじ",
              "大根",
              "枝豆",
              "スイカ",
              "アボカド",
              "ピーマン",
              "ぶどう",
              "ねぎ",
              "なす",
              "玉ねぎ",
              "なめこ",
              "エリンギ",
              "きゅうり",
              "アスパラガス",
              "ブロッコリー",
              "かいわれ大根",
              "ごぼう",
              "にら",
              "アーモンド",
              "わかめ",
              "バナナ",
              "のり",
              "チーズ",
              "ピーナッツ",
              "ほうれんそう",
              "しじみ",
              "うに",
              "あわび",
              "すじこ",
              "にんにく"]

data = {}
vitamin = {}

for i in range(len(foods_list)):
    r = requests.get(URL[i], verify=False)
    html = r.text
    root = lxml.html.fromstring(html)

    for j in range(len(xpath)):
        titleH1 = root.xpath(xpath[j])
        vitamin[vitamin_list[j]] = titleH1[0].text
    print('"'+str(foods_list[i])+'":'+str(vitamin)+",")  # とりあえず表示まで
