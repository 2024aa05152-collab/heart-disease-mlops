import pytest
from unittest.mock import MagicMock, patch
import sys
import os
import numpy as np
from fastapi.testclient import TestClient

# Add the project root to sys.path so we can import 'app'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture(scope="module")
def mock_model():
    """
    Creates a fake model object that mimics the real Sklearn model.
    """
    mock = MagicMock()
    # Mock behavior for predict: Return [0] (No disease)
    mock.predict.return_value = np.array([0])
    # Mock behavior for predict_proba: Return [[0.8, 0.2]] (80% sure)
    mock.predict_proba.return_value = np.array([[0.8, 0.2]])
    return mock

@pytest.fixture(scope="function")
def client(mock_model):
    """
    Creates a TestClient with a MOCKED model and MOCKED load status.
    """
    # 1. Start the patchers
    # We patch 'load_model' and specifically 'MODEL_LOADED' inside app.main
    with patch("mlflow.sklearn.load_model", return_value=mock_model), \
         patch("dotenv.load_dotenv"):
        
        # 2. Force reload to apply patches
        if "app.main" in sys.modules:
            del sys.modules["app.main"]
        
        # 3. Import the app newly
        import app.main as main_module
        
        # 4. Explicitly set the status variables for the health check
        main_module.model = mock_model
        main_module.MODEL_LOADED = True
        
        # 5. Yield the client
        with TestClient(main_module.app) as c:
            yield c
