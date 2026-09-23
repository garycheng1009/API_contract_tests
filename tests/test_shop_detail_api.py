"""momo 店鋪明細 API 的 live pytest 測試。"""

import pytest

from momo_api import VALID_ENTP_CODE, query_shop_detail
from schemas import ShopDetailResponse


@pytest.fixture(scope="session")
def valid_response() -> tuple[int, dict]:
    """成功案例只呼叫一次 API，供多個測試共用。"""
    return query_shop_detail(VALID_ENTP_CODE)


def test_success_status_code_is_200(valid_response: tuple[int, dict]) -> None:
    """成功案例應回 HTTP 200。"""
    status_code, _ = valid_response

    assert status_code == 200


def test_success_response_matches_schema(valid_response: tuple[int, dict]) -> None:
    """必要欄位應存在，且型別符合 schema。"""
    _, body = valid_response

    parsed = ShopDetailResponse.model_validate(body)

    assert parsed.success is True
    assert parsed.resultCode == "200"
    assert parsed.data is not None


def test_shop_name_is_not_empty(valid_response: tuple[int, dict]) -> None:
    """店鋪名稱不可是空字串。"""
    _, body = valid_response
    shop_name = body["data"]["shopDetailData"]["shopHeader"]["shopName"]

    assert shop_name.strip() != ""


def test_response_entp_code_matches_request(valid_response: tuple[int, dict]) -> None:
    """回傳的 entpCode 應與請求一致，且不可為空。"""
    _, body = valid_response
    entp_code = body["data"]["shopDetailData"]["shopHeader"]["momoAsk"]["entpCode"]

    assert entp_code != ""
    assert entp_code == VALID_ENTP_CODE


@pytest.mark.parametrize(
    ("entp_code", "expected_result_code"),
    [
        ("", "-1"),
        ("TP9999999", "EC0014"),
    ],
)
def test_negative_entp_code_cases(
    entp_code: str,
    expected_result_code: str,
) -> None:
    """驗證空值與不存在店鋪代碼的實際錯誤回應。"""
    status_code, body = query_shop_detail(entp_code)

    assert status_code == 200
    assert body["resultCode"] == expected_result_code
    assert body["resultMessage"].strip() != ""
    assert body["data"] is None
