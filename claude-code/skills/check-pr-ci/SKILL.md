---
name: check-pr-ci
description: PR 생성 후 GitHub Actions CI 상태 및 리뷰 댓글을 확인. "CI 결과", "PR 체크", "Actions 상태", "PR 리뷰 확인", "체크 통과", "CI 확인해줘" 등에 트리거.
---

# Check PR CI

PR의 GitHub Actions CI 상태와 리뷰 댓글을 `gh` CLI로 확인한다.

## Workflow

### Step 1: PR 번호 확인

인자로 PR 번호가 주어지면 사용. 없으면 현재 브랜치의 PR을 찾는다:

```bash
gh pr view --json number,title,url --jq '.number'
```

### Step 2: CI 체크 상태 확인

```bash
gh pr checks {pr_number}
```

- 모든 체크가 pass이면 통과로 판단
- pending이면 Step 2.5로 진행 (사용자에게 재실행을 요청하지 않는다)
- fail이 있으면 Step 3으로 진행

### Step 2.5: pending이면 백그라운드 모니터링

pending 체크가 있으면 백그라운드로 watch를 걸어두고, 현재 상태를 요약 보고한 뒤 완료 알림 시 Step 2부터 다시 수행해 최종 결과를 보고한다:

```bash
# Bash 도구의 run_in_background=true로 실행 — 종료 시 자동으로 재호출됨
gh pr checks {pr_number} --watch --interval 30
```

- watch는 모든 체크가 끝나면 종료된다 (fail 있으면 non-zero exit — 정상 동작)
- 이미 watch가 걸려 있으면 중복으로 걸지 않는다

### Step 3: 실패 시 로그 확인

실패한 Actions run의 로그를 확인한다:

```bash
gh run list --branch {branch} --limit 3 --json databaseId,status,conclusion,name
gh run view {run_id} --log-failed
```

실패 원인을 요약하여 사용자에게 전달한다.

### Step 4: PR 리뷰 댓글 확인

```bash
gh pr view {pr_number} --comments --json comments
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments
```

- 봇 또는 리뷰어의 댓글 내용을 요약
- 수정 요청 사항이 있으면 정리하여 전달

### Step 5: 결과 요약

아래 형식으로 결과를 보고한다:

```
## PR #{number} CI 결과

- **상태**: pass / fail / pending
- **체크 항목**: {통과 N개} / {전체 N개}
- **리뷰 댓글**: {댓글 요약 또는 "없음"}
- **수정 필요 사항**: {있으면 나열}
```
