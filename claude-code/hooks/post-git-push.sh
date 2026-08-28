#!/bin/bash
input=$(cat)
cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // ""')
cwd=$(printf '%s' "$input" | jq -r '.cwd // "."')
case "$cmd" in
  *"git push"*)
    cd "$cwd" 2>/dev/null || exit 0
    branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null) || exit 0
    [ "$branch" = "HEAD" ] && exit 0
    url=$(gh repo view --json url -q .url 2>/dev/null) || exit 0
    msg="git push 실행됨. 푸시가 성공했다면 응답에 반드시 포함할 것 — 브랜치: ${url}/tree/${branch} / PR 생성: ${url}/pull/new/${branch} / 관련 지라 티켓이 있으면 티켓 URL도 함께 안내"
    ;;
  *) exit 0 ;;
esac
jq -n --arg c "$msg" '{hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:$c}}'
