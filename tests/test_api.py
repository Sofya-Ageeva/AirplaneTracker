from typing import Dict, Optional
from unittest.mock import Mock, patch

import pytest

from src.api import AeroplanesAPI


class TestAeroplanesAPI:
    """Тесты для API"""

    def setup_method(self) -> None:
        self.api = AeroplanesAPI()

    @patch('src.api.requests.get')
    def test_get_country_coordinates_success(self, mock_get: Mock) -> None:
        """Тест успешного получения координат"""
        # Мокаем ответ API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'boundingbox': ['40.0', '45.0', '30.0', '35.0'],
                'display_name': 'Test Country'
            }
        ]
        mock_get.return_value = mock_response

        coords: Optional[Dict[str, float]] = self.api.get_country_coordinates("Test Country")

        assert coords is not None
        assert coords['south'] == 40.0
        assert coords['north'] == 45.0
        assert coords['west'] == 30.0
        assert coords['east'] == 35.0

    @patch('src.api.requests.get')
    def test_get_country_coordinates_not_found(self, mock_get: Mock) -> None:
        """Тест: страна не найдена"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        with pytest.raises(Exception):
            self.api.get_country_coordinates("NonExistent")

    @patch('src.api.requests.get')
    def test_make_request_error(self, mock_get: Mock) -> None:
        """Тест: ошибка запроса"""
        mock_get.side_effect = Exception("Connection error")

        with pytest.raises(Exception):
            self.api.get_country_coordinates("Test")
