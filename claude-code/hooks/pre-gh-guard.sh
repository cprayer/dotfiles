#!/bin/bash
# ~/.claude/CLAUDE.md "사용자 컨펌 필수 작업" 을 결정론적으로 강제
input=$(cat)
cmd=$(printf '%s' "$input" | jq -r '.tool_input.command // ""')

ask() {
  jq -n --arg r "$1" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"ask",permissionDecisionReason:$r}}'
  exit 0
}

# --body-file 을 실제로 열어 줄 수를 센다. 세지 못하면 빈 문자열(= 사유 미첨부).
body_lines() {
  local f n
  printf '%s' "$cmd" | grep -qE '(^| )--body-file[= ]' || return 0
  f=$(printf '%s' "$cmd" | sed -nE 's/.*(^| )--body-file[= ]+"?([^"[:space:]]+)"?.*/\2/p')
  [ -n "$f" ] && [ "$f" != "-" ] && [ -r "$f" ] || return 0
  n=$(grep -cv '^[[:space:]]*$' "$f" 2>/dev/null) || return 0
  printf '%s' "$n"
}

# 분량 초과 시 ask 사유에 덧붙일 체크리스트 (형용사 대신 실측된 삭제 대상 유형)
brevity_note() {
  local n="$1"
  [ -n "$n" ] || return 0
  [ "$n" -gt 15 ] 2>/dev/null || { printf ' / 본문 %s줄 (상한 15 — 통과)' "$n"; return 0; }
  printf '%s' " / ⚠ 본문 ${n}줄 — pr-draft 상한 15줄 초과입니다. 게시 전에 아래 유형부터 걷어내고 다시 시도하세요: (1) 컷오버 일정·경위 재서술 (2) 표·수치에 이미 있는 값의 문장 재서술 (3) 설계 배경·트레이드오프 설명 (4) 리뷰어 확인 체크리스트·코드리뷰 포인트·확인 완료 문구 (5) 빌드·검증 생략의 환경적 사유, conflict 해결 과정. 초과분이 전부 리뷰 판단에 쓰이는 근거(수치·해시·로그·출처 링크)라면 그 사실을 사용자에게 한 줄로 밝히고 진행하면 됩니다."
}

case "$cmd" in
  *"gh pr create"*|*"gh pr edit"*)
    ask "PR 제목·본문 전문을 사용자에게 보여주고 컨펌받았는지 확인 — ~/.claude/CLAUDE.md 사용자 컨펌 필수 작업$(brevity_note "$(body_lines)")"
    ;;
esac

# pending(draft) 리뷰 생성인지 판정.
# draft = pulls/{n}/reviews 로 POST 하면서 event 를 일절 지정하지 않은 경우.
# event 가 붙는 순간 즉시 공개 게시되므로, 조금이라도 불확실하면 draft 로 보지 않는다.
is_pending_review() {
  # 엔드포인트가 정확히 .../pulls/{n}/reviews 여야 한다.
  # reviews/{id}/events (제출), reviews/{id} (수정) 은 뒤에 / 가 붙어 여기서 탈락한다.
  printf '%s' "$cmd" | grep -qE 'pulls/[0-9]+/reviews([[:space:]]|"|'\''|$)' || return 1

  # PATCH/PUT 은 draft 생성이 아니다.
  printf '%s' "$cmd" | grep -qE '(-X|--method)[= ]+(PATCH|PUT|DELETE)' && return 1

  # 커맨드 문자열에 event 가 보이면 draft 가 아니다.
  printf '%s' "$cmd" | grep -q 'event' && return 1

  # --input 으로 본문을 넘기는 경우 파일을 실제로 열어 event 키를 확인한다.
  if printf '%s' "$cmd" | grep -qE '(^| )--input[= ]'; then
    f=$(printf '%s' "$cmd" | sed -nE 's/.*(^| )--input[= ]+"?([^"[:space:]]+)"?.*/\2/p')
    # stdin(-) 이나 읽을 수 없는 경로면 내용을 확인할 수 없으므로 draft 로 보지 않는다.
    [ -n "$f" ] && [ "$f" != "-" ] && [ -r "$f" ] || return 1
    grep -q '"event"' "$f" && return 1
  fi

  return 0
}

# gh api 우회 차단: -f/-F/--field 등이 있으면 -X 없이도 POST 로 동작
if printf '%s' "$cmd" | grep -q 'gh api' \
  && printf '%s' "$cmd" | grep -q 'pulls' \
  && printf '%s' "$cmd" | grep -qE '(-X|--method)[= ]+(POST|PATCH|PUT)|(^| )(-f|-F|--field|--raw-field|--input)( |=)'; then
  # pending(draft) 리뷰는 공개되지 않으므로 컨펌 없이 통과시킨다.
  is_pending_review || ask "gh api 를 통한 PR 생성/편집/공개 리뷰 게시 시도 — 본문 컨펌 후 진행 (~/.claude/CLAUDE.md 사용자 컨펌 필수 작업)"
fi

exit 0
