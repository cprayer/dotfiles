# codex

`~/.codex` 설정의 공개용 사본입니다. `claude-code/` 와 마찬가지로 `.chezmoiignore` 로
`chezmoi apply` 대상에서 제외돼 있습니다.

## 구성

| 경로 | 대응 위치 | 내용 |
|---|---|---|
| `config.toml` | `~/.codex/config.toml` | reasoning effort, 승인 정책, 샌드박스 모드, MCP 서버, 플러그인 |
| `hooks.json` | `~/.codex/hooks.json` | 훅 배선 |
| `hooks/*` | `~/.codex/hooks/` | PreToolUse / PostToolUse 훅 스크립트 (`../claude-code/hooks/` 와 같은 정책) |

## 훅

`pre-gh-guard.sh` 는 실행 권한이 필요합니다 (`chmod +x`). `post_git_push.py` 는
`test_post_git_push.py` 로 테스트합니다.

## AGENTS.md 공유

로컬에서는 `~/.codex/AGENTS.md` 를 `~/.claude/CLAUDE.md` 로 심볼릭 링크해 두 도구가 같은
작업 정책을 읽게 하고 있습니다.

```bash
ln -s ~/.claude/CLAUDE.md ~/.codex/AGENTS.md
```

## 빠져 있는 것

`auth.json`, 세션 로그·SQLite, `[projects.*]` 신뢰 경로, `[otel]` 내보내기 설정,
`[shell_environment_policy.set]` (시크릿 포함), `[hooks.state]` 신뢰 해시, 사내 MCP 서버와
마켓플레이스는 전부 제외했습니다. `[hooks.state]` 가 없으면 새 머신에서 훅 신뢰 여부를
Codex 가 다시 물어보는데, 정상 동작입니다.
