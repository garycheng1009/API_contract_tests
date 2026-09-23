"""momo 店鋪明細 API 的簡單呼叫工具。"""

import json
from typing import Any

import requests


API_URL = "https://3pf.momo.com.tw/shop/app/info/detail/query/v1"
VALID_ENTP_CODE = "TP0007070"

# requests 預設 User-Agent 會被此 API 回 406，改用 curl User-Agent 可正常取得 JSON。
DEFAULT_HEADERS = {
    "content-type": "application/json",
    "rc": "",
    "User-Agent": "curl/8.4.0",
}


def query_shop_detail(entp_code: str) -> tuple[int, dict[str, Any]]:
    """送出店鋪代碼並回傳 HTTP 狀態碼與 JSON body。"""
    payload = {
        "host": "momoshop",
        "data": {
            "entpCode": entp_code,
        },
    }

    response = requests.post(
        API_URL,
        headers=DEFAULT_HEADERS,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        timeout=20,
    )

    # API 未宣告 charset，直接用 UTF-8 解碼 response content。
    body = json.loads(response.content.decode("utf-8"))
    return response.status_code, body
