from src.core.logging_config import setup_logging

logger = setup_logging(__name__, service="webhook_yookassa")

from fastapi import Request
from fastapi import HTTPException
from fastapi import FastAPI

app = FastAPI()


@app.post("/webhooks/yookassa")
async def yookassa_webhook(request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    logger.info(f"YooKassa webhook received: {data}")

    event = data.get("event")
    payment = data.get("object", {})

    if not payment:
        raise HTTPException(status_code=400, detail="No payment object")

    payment_id = payment.get("id")
    status = payment.get("status")
    metadata = payment.get("metadata", {})

    # 🔹 Успешная оплата
    if event == "payment.succeeded":
        user_id = metadata.get("user_id")
        order_id = metadata.get("order_id")

        logger.info(f"Payment succeeded: {payment_id}")

        # TODO: обновить БД
        # await PaymentService.mark_as_paid(order_id)

    # 🔹 Отмена платежа
    elif event == "payment.canceled":
        logger.warning(f"Payment canceled: {payment_id}")

    return {"status": "ok"}