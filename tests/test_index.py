import os
import sys
import pathlib
import unittest
from unittest.mock import patch

# Ensure src/ is in sys.path
sys.path.insert(0, str(pathlib.Path(__file__).absolute().parent.parent / "src"))

import index


class TestWorkerIndex(unittest.TestCase):

    def test_top_level_import_does_not_instantiate_api(self):
        """Verify that importing index.py does not instantiate ytm.YouTubeMusic() at top-level."""
        self.assertIsNone(index._api)

    @patch("ytm.YouTubeMusic")
    def test_get_api_lazy_instantiation(self, mock_ytm):
        """Verify that get_api() lazily instantiates ytm.YouTubeMusic()."""
        # Ensure _api is reset to None before test
        original_api = index._api
        index._api = None
        try:
            api_instance = index.get_api()
            mock_ytm.assert_called_once()
            self.assertEqual(api_instance, mock_ytm.return_value)
            self.assertEqual(index._api, mock_ytm.return_value)
        finally:
            index._api = original_api

    def test_cert_verify_bypass(self):
        """Verify that requests HTTPAdapter.cert_verify does not raise OSError for certifi bundle."""
        import requests
        adapter = requests.adapters.HTTPAdapter()
        # Passing None for conn should not raise OSError when cert_verify is patched to noop
        try:
            adapter.cert_verify(None, "https://music.youtube.com", True, None)
        except OSError as e:
            self.fail(f"cert_verify raised OSError: {e}")

    def test_pyodide_http_without_xmlhttprequest(self):
        """Verify pyodide_http patch_all handles js module without XMLHttpRequest gracefully."""
        import sys
        import types
        import pyodide_http

        # Create mock js module without XMLHttpRequest
        mock_js = types.ModuleType("js")
        mock_js.fetch = lambda *args, **kwargs: None

        with patch.dict(sys.modules, {"js": mock_js}):
            # should_patch should check hasattr without raising ImportError for XMLHttpRequest
            self.assertTrue(pyodide_http.should_patch())
            pyodide_http.patch_all()


if __name__ == "__main__":
    unittest.main()
