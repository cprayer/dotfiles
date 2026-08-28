---
name: proto-rename
description: |
  Rename proto fields or messages in .proto definitions and propagate to Kotlin service layers.
  Triggers on: "proto rename", "proto 이름 변경", "proto 필드", "message 이름",
  and any field/message rename where a .proto file is involved.
---

# Proto Rename Skill

## Workflow
1. Grep으로 변경 대상의 모든 사용처 찾기 (proto, kt, test)
2. 사용자에게 변경 스코프 목록 보여주기
3. 변경 순서: proto → Kotlin service → test → converter
4. 검증: `./gradlew :module-name:build`

## Rules
- Proto field number는 절대 변경하지 않음
- 하위 호환성 유지 확인
- admin proto와 service proto 구분하여 각각 확인
- 변경 스코프 밖 파일은 절대 변경하지 않음
