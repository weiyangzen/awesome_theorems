# Exact-statement gate: blocked

Item: `S56-M-1202-STATEMENT`  
Theorem: `THM-M-1202`  
Base revision: `446f3e80e7a93deeca70150fa80d9ee079ee0586`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the title "Lax entropy condition," Peter Lax, the year 1957, and the
gloss "entropy condition for shocks." The intake identifies Lax's *Hyperbolic Systems of
Conservation Laws II* (CPAM 10 (1957), 537-566, DOI `10.1002/cpa.3160100406`) as a discovery
candidate, but it deliberately records that no exact page, displayed formula, source convention,
or errata review has been inspected and accepted.

The intake's narrow classical-shock scope still leaves proposition-changing choices open:

- the state space and regularity of the flux, and the precise strict-hyperbolicity assumptions;
- increasing or decreasing eigenvalue order and the characteristic-family index type;
- the orientation of left and right traces and the sign convention for shock speed;
- whether Rankine-Hugoniot compatibility is a premise, part of a defined `k`-shock, or part of the
  conclusion;
- whether the canonical claim is only
  `lambda_k(u_R) < s ∧ s < lambda_k(u_L)`, includes adjacent-family inequalities, or asserts the
  incoming-characteristic count;
- the endpoint clauses for the first and last characteristic families; and
- whether the source passage is a definition/admissibility criterion or a necessity,
  sufficiency, equivalence, existence, or uniqueness theorem.

These alternatives are not interchangeable statements. In particular, treating the provisional
core inequality in `intake.json` as canonical would ignore its explicitly unresolved source
orientation and would not determine the adjacent-family or endpoint clauses. Encoding an abstract
record whose fields assume the desired inequalities would likewise replace the mathematical claim
with an interface. Either approach would manufacture statement evidence.

The repository separately schedules the Rankine-Hugoniot condition (`THM-M-1200`), the general
entropy condition (`THM-M-1201`), Oleinik's scalar condition (`THM-M-1203`), and Kruzkov's theorem
(`THM-M-1204`). Substituting any of those, or silently combining them with this target, would
broaden or duplicate the assigned theorem.

The first failed gate is rev-5.6 section 5 canonical human-claim identity. It fails before minimal
imports, fixed binders and universes, an elaborated-expression hash, checked alternate transports,
or meaningful removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations can be
produced. No Lean declaration, axiom, placeholder, assumed admissibility predicate, weakened
special case, or broadened theorem was introduced. Machine debt remains `M4`; statement acceptance
and theorem completion are false.

## Pinned environment and scoped checks

Commands were run in this worker clone on 2026-07-12 (Asia/Shanghai). The existing canonical
`.lake` artifacts were used read-only through the worker link. No update, build, dependency clone,
fetch, or other dependency mutation was run.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1202` | 0 | Rank 396, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the title, English gloss, candidate paper, and DOI | 0 | Found only the terse catalogue metadata and generated projections; no exact reviewed proposition outside this intake |
| pinned-mathlib `rg` search for Lax shocks, Rankine-Hugoniot, conservation laws, shock waves, hyperbolic systems, and entropy conditions | 1 | No matching theorem-specific API (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` elaboration command because no exact
expression exists. Elaborating one freely selected convention would be fake evidence rather than
the assigned exact-statement deliverable.

## Retry condition

An accountable source review must pin and hash an immutable edition of the 1957 paper, identify the
exact page and formula or proposition, inspect corrections and errata, and freeze every state-space,
flux, hyperbolicity, eigenvalue-order, family-index, trace-orientation, speed-sign, jump-condition,
quantifier, conclusion, and endpoint choice listed above. It must also decide which provisional
alternate formulation is canonical and which directions between formulations are actually
credited. A later statement run can then encode that exact claim, minimize pinned imports,
serialize and hash its elaboration and environment, compile checked transports, and execute all
four required mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
