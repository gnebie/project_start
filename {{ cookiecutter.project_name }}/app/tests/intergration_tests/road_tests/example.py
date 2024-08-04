# test_routes/test_payment_routes.py

from app.api.schemas.schemas import UserInfo
from app.api.models.billing import BillingOperation
from app.api.enums.enums import OperationType, PaymentStatus
import pytest
from unittest.mock import Mock, patch
from unittest.mock import AsyncMock
from fastapi import status
from app.api.schemas import PaymentIntentRequest
from uuid import UUID, uuid4
from fastapi import Request, HTTPException
from app.config import settings
import stripe
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, Field
import logging
from app.api.services import billing_service
from starlette.testclient import TestClient
from icecream import ic

logger = logging.getLogger(__name__)


@pytest.fixture
def mock_request():
    return Request(scope={"type": "http"})


def dict_to_mock(data):
    mock_obj = Mock()
    for key, value in data.items():
        setattr(mock_obj, key, value)
    return mock_obj


@pytest.mark.asyncio
async def test_session_fixture(session):
    assert session is not None
    assert isinstance(session, AsyncSession)
    try:
        new_operation = BillingOperation(
            user_uuid=uuid4(), operation_type=OperationType.PURCHASE, amount=100.0, payment_intent_id="pi_1F6gB8EZPqZZJppJmR1OsJv5", currency="USD", discounts=5.0, payment_status=PaymentStatus.SUCCEEDED, libelle="Test Purchase"
        )
    except Exception as e:
        ic(e)
        logger.error("Error adding middlewares", exc_info=True)
        raise e

    session.add(new_operation)
    await session.commit()

    result = await session.execute(select(BillingOperation).where(BillingOperation.payment_intent_id == "pi_1F6gB8EZPqZZJppJmR1OsJv5"))
    operation = result.scalar_one()

    assert operation is not None
    assert operation.payment_intent_id == "pi_1F6gB8EZPqZZJppJmR1OsJv5"

    # Supprimer l'opération de facturation de la base de données
    await session.delete(operation)
    await session.commit()

    # Vérifier que l'opération de facturation a été supprimée
    result = await session.execute(select(BillingOperation).where(BillingOperation.payment_intent_id == "pi_1F6gB8EZPqZZJppJmR1OsJv5"))
    operation = result.scalar_one_or_none()
    assert operation is None

    print("session test Success")


@pytest.mark.asyncio
async def post_endpoint_tester(
    test_app, session, permission_list: list[str], request_data: dict, response_data: dict, service_patch: str, route: str, response_status_code: int = status.HTTP_200_OK, auth_token: str = "valid_token", verb: str = "post"
) -> dict:
    """
    Test a POST endpoint with the given parameters.

    Args:
        test_app: The FastAPI test client.
        session: The database session fixture.
        permission_list (list[str]): List of permissions to mock for the user.
        request_data (dict): The JSON payload to send with the POST request.
        response_data (dict): The expected response data from the service.
        service_patch (str): The path to the service function to patch.
        route (str): The API route to test.

    Returns:
        dict: The JSON response data from the endpoint.
    """
    mock_user = UserInfo(username="test_user", permissions=permission_list)
    headers = {"Authorization": f"Bearer {auth_token}"}

    with patch("httpx.AsyncClient.post") as mock_post:
        mock_post.return_value = Mock()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"permissions": permission_list}
        with patch(service_patch) as mock_create:
            mock_create.return_value = response_data
            with patch("app.middleware.verify_login_permissions.verify_permissions_short") as mock_verify, patch("app.api.db.get_async_session", return_value=session):

                mock_verify.return_value = mock_user

                if verb.lower() == "get":
                    response = test_app.get(route, json=request_data, headers=headers)
                elif verb.lower() == "post":
                    response = test_app.post(route, json=request_data, headers=headers)
                elif verb.lower() == "put":
                    response = test_app.put(route, json=request_data, headers=headers)
                elif verb.lower() == "delete":
                    response = test_app.delete(route, json=request_data, headers=headers)
                else:
                    # default get
                    response = test_app.get(route, json=request_data, headers=headers)

                # Validate response status
                assert response.status_code == response_status_code, f"Expected {response_status_code} but got {response.status_code}"

                # Validate response data
                data = response.json()

                return data


@pytest.mark.asyncio
async def test_create_payment_intent_endpoint(test_app, session):
    payment_intent_data = {"user_uuid": "123e4567-e89b-12d3-a456-426614174000", "amount": 1000, "currency": "usd", "payment_method_types": ["card"], "operation_type": "purchase"}
    response_data = {"client_secret": "secret_12345", "transaction_id": "pi_1F6gB8EZPqZZJppJmR1OsJv5"}

    datas = await post_endpoint_tester(test_app, session, ["CreateMyInfos", "GetMyInfos"], payment_intent_data, response_data, "app.api.services.billing_service.create_payment_intent", "/api/v1/billing/create-payment-intent/")
    assert "client_secret" in datas
    assert datas["client_secret"] == "secret_12345"
    assert "transaction_id" in datas


@pytest.mark.asyncio
async def test_create_payment_intent_service_to_db(session: AsyncSession):
    logger.info("Test test_create_payment_intent_service_to_db commencé")
    logger.error(session)

    mock_user = UserInfo(username="test_user", permissions=["CreateMyInfos", "GetMyInfos"])
    request_data = PaymentIntentRequest(user_uuid="123e4567-e89b-12d3-a456-426614174000", amount=1000, currency="usd", payment_method_types=["card"], operation_type="purchase")
    logger.info(f"Session avant utilisation : {session}")
    with patch("stripe.PaymentIntent.create") as mock_create:
        mock_create.return_value = dict_to_mock({"id": "pi_1F6gB8EZPqZZJppJmR1OsJv5", "client_secret": "secret_12345", "status": "succeeded"})
        logger.info("Appel de create_payment_intent")
        response = await billing_service.create_payment_intent(request_data, session, mock_user)
        logger.info("reponse recue")
        assert response["client_secret"] == "secret_12345"
        assert "transaction_id" in response
