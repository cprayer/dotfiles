---
name: grpc-conventions
description: gRPC/Protobuf 코드 작성 컨벤션 — Kotlin DSL 로 request/response 생성, well-known type(FieldMask/Timestamp) 처리, Enum↔Proto 변환 시 전체 case 명시. proto 파일이나 gRPC 서비스 코드를 작성·수정할 때 사용.
---

# gRPC 서비스 컨벤션

## stub 사용

stub 은 `*Kt.kt` 로 끝나는 파일에서 Kotlin DSL 을 사용해 request / response 를 생성한다.

## Protobuf well-known type

Java Builder 패턴 대신 Kotlin DSL 을 사용한다.

```kotlin
// GOOD
fieldMask { paths.addAll(list) }        // import com.google.protobuf.fieldMask
timestamp { seconds = ... }             // import com.google.protobuf.timestamp

// BAD
FieldMask.newBuilder().addAllPaths(list).build()
```

## Enum ↔ Proto 변환

`else` 를 쓰면 proto 에 새 값이 추가돼도 컴파일 타임에 감지되지 않는다. 모든 필드를 명시적으로 나열하고 `UNRECOGNIZED`, `UNSPECIFIED` 도 명시적으로 처리한다.

```kotlin
// GOOD
fun toProto(): FooProto = when (this) {
    A -> FooProto.A
    B -> FooProto.B
}

fun fromProto(proto: FooProto): Foo = when (proto) {
    FooProto.A -> A
    FooProto.B -> B
    FooProto.UNSPECIFIED, FooProto.UNRECOGNIZED -> DEFAULT
}

// BAD: 새 필드 추가 시 누락 가능
fun fromProto(proto: FooProto): Foo = when (proto) {
    FooProto.A -> A
    else -> DEFAULT
}
```

## proto 이름 변경

proto field/message rename 은 `proto-rename` 스킬을 사용한다. admin proto 와 service proto 는 변경 범위를 독립적으로 판단한다.
