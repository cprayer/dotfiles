#!/bin/bash
# ~/.claude/CLAUDE.md "사용자 컨펌 필수 작업" 을 결정론적으로 강제
input=$(cat)
cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // ""')

ask() {
  jq -n --arg r "$1" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"ask",permissionDecisionReason:$r}}'
  exit 0
}

case "$cmd" in
  *"gh pr create"*|*"gh pr edit"*)
    ask "PR 제목·본문 전문을 사용자에게 보여주고 컨펌받았는지 확인 — ~/.claude/CLAUDE.md 사용자 컨펌 필수 작업"
    ;;
esac

# gh api 우회 차단: -f/-F/--field 등이 있으면 -X 없이도 POST 로 동작
if printf '%s' "$cmd" | grep -q 'gh api' \
  && printf '%s' "$cmd" | grep -q 'pulls' \
  && printf '%s' "$cmd" | grep -qE '(-X|--method)[= ]+(POST|PATCH|PUT)|(^| )(-f|-F|--field|--raw-field|--input)( |=)'; then
  ask "gh api 를 통한 PR 생성/편집 시도 — PR 본문 컨펌 후 진행 (~/.claude/CLAUDE.md 사용자 컨펌 필수 작업)"
fi

exit 0
