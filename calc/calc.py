"""
栄養ランキング計算のためのスクリプトファイル

ランキングアルゴリズム：ある食材の栄養素ランキング
各栄養素について多い順に並べる. 多い順に順位を割り当てる.
例）　キャベツ：　ビタミンA 10位　ビタミンB 20位 ビタミンC 30位タイ
このとき, ビタミンCが一番少ないと考え, ビタミンCを多く含む食材を推薦する.
推薦時には, あらかじめ, ある栄養素を多く含む食材がリストアップされているので, それを利用する.
計算済みのランキングを利用して, 足りてない栄養素のランキング上位を推薦という形でもよい.

"""
from answers import ANSWER, VITAMINS, FOODS
from pprint import pprint

def ranknize():
  """
  ランキング数値に変換するだけ
  """

  food_ids = FOODS.keys()
  ranking = {}

  for vitamin in VITAMINS:
    
    result = []
    for food_id in food_ids:
      value = float(FOODS[food_id][vitamin])
      result.append([value, food_id])
    
    result.sort(reverse = True)

    previous = None
    score = 0
    for s in result:
      value = s[0]
      food_id = s[1]
      if not s[0] == previous:
        score += 1
      
      if not food_id in ranking.keys():
        ranking[food_id] = {}
      
      ranking[food_id][vitamin] = score
      
      previous = s[0]
  
  pprint(ranking)
  return ranking

if __name__ == "__main__":
    ranknize()