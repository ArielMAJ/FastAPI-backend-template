"""End-to-end tests for the v1 root endpoint GET method."""

import pytest


@pytest.mark.parametrize(
    "random_return_value", [0.1, 0.2, 0.3]
)  # Specify different sleep times here
@pytest.mark.anyio
async def test_root_response_GET(client, mocker, random_return_value):
    """Test the endpoint."""
    mock_sleep = mocker.patch("asyncio.sleep")
    mock_sleep.side_effect = lambda *args, **kwargs: None

    mock_random = mocker.patch("src.utils.random_util.random")
    mock_random.return_value = random_return_value

    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World message from the back-end!"}
    mock_sleep.assert_called_with(random_return_value * 7)
