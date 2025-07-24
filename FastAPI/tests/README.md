# Fetch Outlet Endpoint Test Plan

This directory contains comprehensive tests for the fetch outlet GET endpoint (`/fetchOutlet/`).

## Test Structure

The test suite is organized into several categories:

### 1. Unit Tests (`TestFetchOutletUnit`)
- Test the `getRestaurant()` function in isolation
- Mock database connections and responses
- Validate data transformation and formatting
- Test edge cases like empty results and single entries

### 2. Integration Tests (`TestFetchOutletIntegration`)
- Test the complete API endpoint using FastAPI TestClient
- Verify HTTP responses and status codes
- Test endpoint behavior with different data scenarios
- Validate end-to-end functionality

### 3. Error Handling Tests (`TestFetchOutletErrorHandling`)
- Test database connection failures
- Test query execution errors
- Test cursor fetch errors
- Verify proper error propagation

### 4. Response Format Tests (`TestFetchOutletResponseFormat`)
- Validate JSON response structure
- Check required fields presence
- Test data type constraints
- Verify coordinate ranges (lat/lng)

### 5. Performance Tests (`TestFetchOutletPerformance`)
- Test handling of large datasets
- Verify response times with multiple restaurants
- Check memory usage patterns

### 6. Edge Case Tests (`TestFetchOutletEdgeCases`)
- Test special characters in restaurant names/addresses
- Test null/None values handling
- Test Unicode characters support
- Test boundary conditions

## Running the Tests

### Prerequisites

```bash
pip install -r requirements.txt
```

### Basic Usage

```bash
# Run all tests
python -m pytest tests/test_fetch_outlet.py

# Run with verbose output
python -m pytest tests/test_fetch_outlet.py -v

# Run specific test categories
python -m pytest tests/test_fetch_outlet.py -m unit
python -m pytest tests/test_fetch_outlet.py -m integration
python -m pytest tests/test_fetch_outlet.py -m performance
python -m pytest tests/test_fetch_outlet.py -m edge_case
```

### Using the Test Runner Script

```bash
# Run all tests
python run_tests.py

# Run specific categories
python run_tests.py --unit
python run_tests.py --integration
python run_tests.py --performance
python run_tests.py --edge-case

# Run with coverage report
python run_tests.py --coverage

# Run with verbose output
python run_tests.py --verbose
```

### Coverage Reports

To generate coverage reports:

```bash
# Install coverage (if not already installed)
pip install pytest-cov

# Run tests with coverage
python run_tests.py --coverage

# View HTML coverage report
open htmlcov/index.html
```

## Test Data

The tests use mocked data to avoid dependencies on actual database connections. Sample test data includes:

- Restaurant names with various formats and special characters
- Geographic coordinates (latitude/longitude)
- Address information
- Waze URL links
- Edge cases with null/None values

## Expected API Response Format

The fetch outlet endpoint should return a JSON array with the following structure:

```json
[
  {
    "id": 0,
    "name": "Restaurant Name",
    "address": "Restaurant Address",
    "lat": 40.7128,
    "lng": -74.0060,
    "waze_url": "https://waze.com/link",
    "radius": 5000
  }
]
```

## Test Coverage Goals

- **Unit Tests**: 100% coverage of the `getRestaurant()` function
- **Integration Tests**: Cover all API endpoint paths
- **Error Handling**: Cover all potential failure scenarios
- **Edge Cases**: Cover boundary conditions and special cases

## Mock Strategy

The tests use Python's `unittest.mock` library to:

- Mock database connections (`psycopg2` connections)
- Mock cursor operations and database queries
- Mock the `initDB_cnxn()` function
- Simulate various database response scenarios
- Test error conditions without actual database failures

## Continuous Integration

These tests are designed to run in CI/CD pipelines without requiring:
- Actual database connections
- External service dependencies
- Specific environment configurations

## Adding New Tests

When adding new tests:

1. Follow the existing naming conventions
2. Use appropriate test markers (@pytest.mark.unit, etc.)
3. Include docstrings explaining the test purpose
4. Mock all external dependencies
5. Add assertions for both positive and negative cases

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running tests from the FastAPI directory
2. **Missing Dependencies**: Run `pip install -r requirements.txt`
3. **Path Issues**: Use the test runner script or ensure PYTHONPATH includes the app directory

### Debug Mode

Run tests with detailed output:

```bash
python -m pytest tests/test_fetch_outlet.py -vv --tb=long
```