from pathlib import Path
import subprocess
import unittest
import uuid

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

    def test_uuid_defaults_do_not_depend_on_procfs(self):
        self.assertNotIn("/proc/sys/kernel/random/uuid", self.script)
        self.assertIn("generate_uuid()", self.script)
        self.assertIn("python3 -c 'import uuid; print(uuid.uuid4())'", self.script)

    def test_uuid_generator_produces_uuid4(self):
        generated = subprocess.run(
            ["python3", "-c", "import uuid; print(uuid.uuid4())"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        parsed = uuid.UUID(generated)
        self.assertEqual(parsed.version, 4)
        self.assertEqual(str(parsed), generated)

    def test_explicit_credentials_override_generated_defaults(self):
        self.assertIn('if [ -n "${R_ID:-}" ]; then', self.script)
        self.assertIn('R_ID="$(generate_uuid)"', self.script)
        self.assertIn('PASSWORD="${PASSWORD:-$(generate_uuid)}"', self.script)
        self.assertIn('R_ID_LOCKED=1', self.script)

    def test_mimic_support_hooks(self):
        self.assertIn('modprobe mimic', self.script)
        self.assertIn('Rotated R_ID', self.script)
        df = (ROOT / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn("bookworm_mimic_", df)
        self.assertIn("/usr/local/bin/mimic", df)


if __name__ == "__main__":
    unittest.main()
