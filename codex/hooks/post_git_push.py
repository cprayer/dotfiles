#!/usr/bin/env python3
import json
import os
import re
import shlex
import subprocess
import sys
from urllib.parse import quote


SEPARATOR_CHARS = frozenset(";&|()\n")
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")


def _is_separator(token):
    return bool(token) and all(character in SEPARATOR_CHARS for character in token)


def _command_segments(command):
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()\n")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = ""

    segment = []
    try:
        for token in lexer:
            if _is_separator(token):
                if segment:
                    yield segment
                    segment = []
            else:
                segment.append(token)
    except ValueError:
        return

    if segment:
        yield segment


def _skip_command_prefix(segment):
    index = 0
    while index < len(segment):
        token = segment[index]
        if ASSIGNMENT.match(token):
            index += 1
            continue
        if token == "command":
            index += 1
            continue
        if token == "env":
            index += 1
            while index < len(segment):
                token = segment[index]
                if ASSIGNMENT.match(token) or token in {"-i", "--ignore-environment"}:
                    index += 1
                    continue
                if token in {"-u", "--unset"} and index + 1 < len(segment):
                    index += 2
                    continue
                if token.startswith("--unset="):
                    index += 1
                    continue
                break
            continue
        break
    return segment[index:]


def has_real_push(command):
    if not isinstance(command, str):
        return False

    for segment in _command_segments(command):
        executable = _skip_command_prefix(segment)
        if len(executable) < 2:
            continue
        if os.path.basename(executable[0]) != "git" or executable[1] != "push":
            continue
        if any(argument in {"--dry-run", "-n"} for argument in executable[2:]):
            continue
        return True
    return False


def successful(tool_response):
    if not isinstance(tool_response, dict):
        return False
    exit_code = tool_response.get("exit_code")
    return type(exit_code) is int and exit_code == 0


def _run_git(cwd, *arguments):
    result = subprocess.run(
        ["git", *arguments],
        cwd=cwd,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def _github_url(remote):
    if not remote:
        return None

    patterns = (
        r"^git@github\.com:(.+)$",
        r"^ssh://git@github\.com/(.+)$",
        r"^https?://github\.com/(.+)$",
    )
    for pattern in patterns:
        match = re.match(pattern, remote.rstrip("/"))
        if not match:
            continue
        path = match.group(1)
        if path.endswith(".git"):
            path = path[:-4]
        if len(path.split("/")) != 2:
            return None
        return f"https://github.com/{path}"
    return None


def handle(payload):
    if not isinstance(payload, dict):
        return None
    if payload.get("hook_event_name") != "PostToolUse" or payload.get("tool_name") != "Bash":
        return None
    if not successful(payload.get("tool_response")):
        return None

    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict) or not has_real_push(tool_input.get("command")):
        return None

    cwd = payload.get("cwd")
    if not isinstance(cwd, str) or not cwd:
        return None

    branch = _run_git(cwd, "branch", "--show-current")
    remote = _run_git(cwd, "remote", "get-url", "origin")
    repository_url = _github_url(remote)
    if not branch or branch == "HEAD" or not repository_url:
        return None

    branch_path = quote(branch, safe="/")
    message = (
        "git push 성공. 응답에 반드시 포함할 것 — "
        f"브랜치: {repository_url}/tree/{branch_path} / "
        f"PR 생성: {repository_url}/pull/new/{branch_path} / "
        "관련 지라 티켓이 있으면 티켓 URL도 함께 안내"
    )
    return {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": message,
        }
    }


def main():
    try:
        payload = json.load(sys.stdin)
        result = handle(payload)
    except (json.JSONDecodeError, OSError, ValueError):
        return

    if result is not None:
        json.dump(result, sys.stdout, ensure_ascii=False, separators=(",", ":"))


if __name__ == "__main__":
    main()
