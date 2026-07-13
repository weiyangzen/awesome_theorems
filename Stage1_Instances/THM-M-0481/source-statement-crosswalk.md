# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:3532-3537` supplies exactly the title `伯特兰假设`, attribution to
Joseph Bertrand, the year 1845, the gloss `n与2n之间必有素数`, importance "high," and status
`已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The statement sentence has SHA-256
`df368dff769cd482316d067701b0cc7cf9cf92258fada1c2e26b157651c77fab`. The record gives no
bibliography, domain, positivity premise, endpoint convention, ordered binders, proof boundary,
correction history, reviewer, or formal declaration.

`Docs/Stage0_Blueprint.md:13190-13215` repeats the gloss while explicitly leaving the target formal
system, foundation, exact definitions and premises, proof route, dependencies, alternate forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

No Joseph Bertrand primary edition, exact 1845 passage, translation, theorem/page locator, proof
source, errata record, immutable source artifact, or independent source review was found in the
repository. The catalog is therefore a discovery source and cannot establish `H0`.

## Clause crosswalk

| Catalog component | Candidate mathematical meaning | Pinned Lean surface | Intake assessment |
|---|---|---|---|
| `n` | a positive natural number | `(n : Nat) (hn0 : n != 0)` | domain and positivity premise are absent from the catalog |
| lower endpoint | the prime is greater than `n` | `n < p` | matches the usual reading of "between," but no source definition is cited |
| upper endpoint | the prime is at most `2n`, or strictly below it under a stronger premise | `p <= 2 * n` | strict versus inclusive wording is unresolved |
| prime witness | there exists a natural prime `p` | `Exists fun p => Nat.Prime p ...` | conventional encoding; exact binder and set/filter alternatives remain open |
| `n = 0` | must be excluded in either common form | explicit `hn0` in the pinned root | missing semantic prerequisite |
| `n = 1` | included only by the half-closed form | witness `p = 2` | decisive boundary for selecting the exact formulation |
| `已验证` | untrusted catalog label | a kernel receipt would be required | no H or M completion credit |

## Pinned Lean discovery anchor

At manifest-pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.NumberTheory.Bertrand` contains:

```text
Nat.exists_prime_lt_and_le_two_mul
  (n : Nat) (hn0 : n != 0) :
  exists p, Nat.Prime p and n < p and p <= 2 * n
```

It also exposes alias `Nat.bertrand`. The current module file has SHA-256
`ca1588962a2c598e0f089bda6ab9fa108e89c3ee479c76bab4914f754508eb26` and git blob
`9e3752f27172341ba6b5d9d22f17a160f5a68b15`. Its module documentation describes the positive,
half-closed theorem and cites Aigner-Ziegler, Tochiori, and Carneiro as proof leads. Those
bibliographic entries are secondary/modern leads and are not a primary Bertrand source crosswalk.

The pinned proof source visibly separates a large-`n` inequality branch from a finite prime-cover
branch. That architecture is discovery information for later audit and obligation-tree work.
`IntakeProbe.lean` only authenticates adjacent declarations and boundaries; it does not declare the
canonical target, inspect terminal proof provenance or transitive trust, or credit `M0-W`.

## Source and statement gates

Before leaving `H1`, accountable reviewers must preserve an immutable approved primary or
authoritative source, give a pinpoint proposition and incorporated definitions, map the domain,
positivity premise, both endpoints, boundary cases, proof and correction history, and independently
approve fidelity to `THM-M-0481`.

Before the statement node can pass, it must choose precisely that source-approved form, minimize
pinned imports, serialize the elaborated expression and environment fingerprints, compile every
credited transport, and mutation-test a removed positivity hypothesis, changed domain, changed
binder scope, and the `n = 0`/`n = 1` boundary behavior. Intake deliberately leaves those fields open.
