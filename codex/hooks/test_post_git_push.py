import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("post_git_push.py")
MISSING = object()


class PostGitPushHookTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)
        subprocess.run(
            ["git", "init", "-q", "-b", "feature/test"],
            cwd=self.repo,
            check=True,
        )
        subprocess.run(
            ["git", "remote", "add", "origin", "git@github.com:example/repo.git"],
            cwd=self.repo,
            check=True,
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_hook(self, command, exit_code=MISSING, tool_name="Bash"):
        tool_response = {}
        if exit_code is not MISSING:
            tool_response["exit_code"] = exit_code

        payload = {
            "hook_event_name": "PostToolUse",
            "tool_name": tool_name,
            "tool_input": {"command": command},
            "tool_response": tool_response,
            "cwd": str(self.repo),
        }
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout) if result.stdout else None

    def assert_success_context(self, result):
        self.assertEqual(
            result,
            {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": (
                        "git push 성공. 응답에 반드시 포함할 것 — "
                        "브랜치: https://github.com/example/repo/tree/feature/test / "
                        "PR 생성: https://github.com/example/repo/pull/new/feature/test / "
                        "관련 지라 티켓이 있으면 티켓 URL도 함께 안내"
                    ),
                }
            },
        )

    def test_direct_successful_push_returns_links(self):
        self.assert_success_context(self.run_hook("git push origin feature/test", exit_code=0))

    def test_chained_successful_push_returns_links(self):
        command = "git status --short && git push origin feature/test"
        self.assert_success_context(self.run_hook(command, exit_code=0))

    def test_assignment_and_command_wrapper_are_supported(self):
        command = "TRACE=1 command git push origin feature/test"
        self.assert_success_context(self.run_hook(command, exit_code=0))

    def test_quoted_search_text_does_not_match(self):
        self.assertIsNone(self.run_hook("rg -n 'git push' file", exit_code=0))

    def test_echo_text_does_not_match(self):
        self.assertIsNone(self.run_hook("echo git push", exit_code=0))

    def test_failed_push_does_not_match(self):
        self.assertIsNone(self.run_hook("git push origin feature/test", exit_code=1))

    def test_dry_run_does_not_match(self):
        for flag in ("--dry-run", "-n"):
            with self.subTest(flag=flag):
                self.assertIsNone(self.run_hook(f"git push {flag} origin feature/test", exit_code=0))

    def test_missing_or_non_integer_status_does_not_match(self):
        self.assertIsNone(self.run_hook("git push origin feature/test"))
        self.assertIsNone(self.run_hook("git push origin feature/test", exit_code="0"))

    def test_non_bash_tool_does_not_match(self):
        self.assertIsNone(
            self.run_hook("git push origin feature/test", exit_code=0, tool_name="apply_patch")
        )


if __name__ == "__main__":
    unittest.main()
