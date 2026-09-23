"""依實際 momo API response 建立的 Pydantic schema。"""

from pydantic import BaseModel, ConfigDict, StrictBool, StrictStr


class FlexibleModel(BaseModel):
    """允許 API 新增未定義欄位，避免非核心欄位變動造成測試失敗。"""

    model_config = ConfigDict(extra="allow")


class MomoAsk(FlexibleModel):
    entpCode: StrictStr


class ShopHeader(FlexibleModel):
    shopName: StrictStr
    momoAsk: MomoAsk


class ShopDetailData(FlexibleModel):
    shopHeader: ShopHeader


class ResponseData(FlexibleModel):
    shopDetailData: ShopDetailData


class ShopDetailResponse(FlexibleModel):
    """只定義這次 contract test 真正需要的核心欄位。"""

    success: StrictBool
    resultCode: StrictStr
    resultMessage: StrictStr
    data: ResponseData | None
