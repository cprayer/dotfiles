---
paths:
  - "**/*.{kt,kts}"
---

# Kotlin 코드 작성 규칙

### Kotlin 코딩 규칙

#### Null 안전성
- `!!` (non-null assertion) — 프로덕션 코드에서는 사용하지 않는다. 테스트 코드도 대안이 없을 때만
- `requireNotNull()`, `checkNotNull()` 보다 빌트인 non-nullable 메서드 우선
  - `Result`: `getOrThrow()`, `getOrElse { }`, `getOrDefault()`
  - `Map`: `getValue()` (없으면 `NoSuchElementException`)
  - `Collection`: `first()`, `single()`
- `result.getOrNull()!!` — 원래 예외 정보가 손실되고 NPE 로 변환되므로 쓰지 않는다

#### Import 규칙
- FQCN(Fully Qualified Class Name) 대신 import 문 사용. 클래스명 충돌 시 import alias 지정

#### 생성자 주입
- `@Autowired` 대신 생성자 주입만 사용

### Coroutine & Reactive 처리
- `suspend fun` 으로 비동기 함수 선언
- `coroutineScope { }` + `async { }` / `await()` 로 병렬 호출
- `runBlocking` 사용 최소화
- `@Async` 대신 Coroutine 선호

### 코드 포매팅
- JSON 파일 작성/편집 시 pretty-print
- 날짜 필드: 별도 지정 없으면 `YYYY-MM-DD HH:MM:SS` 형식

### 테스트 스타일
- **Kotest**: 스펙 스타일은 레포·모듈마다 다르므로 신규 테스트 작성 전 형제 테스트 파일에서 `rg -o 'FunSpec|DescribeSpec'` 로 실제 스타일을 확인하고 그것을 따른다
- **MockK**: `mockk()`, `every`, `verify`, `slot`, `coEvery`, `coVerify`
- 테스트 네이밍은 한글 허용
