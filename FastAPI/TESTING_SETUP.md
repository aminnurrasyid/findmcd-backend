# Testing Setup Guide for Fetch Outlet Endpoint

This document provides a complete guide for setting up and running the pytest test plan for the fetch outlet GET endpoint.

## 🎯 Test Plan Overview

The test plan covers the `/fetchOutlet/` GET endpoint with comprehensive testing including:

- **Unit Tests**: Testing the `getRestaurant()` function in isolation
- **Integration Tests**: Testing the complete API endpoint
- **Error Handling**: Database connection and query error scenarios
- **Response Format**: JSON structure and field validation
- **Performance**: Large dataset handling
- **Edge Cases**: Special characters, null values, boundary conditions

## 📋 Prerequisites

### System Requirements
- Python 3.8 or higher
- pip or pip3 package manager
- Virtual environment support (recommended)

### Environment Setup

1. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv test_env
   source test_env/bin/activate  # On Linux/Mac
   # or
   test_env\Scripts\activate     # On Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python -c "import pytest; print('✅ pytest installed successfully')"
   python -c "import fastapi; print('✅ FastAPI installed successfully')"
   ```

## 🚀 Running the Tests

### Quick Start

```bash
# Navigate to the FastAPI directory
cd FastAPI

# Run all tests
python -m pytest tests/test_fetch_outlet.py -v

# Or use the test runner script
python run_tests.py
```

### Test Categories

Run specific test categories using markers:

```bash
# Unit tests only
python -m pytest tests/test_fetch_outlet.py -m unit -v

# Integration tests only  
python -m pytest tests/test_fetch_outlet.py -m integration -v

# Performance tests only
python -m pytest tests/test_fetch_outlet.py -m performance -v

# Edge case tests only
python -m pytest tests/test_fetch_outlet.py -m edge_case -v
```

### Using the Test Runner Script

The provided `run_tests.py` script offers convenient options:

```bash
# Basic usage
python run_tests.py                    # Run all tests
python run_tests.py --unit             # Unit tests only
python run_tests.py --integration      # Integration tests only
python run_tests.py --performance      # Performance tests only
python run_tests.py --edge-case        # Edge case tests only

# Advanced options
python run_tests.py --coverage         # Run with coverage report
python run_tests.py --verbose          # Detailed output
python run_tests.py --file tests/test_fetch_outlet.py  # Specific file
```

### Coverage Reports

To generate test coverage reports:

```bash
# Install coverage plugin (if not already installed)
pip install pytest-cov

# Run tests with coverage
python run_tests.py --coverage

# View HTML coverage report
open htmlcov/index.html  # On Mac/Linux
# or
start htmlcov/index.html # On Windows
```

## 📊 Test Structure

### File Organization
```
FastAPI/
├── tests/
│   ├── __init__.py
│   ├── test_fetch_outlet.py     # Main test file
│   └── README.md                # Test documentation
├── pytest.ini                   # Pytest configuration
├── run_tests.py                # Test runner script
└── requirements.txt             # Dependencies (updated with pytest)
```

### Test Classes

1. **`TestFetchOutletUnit`** - Unit tests for `getRestaurant()` function
2. **`TestFetchOutletIntegration`** - API endpoint integration tests
3. **`TestFetchOutletErrorHandling`** - Error scenario tests
4. **`TestFetchOutletResponseFormat`** - Response validation tests
5. **`TestFetchOutletPerformance`** - Performance and load tests
6. **`TestFetchOutletEdgeCases`** - Edge case and boundary tests

## 🔧 Test Configuration

### Pytest Configuration (`pytest.ini`)

The test suite is configured with:
- Automatic test discovery in the `tests/` directory
- Verbose output with short traceback format
- Color output for better readability
- Test duration reporting
- Custom markers for test categorization

### Markers

Tests are organized using custom markers:
- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.performance` - Performance tests
- `@pytest.mark.edge_case` - Edge case tests

## 🎭 Mocking Strategy

The tests use comprehensive mocking to avoid external dependencies:

- **Database Connections**: Mock `psycopg2` connections and cursors
- **Database Queries**: Mock SQL query execution and results
- **API Responses**: Mock FastAPI responses and status codes
- **Error Conditions**: Simulate database and connection errors

