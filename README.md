## Shop Detail API Contract Testing

使用 Python、requests、pytest 與 Pydantic，對 momo 店鋪明細 API 進行 live API contract testing。

## 環境需求

- Python 3.10+
- 可連線至測試 API 的網路環境

## 安裝方式

Windows PowerShell：

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

macOS / Linux：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 執行測試

```bash
python -m pytest -v
```

## 專案結構

```text
API_contract_tests/
├── momo_api.py
├── schemas.py
├── requirements.txt
├── pytest.ini
├── README.md
└── tests/
    └── test_shop_detail_api.py
```

## 測試範圍

依題目要求與實際 API response，測試以下內容：

- 成功案例 HTTP status code 為 200。
- 使用 Pydantic schema 驗證必要欄位存在且型別正確。
- `shopName` 不可為空。
- response 的 `entpCode` 不可為空，且必須與 request 的 `TP0007070` 一致。
- 空的 `entpCode`：實測為 HTTP 200、`resultCode: "-1"`、`data: null`。
- 不存在的 `TP9999999`：實測為 HTTP 200、`resultCode: "EC0014"`、`data: null`。

## Contract 設計

Schema 只定義這次測試真正需要的核心欄位：

- `success`
- `resultCode`
- `resultMessage`
- `data`
- `data.shopDetailData`
- `data.shopDetailData.shopHeader`
- `shopHeader.shopName`
- `shopHeader.momoAsk`
- `momoAsk.entpCode`

這些欄位若缺少或型別改變，可能影響目前的 API 判讀與店鋪識別，因此列入 contract。

Schema 使用 `extra="allow"`。API 如果只是新增非核心欄位，測試不會因此失敗；但上述核心欄位缺少或型別不正確時，Pydantic 驗證仍會失敗。

## 實測注意事項

- Python requests 使用預設 `User-Agent: python-requests/...` 時，此 API 會回 HTTP 406。
- 改用 `User-Agent: curl/8.4.0` 後，可正常取得 HTTP 200 與 JSON response。
- 題目提供的 `rc` header 會保留在 request 中。
- 成功案例使用 session scope fixture，只呼叫一次 API，避免每個 test 重複呼叫相同資料。
- Schema 驗證集中在單一 contract test；其他測試各自驗證 business data，避免同一個 schema 問題造成多個重複失敗。
- 負面案例使用 `pytest.mark.parametrize`，以相同測試邏輯驗證兩種不同輸入。
