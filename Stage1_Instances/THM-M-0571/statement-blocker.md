# Statement gate blocker

Item: `S56-M-0571-STATEMENT`  
Theorem: `THM-M-0571`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The accepted intake deliberately leaves `canonical_claim` null and records the first blocker as
primary-source and local-index variant selection. The complete upstream metadata is only the title
"local index theorem" and the gloss "a local formula for the index density". It does not identify a
primary-source theorem/page or select among a local Gauss-Bonnet formula for the de Rham complex, a
Dolbeault/local Riemann-Roch formula, a Dirac-operator formula, a families theorem, or a general
elliptic local Atiyah-Singer theorem. These variants have different manifold and bundle hypotheses,
operators, gradings, characteristic forms, normalizations, and pointwise/asymptotic conclusions.

Choosing one variant here would invent missing mathematics and violate sections 2, 5, and 5.1 of
`Docs/Stage1_Blueprint_rev-5.6.md`. Consequently the exact ordered binders, hypotheses, conclusion,
boundary cases, minimal imports, serialized expression, expression hash, checked transports, and
the required removed-hypothesis/domain/binder-scope/boundary mutations cannot truthfully be
produced. Machine status remains `M4`.

The historical module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_118.lean` does not repair
this identity failure. Its `StatementShape` asserts the existence of a caller-supplied
`LocalIndexTheoremData`; that structure takes the operator type, ellipticity predicate, analytic
index, both densities, integration functional, and the desired local and global formulae as data.
The module itself calls this a statement-shape boundary and says its central analytic and
cohomological objects are abstract. It elaborates in the pinned environment, but it is not a
source-faithful encoding of any selected local index theorem and receives no statement credit.

No `Statement.lean`, opaque proxy predicate, theorem, axiom, `sorry`, or substitute special case was
introduced. The scoped pinned-mathlib search found no source occurrence for the local index theorem,
index density, Atiyah-Singer theorem, Dirac operator, or heat-kernel supertrace. This negative search
is only statement-phase environment evidence, not the downstream anchor audit.

## Environment fingerprint

- Repository base revision: `621e4c254d9e0dc9b50a60e66930c9f43601b890`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Historical discovery module SHA-256:
  `82983a81bd23ca849f1099654257647792b893657fd987df73d96b1b4c2c530c`.

The worker clone uses the existing canonical pinned `.lake` artifacts. The preflight worktree had
only the pre-existing untracked `Formalizations/Lean/.lake` entry. No update, build, fetch, clone, or
dependency mutation command was used.

## Validation evidence

Commands ran from the repository root unless a leading `cd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard passed: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0571` | 0 | Rank 118, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_118.lean` | 0 | Historical abstract boundary elaborated and printed its probes; this is not exact-target evidence |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'Atiyah.Singer\|local index theorem\|index density\|Dirac operator\|heat kernel.*supertrace\|supertrace.*heat kernel' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No matching source occurrence in pinned mathlib (`rg` exit 1 means no match) |

## Retry condition

An accountable source reviewer must select an immutable primary-source edition and exact
theorem/page, including every incorporated definition and any errata. The crosswalk must freeze the
geometric category, dimension/parity, compactness and boundary assumptions, grading and bundles,
operator and ellipticity/Dirac hypotheses, heat-kernel and diagonal-supertrace semantics,
characteristic form and normalization, and convergence/equality mode. A later statement worker can
then encode that exact claim with concrete pinned definitions, minimize imports, fingerprint the
elaborated expression, check transports, and run all four mutation classes.

Until that retry condition is met, statement acceptance, audit completion, and theorem completion
are false. Because this assigned phase is blocked rather than genuinely self-tested to its
completion gate, no `.stage1-worker-selftest.json` is emitted.
