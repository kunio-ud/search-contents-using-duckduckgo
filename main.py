from duckduckgo_search.exceptions import DuckDuckGoSearchException
from duckduckgo_search import DDGS
import openai
import os
from dotenv import load_dotenv
import json
import time
from datetime import datetime

# 現在の日時を取得
now = datetime.now()

# 日付を指定のフォーマットで文字列に変換
date_str = now.strftime('%Y%m%d_%H%M%S')

# ファイル名を作成
filename = f'videos_{date_str}.md'

# .env を読み込む
load_dotenv()

# 環境変数からAPIキーを取得
API_KEY = os.getenv("OPENAI_API_KEY", None)
if not API_KEY:
    raise ValueError("OPENAI_API_KEYが設定されていません！.envファイルを確認してください。")

openai.api_key = API_KEY

PROMPT = os.getenv("PROMPT", None)


def summarize_text(text:str):
    """OpenAI APIを使って検索結果を要約"""
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # より高速でコストを抑えたモデル
        messages=[
            {
                "role": "system",
                "content": "あなたは優れたWebブロガーです。どんな商材も売ることができるトップブロガーです。"
            },
            {
                "role": "user",
                "content": f'''
本日、検索した結果は、これです。
{text}
これをインプットとし、
{PROMPT}
                '''
            }
        ],
        max_tokens=3000,  # 必要に応じて調整
    )
    return response["choices"][0]["message"]["content"]




def search_videos():
    query = "Python 初心者 最新トレンド"

    with DDGS() as ddgs:
        results = list(ddgs.text(
            keywords=query,       # 検索ワード
            region='jp-jp',       # リージョン 日本は"jp-jp",指定なしの場合は"wt-wt"
            safesearch='on',     # セーフサーチOFF->"off",ON->"on",標準->"moderate"
            timelimit="d",        # 期間指定 指定なし->None,過去1日->"d",過去1週間->"w", 過去1か月->"m",過去1年->"y"
            max_results=10         # 取得件数
        ))
        return results



def save_markdown(content, filename="tiktok_cat_videos.md"):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)


if __name__ == "__main__":
    search_videos_results = search_videos()
    json_string = json.dumps(search_videos_results)
    summary = summarize_text(json_string)
    print("要約結果:", summary)
    save_markdown( json_string + "\n" + summary, filename )

