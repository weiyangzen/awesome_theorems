# THM-M-1277 proof-phase recheck at current base

Item: `S56-M-1277-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `46320e01d1897482417e7b0d03a15a5b77ae5275`

Base tree: `2260ad94d18a6662ffc00f47b8955ae3a2a18184`

Worker slot: `36`

## Verdict

`blocked`. The exact frozen Lean target cannot have the requested positive
proof body. A fresh trust-level-zero replay at this base checks the tracked,
placeholder-free countertheorem

```text
Stage1Rev56.THMM1277.not_statement :
  Not Stage1Rev56.THMM1277.Statement
```

The defect is in `SmoothCompactIn`: `ContDiff Real top` elaborates at
mathlib's analytic order `omega`, rather than smooth order `infinity` (the
coerced top of `ENat`). Analytic uniqueness makes every compactly supported
approximant identically zero. The encoded `ZeroBoundarySobolev` predicate then
forces every admitted scalar field to vanish almost everywhere, so every
admissible exponential integral equals `volume Omega` for every exponent. On
the bounded open unit ball, the supercritical clause with
`C = volume Omega` demands `volume Omega < volume Omega`.

This refutes only the frozen formal encoding, not the mathematical
Moser-Trudinger theorem. Editing the statement or proving a corrected theorem
inside this proof item would be an illegal target substitution. No positive
root proof, proof-node receipt, obligation closure, audit completion, or
theorem completion is claimed. The recorded vector remains `[H1, M3, R3]`;
`M5` is only the proposed machine diagnosis for this exact statement
mismatch.

The prerequisite obligation-tree item remains provisional `[_]`, not
master-accepted `[x]`. Its positive architecture is structurally valid but
predates the refutation: the conditional branch composer cannot supply the
false sharpness premise and its root remains open `M3`. Independently, the
statement record lacks a normalized elaborated-expression fingerprint and
mutation tests, while `scope-map.md` conflicts with the formal target about
the nonempty-domain condition.

## Validation

All successful Lean checks read the existing pinned artifacts without
modifying them. No `lake update`, `lake build`, dependency clone/fetch, or
network access was used. The automation-provided untracked `.lake` symlink
makes this nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1277` | 0 | Rank 328; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1277/check_obligation_tree.py` | 0 | `PASS`: 24 obligations, 48 typed edges, denominator `e17739e...f60575`; root open `M3` |
| `lake env lean --trust=0 -t0 --root=../.. ../../Stage1_Instances/THM-M-1277/Statement.lean` from `Formalizations/Lean` | 1 | Environmental failure before elaboration: the pinned `flt-regular` package artifact cannot resolve `HEAD`; no fetch or repair was attempted |
| Fresh direct pinned-Lean trust-zero recipe below | 0 | Statement and proof both elaborated; exact countertheorem observed; all 13 axiom reports were exactly `propext`, `Classical.choice`, and `Quot.sound` |
| Independent read-only proof review and fresh trust-zero replay | 0 | Reproduced the refutation, exact type, axiom reports, and `.olean` hashes |
| `rg -n '\\b(sorry|admit|sorryAx)\\b|^[[:space:]]*(axiom|unsafe)\\b' Stage1_Instances/THM-M-1277 --glob '*.lean'` | 1, expected | No prohibited placeholder, declared axiom, or unsafe declaration |
| Pinned `lean --version`; pinned mathlib commit/tree query | 0 | Lean 4.29.0 commit `98dc76e...fab16740`; mathlib `8a178386...eea95`, tree `bdc39a31...2c19e5c2b` |
| Aggregate blocker-packet invariant, structural, JSON, placeholder, whitespace, and self-test-absence check | 0 | Current-base identities and blocked/open state agree; scoped files are valid and clean; root self-test is absent |

The successful replay copied only `Statement.lean` and `Proof.lean` to a
temporary directory, assembled `LEAN_PATH` from existing package outputs
(excluding the incomplete `flt-regular` artifact), and invoked the pinned Lean
executable with `--trust=0 -t0`. It created no repository output and removed
the temporary directory.

Fresh SHA-256 values were
`6f184999ed81c69800d9f91cd3c969557853b7ff370c05fdd6790cd31de4e65a`
for `Statement.olean`,
`0597c2f2ed998eba1e50fadc0aba30d461226e4bf31a85dc3d3b4560355686db`
for `Proof.olean`,
`593f08c48172c08e242b8073f6550e2d3f100806c26d98d9ddb387dc8a1fb3a8`
for statement output, and
`2f47380b9e5a682199aa7e433ad923111d99b9612a1d9bb3a050fa4f8c10d9c8`
for proof output.

## Retry condition

The first failed gate is exact canonical statement correctness. Reopen
`S56-M-1277-STATEMENT`, replace the analytic order with the intended smooth
order `((top : ENat) : WithTop ENat)`, reconcile the nonempty-domain scope
text, run exact-expression identity and mutation gates, and publish a new
version of the obligation registry, typed graphs, and validation specifications
for the changed fingerprint before another proof attempt.

The remaining root cut set is `S56-M-1277-STATEMENT`. Because the assigned
positive proof phase is not genuinely self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent and the item remains
`[ ]`.
