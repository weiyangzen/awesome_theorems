# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records `陈景润定理`, attributes it to Jingrun Chen, gives 1973,
and states only that every sufficiently large even number is a sum of a prime and an almost prime.
Stage0 repeats the gloss while leaving exact definitions, premises, proof history, axioms, and
formal artifacts open. The rev-5.6 manifest preserves `已验证` only as an untrusted source label.

The record supplies no paper title, edition, theorem number, page, definition of almost prime,
translation, errata, or formal declaration. Thus it locates a famous theorem family but is not an
`H0` source crosswalk.

## Primary-source work required

Chen Jingrun's 1973 publication is the expected historical source locator, but this intake does not
claim an inspected bibliographic edition or pinpoint theorem. The source audit must acquire an
immutable scan or edition, record its complete citation and exact theorem/page, translate the
statement, map all assumptions and definitions, check corrections or errata, and obtain independent
review. A modern authoritative source may clarify notation but cannot silently replace the primary
statement.

## Crosswalk

| Repository phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "sufficiently large" | existence of a threshold beyond which the assertion holds | `exists N0, forall N, N0 <= N -> ...` or checked eventual form | shape identified; source wording open |
| "even number" | positive even integer/natural | `Even N` or divisibility by two | API routine; domain and boundary open |
| "prime" | one prime natural summand | `Nat.Prime p` | pinned API probed |
| "almost prime" | expected `P_2`, at most two prime factors counted with multiplicity | `Nat.factorization`, support, and exponent sum, or checked product encoding | convention not source-frozen |
| "sum" | additive representation of the even number | witnesses `p a` and equality `N = p + a` | equality orientation and positivity open |
| 1973 / Jingrun Chen | historical locator | immutable source revision and source-to-binder map | locator only |
| `已验证` | untrusted inventory label | no proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe checks `Nat.Prime`, `Nat.factorization`, finite support cardinality, and eventual
quantification. These are statement ingredients only. Cardinality of factorization support counts
distinct prime divisors and is not by itself the multiplicity-counting `P_2` predicate, so it must
not be used without a source-approved definition and a checked bridge. A bounded local text search
found factorization infrastructure but no target-specific Chen theorem; the formal anchor audit is
a later phase and no global absence claim is made.

