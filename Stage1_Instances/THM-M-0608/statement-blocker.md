# Exact-statement gate: blocked

Item: `S56-M-0608-STATEMENT`  
Theorem: `THM-M-0608`  
Base revision: `99f4faa83aef7915bf92b30fe214fdfc98ec26ae`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is "Seiberg-Witten invariants" / "invariants of four-manifolds". The
accepted intake correctly records that this names a theory and family of invariants, not one
proposition, and leaves both the primary-source statement and theorem variant unselected.

Choosing a familiar formulation would invent missing mathematics. The label could mean construction
and well-definedness of an invariant, metric/perturbation independence of a zero-dimensional count
when `b2+ > 1`, chamber dependence and wall crossing when `b2+ = 1`, a vanishing/nonvanishing result,
or a four-manifold application. These roots differ in their manifold and Spin-c assumptions,
expected dimension, reducible solutions, regularity, orientation, chamber data, codomain, ordered
binders, and conclusion. None can be silently substituted for the metadata label.

The discovery source recorded at intake, Edward Witten's *Monopoles and Four-Manifolds*, has not
been accepted at the granularity of an immutable edition, pinpoint statement, incorporated
definitions, assumptions, conventions, errata, and independent source review. The Seiberg-Witten
physics paper recorded there also does not itself select one rigorous four-manifold invariance
theorem. Consequently there is no canonical human claim from which to derive minimal imports, an
elaborated expression fingerprint, checked transports, or meaningful removed-hypothesis,
changed-domain, binder-scope, and boundary mutations. Machine state remains `M4`; statement and
theorem completion are false.

## Pinned Lean boundary

`StatementProbe.lean` imports only `Mathlib.LinearAlgebra.CliffordAlgebra.SpinGroup` and checks the
algebraic `lipschitzGroup`, `pinGroup`, `spinGroup`, and `spinGroup.toUnits` declarations. This is
the closest name-specific substrate found in the pinned environment, but it is not a Spin-c
structure on a smooth four-manifold and supplies none of the gauge-theoretic objects above. Narrow
mathlib searches found no Seiberg-Witten invariant, monopole equation, four-manifold Spin-c, or
gauge-theoretic moduli-space API. The probe is therefore only feasibility evidence and receives no
statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing canonical `.lake` artifacts were read
only; no update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0608` | 0 | rank 645, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| repository `rg` search for the theorem ID, Chinese/English names, and source title | 0 | only underspecified metadata, intake discovery material, separately owned related targets, and an explicit missing-package note; no exact proposition |
| pinned-mathlib `rg` search for Seiberg-Witten, Spin-c, monopole equations, gauge groups, and four-manifold moduli spaces | 1 | no matching gauge-theory API (`rg` exit 1 means no match) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0608/StatementProbe.lean` | 0 | elaborated the four algebraic spin-group substrate checks |
| `python3 -m json.tool Stage1_Instances/THM-M-0608/statement-blocker.json` | 0 | blocker JSON is syntactically valid |
| `git diff --check -- Stage1_Instances/THM-M-0608` | 0 | no whitespace errors |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary-source edition, select
and transcribe one exact theorem with all incorporated definitions and assumptions, dispose of
errata, and independently approve the mapping. A later statement worker can then encode that same
claim with real Lean definitions, minimize pinned imports, serialize and hash the elaborated
expression, check alternate transports, and run all four statement mutations.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
