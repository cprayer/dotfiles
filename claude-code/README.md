# claude-code

`~/.claude` 설정의 공개용 사본입니다. **`chezmoi apply` 대상이 아닙니다** —
라이브 `~/.claude` 에는 머신 로컬 시크릿이 들어 있어서, 정화본이 그걸 덮어쓰지 않도록
`.chezmoiignore` 로 제외해 두었습니다. 쓰려면 필요한 파일만 직접 복사하세요.

## 구성

| 경로 | 대응 위치 | 내용 |
|---|---|---|
| `settings.json` | `~/.claude/settings.json` | 권한 allowlist, 훅 배선, 플러그인 토글, 개인 취향 설정 |
| `CLAUDE.md` | `~/.claude/CLAUDE.md` | 전역 작업 정책 (컨펌 필수 작업, 커밋·푸시 규칙, 산출물 분량, 말투) |
| `rules/*.md` | `~/.claude/rules/` | `paths:` frontmatter 로 파일 유형별 스코핑되는 규칙 |
| `skills/*/SKILL.md` | `~/.claude/skills/` | 개인 스킬 |
| `hooks/*` | `~/.claude/hooks/` | PreToolUse / PostToolUse 훅 스크립트 |

## 훅

- `pre-gh-guard.sh` — `gh pr create` / `gh pr edit` / `gh api` 로 PR 을 만들거나 리뷰를
  공개 게시하려 할 때 `ask` 결정을 반환해 컨펌을 강제합니다. pending(draft) 리뷰
  (`pulls/{n}/reviews` POST 에 `event` 없음) 는 공개되지 않으므로 통과시킵니다.
- `post-git-push.sh` / `post_git_push.py` — `git push` 뒤에 브랜치 URL 과 PR 생성 링크를
  응답에 포함하도록 컨텍스트를 주입합니다.

Codex CLI 쪽 훅 스크립트는 `../codex/hooks/` 에 있습니다.

`settings.json` 의 훅 경로는 `$HOME/.claude/hooks/...` 로 적혀 있습니다. 스크립트는
실행 권한이 필요합니다 (`chmod +x`).

## 빠져 있는 것

시크릿(API 토큰), 사내 도메인·계정·서비스 좌표, 사내 플러그인 마켓플레이스, 회사 도메인
스킬·서브에이전트는 전부 제외했습니다. `settings.json` 의 `env` 블록과 `autoMode.environment`
블록도 통째로 뺐습니다 — 로컬에서 각자 채워 쓰세요.
