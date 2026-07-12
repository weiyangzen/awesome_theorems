# Exact-statement gate: blocked

Item: `S56-M-0383-STATEMENT`  
Theorem: `THM-M-0383`  
Worker base revision: `562c428c3d520ab42bba305174b7cad9409d7c0b`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is the label `Bourgain限制性定理`, the attribution Jean Bourgain, the
year 1991, and the gloss `高维Fourier限制性定理` ("higher-dimensional Fourier restriction
theorem"). The two occurrences in `Docs/researches/math_theorems.md` are identical inventory rows,
not independent sources. `Docs/Stage0_Blueprint.md` repeats the gloss while leaving definitions,
hypotheses, proof route, and formal artifacts open.

Those words describe a family of inequivalent results rather than one proposition. They do not
select:

- a continuous restriction estimate, its dual extension estimate, or a discrete exponential-sum
  result;
- the ambient dimension, hypersurface, curvature assumptions, and surface measure;
- the Fourier-transform normalization and scalar field;
- the input and output spaces, exponent range, endpoints, or representative/trace convention;
- a global or scale-local estimate, the radius dependence, an epsilon loss, or uniformity of the
  constant;
- the exact 1991 publication, theorem/equation number, page, version, or errata disposition.

Each choice changes the domains, ordered binders, hypotheses, conclusion, or boundary cases.
Selecting a standard sphere/paraboloid/cone formulation, an adjoint formulation, or a historically
plausible exponent improvement would therefore invent or substitute mathematics. Consequently
there is no canonical expression to serialize or hash, no justified minimal import set, no checked
alternate transport, and no sound removed-hypothesis, changed-domain, changed-binder-scope, or
boundary mutation. The rev-5.6 section 5.1 statement gate fails before proof evidence may be
inspected. Machine state remains `M4`; statement acceptance and theorem completion are false.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports five candidate infrastructure modules and checks the
Euclidean Fourier transform, the `L^2` Fourier transform isometry, `MemLp`, `eLpNorm`, metric
spheres, and measure restriction. Re-elaboration confirms that these APIs exist in the pinned
environment. They neither define a canonical hypersurface measure or trace convention nor assert
a Bourgain restriction estimate, so the probe receives no statement or proof credit. A narrow
pinned-mathlib name/text search found no Bourgain or Fourier-restriction theorem declaration; this
is only a bounded environment assessment, not the later formal-anchor audit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. Existing canonical `.lake`
artifacts were reused read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0383` | 0 | rank 871, planned, legacy artifacts unaccepted, theorem incomplete |
| repository `rg` search for the theorem ID, Chinese label/gloss, and English restriction wording | 0 | only duplicated underspecified inventory metadata, the open Stage0 row, and this intake dossier were found; no exact proposition or primary-source pinpoint |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision above |
| pinned-mathlib `rg` search for Bourgain/Fourier restriction and restriction/extension estimates | 1 | no theorem-specific declaration found (`rg` exit 1 means no match) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0383/IntakeProbe.lean` | 0 | all six nearby API checks elaborated; no canonical target asserted |

## Retry condition and status boundary

An accountable source reviewer must preserve and hash an immutable primary-source edition, select
and transcribe one exact theorem with its incorporated definitions and assumptions, dispose of
errata and endpoint qualifications, and independently approve the mapping. The source freeze must
fix every dimension, hypersurface/measure, Fourier normalization, function space, exponent,
constant, scale, quantifier, and degenerate case listed above. A later statement worker can then
encode that same claim, minimize pinned imports, serialize and fingerprint the elaborated
expression, check all credited transports, and execute all four required mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The root
remains `[H3, M4, R4]` with `audit_complete: false` and `theorem_complete: false`. The assigned
phase is not genuinely self-tested to its completion gate, so no `.stage1-worker-selftest.json` is
emitted.
