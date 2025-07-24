"""
Test plan for the fetch outlet GET endpoint

This test suite covers:
1. Unit tests for the getRestaurant function
2. Integration tests for the API endpoint
3. Database connection tests
4. Error handling tests
5. Response format validation tests
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
import psycopg2
from app.main import app
from app.routers.fetchOutlet import getRestaurant, router
from app.utility import initDB_cnxn


# Test client for integration tests
client = TestClient(app)


class TestFetchOutletUnit:
    """Unit tests for the outlet fetching functionality"""
    
    def test_getRestaurant_success(self):
        """Test successful restaurant data retrieval from database"""
        # Mock database connection and cursor
        mock_cnxn = Mock()
        mock_cursor = Mock()
        mock_cnxn.cursor.return_value = mock_cursor
        
        # Mock database response
        mock_cursor.fetchall.return_value = [
            ("Restaurant A", "123 Main St", 40.7128, -74.0060, "https://waze.com/link1"),
            ("Restaurant B", "456 Oak Ave", 40.7589, -73.9851, "https://waze.com/link2"),
            ("Restaurant C", "789 Pine Rd", 40.7831, -73.9712, "https://waze.com/link3")
        ]
        
        # Execute function
        result = getRestaurant(mock_cnxn)
        
        # Assertions
        assert len(result) == 3
        assert result[0]["id"] == 0
        assert result[0]["name"] == "Restaurant A"
        assert result[0]["address"] == "123 Main St"
        assert result[0]["lat"] == 40.7128
        assert result[0]["lng"] == -74.0060
        assert result[0]["waze_url"] == "https://waze.com/link1"
        assert result[0]["radius"] == 5000
        
        assert result[1]["id"] == 1
        assert result[1]["name"] == "Restaurant B"
        
        # Verify database interactions
        mock_cnxn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM RestaurantGet();")
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()
    
    def test_getRestaurant_empty_result(self):
        """Test handling of empty database result"""
        # Mock database connection and cursor
        mock_cnxn = Mock()
        mock_cursor = Mock()
        mock_cnxn.cursor.return_value = mock_cursor
        
        # Mock empty database response
        mock_cursor.fetchall.return_value = []
        
        # Execute function
        result = getRestaurant(mock_cnxn)
        
        # Assertions
        assert result == []
        
        # Verify database interactions
        mock_cnxn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM RestaurantGet();")
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()
    
    def test_getRestaurant_single_result(self):
        """Test handling of single restaurant result"""
        # Mock database connection and cursor
        mock_cnxn = Mock()
        mock_cursor = Mock()
        mock_cnxn.cursor.return_value = mock_cursor
        
        # Mock single restaurant response
        mock_cursor.fetchall.return_value = [
            ("Solo Restaurant", "999 Single St", 40.7000, -74.0000, "https://waze.com/solo")
        ]
        
        # Execute function
        result = getRestaurant(mock_cnxn)
        
        # Assertions
        assert len(result) == 1
        assert result[0]["id"] == 0
        assert result[0]["name"] == "Solo Restaurant"
        assert result[0]["address"] == "999 Single St"
        assert result[0]["lat"] == 40.7000
        assert result[0]["lng"] == -74.0000
        assert result[0]["waze_url"] == "https://waze.com/solo"
        assert result[0]["radius"] == 5000
    
    def test_getRestaurant_data_types(self):
        """Test that returned data has correct types"""
        # Mock database connection and cursor
        mock_cnxn = Mock()
        mock_cursor = Mock()
        mock_cnxn.cursor.return_value = mock_cursor
        
        # Mock database response with specific data types
        mock_cursor.fetchall.return_value = [
            ("Test Restaurant", "123 Test St", 40.7128, -74.0060, "https://waze.com/test")
        ]
        
        # Execute function
        result = getRestaurant(mock_cnxn)
        
        # Type assertions
        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert isinstance(result[0]["id"], int)
        assert isinstance(result[0]["name"], str)
        assert isinstance(result[0]["address"], str)
        assert isinstance(result[0]["lat"], (int, float))
        assert isinstance(result[0]["lng"], (int, float))
        assert isinstance(result[0]["waze_url"], str)
        assert isinstance(result[0]["radius"], int)


class TestFetchOutletIntegration:
    """Integration tests for the fetch outlet API endpoint"""
    
    @patch('app.routers.fetchOutlet.initDB_cnxn')
    def test_get_outlet_endpoint_success(self, mock_init_db):
        """Test successful API call to fetch outlet endpoint"""
        # Mock database connection and operations
        mock_cnxn = Mock()
        mock_cursor = Mock()
        mock_cnxn.cursor.return_value = mock_cursor
        mock_init_db.return_value = mock_cnxn
        
        # Mock database response
        mock_cursor.fetchall.return_value = [
            ("API Restaurant", "API Address", 40.7128, -74.0060, "https://waze.com/api")
        ]
        
        # Make API call
        response = client.get("/fetchOutlet/")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "API Restaurant"
        assert data[0]["address"] == "API Address"
        assert data[0]["radius"] == 5000
    
    @patch('app.routers.fetchOutlet.initDB_cnxn')
    def test_get_outlet_endpoint_empty_response(self, mock_init_db):
        """Test API endpoint with empty database response"""
        # Mock database connection and operations
        mock_cnxn = Mock()
        mock_cursor = Mock()
        mock_cnxn.cursor.return_value = mock_cursor
        mock_init_db.return_value = mock_cnxn
        
        # Mock empty database response
        mock_cursor.fetchall.return_value = []
        
        # Make API call
        response = client.get("/fetchOutlet/")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert data == []
    
    @patch('app.routers.fetchOutlet.initDB_cnxn')
    def test_get_outlet_endpoint_multiple_restaurants(self, mock_init_db):
        """Test API endpoint with multiple restaurants"""
        # Mock database connection and operations
        mock_cnxn = Mock()
        mock_cursor = Mock()
        mock_cnxn.cursor.return_value = mock_cursor
        mock_init_db.return_value = mock_cnxn
        
        # Mock multiple restaurants response
        mock_cursor.fetchall.return_value = [
            ("Restaurant 1", "Address 1", 40.7128, -74.0060, "https://waze.com/1"),
            ("Restaurant 2", "Address 2", 40.7589, -73.9851, "https://waze.com/2"),
            ("Restaurant 3", "Address 3", 40.7831, -73.9712, "https://waze.com/3"),
            ("Restaurant 4", "Address 4", 40.8176, -73.9582, "https://waze.com/4"),
            ("Restaurant 5", "Address 5", 40.8518, -73.9390, "https://waze.com/5")
        ]
        
        # Make API call
        response = client.get("/fetchOutlet/")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        
        # Verify sequential IDs
        for i, restaurant in enumerate(data):
            assert restaurant["id"] == i
            assert restaurant["name"] == f"Restaurant {i+1}"
            assert restaurant["radius"] == 5000


class TestFetchOutletErrorHandling:
    """Error handling tests for the fetch outlet functionality"""
    
    @patch('app.routers.fetchOutlet.initDB_cnxn')
    def test_database_connection_error(self, mock_init_db):
        """Test handling of database connection errors"""
        # Mock database connection error
        mock_init_db.side_effect = psycopg2.Error("Database connection failed")
        
        # Make API call and expect it to raise an error
        with pytest.raises(psycopg2.Error):
            response = client.get("/fetchOutlet/")
    
    @patch('app.routers.fetchOutlet.initDB_cnxn')
    def test_database_query_error(self, mock_init_db):
        """Test handling of database query errors"""
        # Mock database connection
        mock_cnxn = Mock()
        mock_cursor = Mock()
        mock_cnxn.cursor.return_value = mock_cursor
        mock_init_db.return_value = mock_cnxn
        
        # Mock database query error
        mock_cursor.execute.side_effect = psycopg2.Error("Query execution failed")
        
        # Make API call and expect it to raise an error
        with pytest.raises(psycopg2.Error):
            response = client.get("/fetchOutlet/")
    
    @patch('app.routers.fetchOutlet.initDB_cnxn')
    def test_cursor_fetch_error(self, mock_init_db):
        """Test handling of cursor fetch errors"""
        # Mock database connection
        mock_cnxn = Mock()
        mock_cursor = Mock()
        mock_cnxn.cursor.return_value = mock_cursor
        mock_init_db.return_value = mock_cnxn
        
        # Mock cursor fetch error
        mock_cursor.fetchall.side_effect = psycopg2.Error("Fetch operation failed")
        
        # Make API call and expect it to raise an error
        with pytest.raises(psycopg2.Error):
            response = client.get("/fetchOutlet/")


class TestFetchOutletResponseFormat:
    """Tests for response format validation"""
    
    @patch('app.routers.fetchOutlet.initDB_cnxn')
    def test_response_format_structure(self, mock_init_db):
        """Test that response follows the expected JSON structure"""
        # Mock database connection and operations
        mock_cnxn = Mock()
        mock_cursor = Mock()
        mock_cnxn.cursor.return_value = mock_cursor
        mock_init_db.return_value = mock_cnxn
        
        # Mock database response
        mock_cursor.fetchall.return_value = [
            ("Test Restaurant", "Test Address", 40.7128, -74.0060, "https://waze.com/test")
        ]
        
        # Make API call
        response = client.get("/fetchOutlet/")
        
        # Assertions for response structure
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        
        data = response.json()
        assert isinstance(data, list)
        
        # Validate each restaurant object structure
        for restaurant in data:
            required_fields = ["id", "name", "address", "lat", "lng", "waze_url", "radius"]
            for field in required_fields:
                assert field in restaurant, f"Missing required field: {field}"
    
    @patch('app.routers.fetchOutlet.initDB_cnxn')
    def test_response_field_constraints(self, mock_init_db):
        """Test field value constraints and ranges"""
        # Mock database connection and operations
        mock_cnxn = Mock()
        mock_cursor = Mock()
        mock_cnxn.cursor.return_value = mock_cursor
        mock_init_db.return_value = mock_cnxn
        
        # Mock database response with boundary values
        mock_cursor.fetchall.return_value = [
            ("Restaurant", "Address", -90.0, -180.0, "https://waze.com/test"),
            ("Restaurant", "Address", 90.0, 180.0, "https://waze.com/test2")
        ]
        
        # Make API call
        response = client.get("/fetchOutlet/")
        data = response.json()
        
        # Validate constraints
        for restaurant in data:
            # Latitude should be between -90 and 90
            assert -90 <= restaurant["lat"] <= 90
            # Longitude should be between -180 and 180
            assert -180 <= restaurant["lng"] <= 180
            # Radius should be positive
            assert restaurant["radius"] > 0
            # URLs should be strings
            assert isinstance(restaurant["waze_url"], str)


class TestFetchOutletPerformance:
    """Performance and load tests for the fetch outlet endpoint"""
    
    @patch('app.routers.fetchOutlet.initDB_cnxn')
    def test_large_dataset_handling(self, mock_init_db):
        """Test endpoint performance with large dataset"""
        # Mock database connection and operations
        mock_cnxn = Mock()
        mock_cursor = Mock()
        mock_cnxn.cursor.return_value = mock_cursor
        mock_init_db.return_value = mock_cnxn
        
        # Mock large dataset (100 restaurants)
        large_dataset = []
        for i in range(100):
            large_dataset.append((
                f"Restaurant {i}",
                f"Address {i}",
                40.0 + (i * 0.01),
                -74.0 + (i * 0.01),
                f"https://waze.com/restaurant{i}"
            ))
        
        mock_cursor.fetchall.return_value = large_dataset
        
        # Make API call
        response = client.get("/fetchOutlet/")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 100
        
        # Verify all entries are properly formatted
        for i, restaurant in enumerate(data):
            assert restaurant["id"] == i
            assert restaurant["name"] == f"Restaurant {i}"
            assert restaurant["radius"] == 5000


class TestFetchOutletEdgeCases:
    """Edge case tests for the fetch outlet functionality"""
    
    @patch('app.routers.fetchOutlet.initDB_cnxn')
    def test_special_characters_in_data(self, mock_init_db):
        """Test handling of special characters in restaurant data"""
        # Mock database connection and operations
        mock_cnxn = Mock()
        mock_cursor = Mock()
        mock_cnxn.cursor.return_value = mock_cursor
        mock_init_db.return_value = mock_cnxn
        
        # Mock data with special characters
        mock_cursor.fetchall.return_value = [
            ("Café José's & Grillé", "123 Münch St. Apt #5", 40.7128, -74.0060, "https://waze.com/café"),
            ("O'Malley's Pub", "456 O'Connor Ave", 40.7589, -73.9851, "https://waze.com/omalley"),
            ("北京餐厅", "789 中文街", 40.7831, -73.9712, "https://waze.com/beijing")
        ]
        
        # Make API call
        response = client.get("/fetchOutlet/")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["name"] == "Café José's & Grillé"
        assert data[1]["name"] == "O'Malley's Pub"
        assert data[2]["name"] == "北京餐厅"
    
    @patch('app.routers.fetchOutlet.initDB_cnxn')
    def test_null_and_none_values(self, mock_init_db):
        """Test handling of null/None values in database response"""
        # Mock database connection and operations
        mock_cnxn = Mock()
        mock_cursor = Mock()
        mock_cnxn.cursor.return_value = mock_cursor
        mock_init_db.return_value = mock_cnxn
        
        # Mock data with None values
        mock_cursor.fetchall.return_value = [
            ("Restaurant", None, 40.7128, -74.0060, "https://waze.com/test"),
            (None, "Address", 40.7589, -73.9851, None),
            ("Valid Restaurant", "Valid Address", 40.7831, -73.9712, "https://waze.com/valid")
        ]
        
        # Make API call
        response = client.get("/fetchOutlet/")
        
        # Assertions
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        
        # Check that None values are preserved/handled appropriately
        assert data[0]["address"] is None
        assert data[1]["name"] is None
        assert data[1]["waze_url"] is None
        assert data[2]["name"] == "Valid Restaurant"


# Pytest configuration and fixtures
@pytest.fixture
def mock_database():
    """Fixture providing a mock database connection"""
    mock_cnxn = Mock()
    mock_cursor = Mock()
    mock_cnxn.cursor.return_value = mock_cursor
    return mock_cnxn, mock_cursor


@pytest.fixture
def sample_restaurant_data():
    """Fixture providing sample restaurant data for tests"""
    return [
        ("Pizza Palace", "123 Pizza St", 40.7128, -74.0060, "https://waze.com/pizza"),
        ("Burger Barn", "456 Burger Ave", 40.7589, -73.9851, "https://waze.com/burger"),
        ("Taco Town", "789 Taco Rd", 40.7831, -73.9712, "https://waze.com/taco")
    ]


# Test configuration
pytest_plugins = []


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "edge_case: Edge case tests")