### Example Mock Usage

```python
@patch('app.routers.fetchOutlet.initDB_cnxn')
def test_example(mock_init_db):
    # Setup mock
    mock_cnxn = Mock()
    mock_cursor = Mock()
    mock_cnxn.cursor.return_value = mock_cursor
    mock_init_db.return_value = mock_cnxn
    
    # Mock database response
    mock_cursor.fetchall.return_value = [
        ("Restaurant Name", "Address", 40.7128, -74.0060, "https://waze.com/link")
    ]
    
    # Test the endpoint
    response = client.get("/fetchOutlet/")
    assert response.status_code == 200
```

## 📈 Expected Test Results

### Successful Test Run Output
```
tests/test_fetch_outlet.py::TestFetchOutletUnit::test_getRestaurant_success PASSED
tests/test_fetch_outlet.py::TestFetchOutletUnit::test_getRestaurant_empty_result PASSED
tests/test_fetch_outlet.py::TestFetchOutletIntegration::test_get_outlet_endpoint_success PASSED
...
========================= 20 passed in 2.34s =========================
```

### Coverage Report Example
```
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
app/routers/fetchOutlet.py           15      0   100%
app/utility.py                        8      0   100%
---------------------------------------------------------------
TOTAL                                23      0   100%
```

## 🐛 Troubleshooting

### Common Issues and Solutions

1. **Import Errors**
   ```bash
   # Ensure you're in the FastAPI directory
   cd FastAPI
   
   # Add current directory to Python path
   export PYTHONPATH="${PYTHONPATH}:."
   ```

2. **Module Not Found**
   ```bash
   # Install missing dependencies
   pip install -r requirements.txt
   
   # Verify FastAPI installation
   python -c "import fastapi; print('OK')"
   ```

3. **Test Discovery Issues**
   ```bash
   # Run from the correct directory
   cd FastAPI
   
   # Use explicit test file path
   python -m pytest tests/test_fetch_outlet.py
   ```

4. **Virtual Environment Issues**
   ```bash
   # Deactivate and recreate virtual environment
   deactivate
   rm -rf test_env
   python3 -m venv test_env
   source test_env/bin/activate
   pip install -r requirements.txt
   ```

### Debug Mode

For detailed debugging information:

```bash
# Run with maximum verbosity and full tracebacks
python -m pytest tests/test_fetch_outlet.py -vv --tb=long

# Run with Python debugger on failures
python -m pytest tests/test_fetch_outlet.py --pdb

# Run with warnings enabled
python -m pytest tests/test_fetch_outlet.py --disable-warnings=false
```

## 🎯 Test Scenarios Covered

### 1. Happy Path Tests
- ✅ Successful restaurant data retrieval
- ✅ Multiple restaurants response
- ✅ Proper JSON formatting
- ✅ Correct HTTP status codes

### 2. Edge Cases
- ✅ Empty database results
- ✅ Single restaurant result
- ✅ Special characters in names/addresses
- ✅ Unicode character support
- ✅ Null/None value handling

### 3. Error Scenarios
- ✅ Database connection failures
- ✅ SQL query execution errors
- ✅ Cursor operation failures
- ✅ Network timeout simulation

### 4. Performance Tests
- ✅ Large dataset handling (100+ restaurants)
- ✅ Response time validation
- ✅ Memory usage patterns

### 5. Data Validation
- ✅ Required field presence
- ✅ Data type validation
- ✅ Coordinate range validation (lat/lng)
- ✅ URL format validation

## 📚 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-cov Coverage Plugin](https://pytest-cov.readthedocs.io/)

## 🤝 Contributing

When adding new tests:

1. Follow the existing naming conventions (`test_*`)
2. Use appropriate test markers for categorization
3. Include comprehensive docstrings
4. Mock all external dependencies
5. Test both success and failure scenarios
6. Validate response formats and data types

## 📝 Test Maintenance

Regular maintenance tasks:

- Update test data to reflect real-world scenarios
- Add tests for new endpoint features
- Update mocks when API contracts change
- Monitor test execution times
- Review and update test coverage goals