from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class IntroPageRequirements(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = (ROOT / "app.py").read_text(encoding="utf-8")

    def test_page_is_intro_only(self):
        forbidden = ["API Key", "API Base URL", "st.chat_input", "API Reference", "Hysteria2 Relay"]
        for text in forbidden:
            with self.subTest(text=text):
                self.assertNotIn(text, self.app)

    def test_page_has_core_intro_sections(self):
        for text in ["DeepSeek V4", "Architecture", "Benchmarks", "Long Context", "Reasoning"]:
            with self.subTest(text=text):
                self.assertIn(text, self.app)

    def test_page_does_not_use_emoji_page_icon(self):
        self.assertIn('page_icon=None', self.app)


class StartupRequirements(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = (ROOT / "start.sh").read_text(encoding="utf-8")

    def test_streamlit_is_not_blocked_by_initial_sleep(self):
        worker = self.script.index("start_backend_with_retry")
        streamlit = self.script.index("exec streamlit run")
        self.assertLess(worker, streamlit)
        self.assertIn("start_backend_with_retry &", self.script)

    def test_backend_retries_three_times_after_delay(self):
        self.assertIn('BACKEND_MAX_ATTEMPTS="${BACKEND_MAX_ATTEMPTS:-3}"', self.script)
        self.assertIn('BACKEND_RETRY_DELAY="${BACKEND_RETRY_DELAY:-60}"', self.script)
        self.assertIn('sleep "$BACKEND_RETRY_DELAY"', self.script)
        self.assertIn('while [ "$attempt" -le "$BACKEND_MAX_ATTEMPTS" ]', self.script)


if __name__ == "__main__":
    unittest.main()
