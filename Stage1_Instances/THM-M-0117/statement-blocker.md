# Exact-statement gate: blocked

Item: `S56-M-0117-STATEMENT`

Theorem: `THM-M-0117`

Base revision: `69662621a19907de342801b09124e8dfe3495e40` (tree
`fbfbc07e2045accdd0144baf892481a9bb6717f8`).

## Decision

The exact Lean 4 statement cannot truthfully be frozen or elaborated from the
received source record. The repository gives only the family name "Moishezon
theorem," Boris Moishezon, the year 1966, and the gloss "algebraicity of
Moisezon manifolds." It gives no primary publication, theorem/page, exact
domain, definitions, hypotheses, conclusion, errata, or independent source
review. The catalog's `verified` label is explicitly untrusted under rev-5.6.

The intake consequently froze only a provisional conservative interpretation:
every compact complex Moishezon manifold is bimeromorphic to a projective
algebraic variety. Its own README and crosswalk make primary-source
disambiguation a hard prerequisite of this phase. In particular, the sparse
gloss does not select that algebraic-model result over the nearby statement
that a Moishezon manifold is projective under an additional Kahler hypothesis.
It also leaves smoothness, connectedness, irreducibility, dimension-zero and
empty cases, the definition of algebraic dimension, the category of the
algebraic model, analytification, and the direction and strength of the
bimeromorphic comparison open. Choosing any of these now would invent,
strengthen, narrow, or substitute proposition-changing mathematics.

There is also no native target surface in the pinned dependency closure. The
owned `StatementInfrastructure.lean` probe checks the available complex-
manifold, one-variable meromorphic-function, transcendence-degree, scheme,
closed-immersion, properness, and Proj APIs. A bounded source search found no
Moishezon predicate, meromorphic-function field or algebraic-dimension API for
complex manifolds, complex analytic-space/analytification interface, or
bimeromorphism declaration. The five probe imports are therefore not claimed
minimal for a canonical target that does not exist.

The legacy `S1_M_037.lean` module elaborates, but it expressly records a
statement shape rather than the analytic theorem. Its `MoishezonAnalyticData`
stores compactness and dimension equality as arbitrary propositions; its
algebraic model comparison is only a function between carriers; and
`StatementShape` neither represents analytification nor requires a
bimeromorphism. Reusing it would violate the intake's explicit exclusion and
receives no statement or proof credit.

Accordingly the canonical formal expression, minimal imports, expression
fingerprint, checked transports, and all four required mutation classes are
undefined. The gate fails before proof evidence is inspected. Lifecycle stays
`planned`, root debt stays `[H3, M4, R4]`, and both audit and theorem completion
remain false.

The predecessor `S56-M-0117-INTAKE` is also only provisional `[_]`, not
master-accepted `[x]`. Concurrent preparation permits this blocker, but a
future statement transition remains dependency ordered.

## Pinned Environment

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
  tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`.
- The automation-provided canonical `.lake` symlink was used read-only. No
  update, build, clone, fetch, or dependency mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-15 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0117` | 0 | rank 37, planned, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0117/StatementInfrastructure.lean` | 0 | adjacent native APIs elaborated; stdout was 27 lines/2599 bytes with SHA-256 `49e1945f064d3269c83c696067b0d481fe645c97b2b13989952984a5b456394f`; stderr was empty |
| bounded pinned-source searches for Moishezon/Moisezon, algebraic dimension, bimeromorphism, meromorphic-function fields, analytification, and complex analytic spaces | 1 | expected no-match results; no exact target interface was located in the searched pinned surfaces |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_037.lean` | 0 | legacy statement-shape and adjacent wrappers elaborated, but no source-faithful analytic target was established |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short`; `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | dependency worktree clean; pinned revision and tree above |
| `python3 -m json.tool Stage1_Instances/THM-M-0117/statement-blocker.json` plus scoped invariants | pending final run | structured blocker identity, null target/imports/hash, unchanged vector, undefined mutations, false completion fields, and no-self-test boundary |
| prohibited-declaration scan of `StatementInfrastructure.lean` | pending final run | expected no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations |
| whitespace checks over the three new owned artifacts | pending final run | no diagnostics expected |
| `test ! -e .stage1-worker-selftest.json` | pending final run | self-test must remain absent because the exact-statement deliverable did not pass |

## Retry Condition And Status Boundary

An accountable source reviewer must lawfully preserve and hash a complete
primary or approved authoritative source, identify the exact theorem and
incorporated definitions, and independently approve its mapping. The review
must settle the bimeromorphic-model versus Kahler-projectivity ambiguity and
all domain, connectedness, smoothness, irreducibility, dimension, algebraic-
dimension, algebraic-model, analytification, comparison, and boundary
conventions. The required native analytic interfaces must then be pinned or
implemented without encoding the conclusion in assumptions. A later worker
can encode only that approved claim, minimize imports, serialize its
elaborated expression and environment, compile all credited transports, and
run removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations. The intake must receive master acceptance before that transition
can be accepted.

This blocker is the assigned phase's truthful result, not statement completion
or theorem completion. No statement receipt or `.stage1-worker-selftest.json`
is emitted.
