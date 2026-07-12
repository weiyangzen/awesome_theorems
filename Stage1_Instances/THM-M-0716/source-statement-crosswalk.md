# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `递归函数`, attributes it to Kurt Gödel, gives
the year 1931, and states only `原始递归函数与部分递归函数` ("primitive recursive functions and
partial recursive functions"). Stage0 repeats that metadata and explicitly leaves precise
definitions, assumptions, proof process, dependencies, axioms, and machine artifact open. The
rev-5.6 manifest preserves `已验证` only as `source_status_untrusted`.

The conjunction-like phrase has no verb or mathematical relation. It therefore cannot determine a
Lean proposition, even though it identifies a computability-theory neighborhood.

## Candidate source work

The Gödel attribution and year are discovery hints, not an accepted primary citation. The source
audit must locate an immutable edition and exact theorem or definition passage, record its page or
number, terminology, assumptions, proof boundary, translation, and errata, and obtain independent
review. In particular, it must not infer from the metadata whether the intended historical object
is primitive recursion, general recursion, partial recursion, or a later inclusion/strictness
result.

## Crosswalk

| Repository phrase | Possible mathematical component | Pinned Lean component | Intake status |
|---|---|---|---|
| "primitive recursive functions" | unary natural-number class or encoded functions on suitable types | `Nat.Primrec`, `Primrec` | APIs probed; exact domain open |
| "partial recursive functions" | partial maps closed under composition, recursion, and minimization | `Nat.Partrec`, `Partrec` | APIs probed; terminology and domain open |
| relation between the classes | inclusion after total-to-partial coercion | `Primrec.to_comp`, `Computable.partrec` | available candidate, not selected target |
| relation between the classes | strict inclusion or a characterization | source-specific proposition | absent from repository record |
| `已验证` | untrusted inventory label | no Lean proposition or proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded probe imports
`Mathlib.Computability.Partrec` and checks `Nat.Primrec`, `Primrec`, `Nat.Partrec`, `Partrec`,
`Computable`, `Primrec.to_comp`, and `Computable.partrec`. This confirms that candidate encoding
ingredients exist. It does not select a source meaning, establish exact statement identity, or
credit any theorem closure. A later anchor audit must separately inspect proof provenance and the
full pinned dependency closure after the statement is frozen.
