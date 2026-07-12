# Exact-statement gate: blocked

Item: `S56-M-0142-STATEMENT`  
Theorem: `THM-M-0142`  
Base revision: `89c05a4e0beafda9df991a7ef71e7d74f5eb9644`

## Decision

No exact Lean 4 target can be truthfully elaborated from the repository's authoritative source
record. The record supplies only the title "Nakajima geometry", the year 1994, and the gloss
"moduli spaces of quiver representations". The manifest's `已验证` value is explicitly untrusted.
Neither the source record nor the intake identifies a primary-source theorem number, page, exact
wording, or proposition.

The gloss names a family of mathematical objects rather than a claim with a truth value. In
particular, it does not determine:

- a quiver (including orientation, doubled-quiver convention, and possible loops), dimension and
  framing vectors, or base field;
- representation spaces, gauge group and action, moment-map convention, parameter, or stability
  condition;
- whether the quotient is affine, GIT, symplectic, or hyperkahler, and which non-emptiness or
  regularity assumptions apply;
- whether the intended conclusion is a construction, moduli interpretation, dimension formula,
  smoothness/symplectic property, resolution statement, or a representation-theoretic result.

These choices change the domains, binders, hypotheses, and conclusion. Nakajima's 1994 paper is a
plausible discovery source, but it contains multiple constructions and results; its bibliographic
identity does not select one of them. The adjacent target `THM-M-0143`, whose gloss explicitly says
"construction of moduli spaces of quiver representations", also prevents silently treating a
construction statement as the root of this target.

Consequently a canonical human claim, minimal imports, normalized kernel expression, expression
hash, checked alternate encodings, and meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutations cannot be produced. Choosing a convenient quotient theorem,
an abstract predicate, or one result from the candidate paper would broaden or substitute the
target. No Lean declaration, `sorry`, axiom, assumed result field, proxy proposition, or weakened
special case was introduced. The machine state remains `M4`; statement acceptance and theorem
completion are false.

## Pinned environment and search

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. The existing canonical `.lake` artifacts were read only;
no update, build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0142` | 0 | Rank 317, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the Chinese title/gloss and English equivalents | 0 | Found only the underspecified metadata, intake discovery record, and adjacent target; no exact proposition |
| pinned-mathlib `rg` search for `Nakajima`, quiver varieties, and moduli of quiver representations | 1 | No matching source declaration (`rg` exit 1 means no match) |
| repo-local Lean `rg` search for the same terms | 1 | No matching Lean declaration (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` check because an exact target expression does
not exist. Elaborating a newly invented abstract interface would be fake statement evidence rather
than validation of the assigned deliverable.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact numbered
proposition/page, include all definitions and assumptions it references, check relevant errata, and
explain its boundary with `THM-M-0143`. It must freeze the quiver, dimension/framing data, field,
moment map, stability and quotient conventions, all degenerate cases, and the exact conclusion. A
later statement run can then encode and elaborate that claim with minimal pinned imports,
fingerprint the resulting expression, add checked transports, and run structural mutations.

Until that retry condition is met, the assigned phase is not genuinely self-tested to its
completion gate, so no `.stage1-worker-selftest.json` is emitted.
