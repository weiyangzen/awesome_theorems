# Exact-statement gate: blocked

Item: `S56-M-0614-STATEMENT`  
Theorem: `THM-M-0614`  
Base revision: `6930a74babf81271621795a2d247c6a48f1c432e`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record names "Taubes's theorem" and glosses it only as "Seiberg-Witten and Gromov invariants". The
accepted intake correctly identifies the intended family as Taubes's `SW=Gr` result, but explicitly
does not select a precise primary-source theorem or freeze its conventions.

That missing detail changes the proposition. A faithful root must distinguish the full comparison
from `SW => Gr` and `Gr => SW`, and must fix the smooth, closed, oriented symplectic four-manifold
hypotheses; `b2+` and chamber behavior; Spin-c, Chern-class and Poincare-duality indexing; expected
dimension and orientations; and the Gromov invariant's exceptional-sphere, torus, sign, point, and
multiple-cover conventions. Replacing this with canonical-class nonvanishing or with an equality of
two abstract functions would be a broadened or substituted theorem.

The discovery papers listed by the intake have not been accepted at the granularity of an immutable
edition, pinpoint statement, all incorporated definitions, the direction-specific source chain,
errata, and independent review. Consequently there is no canonical human statement from which to
derive ordered binders, minimal imports, an expression fingerprint, checked transports, or
meaningful hypothesis/domain/scope/boundary mutations. Machine state remains `M4`; statement and
theorem completion are false.

## Pinned Lean boundary

`StatementProbe.lean` imports only `Mathlib.Geometry.Manifold.Instances.Sphere` and checks general
smooth-manifold declarations. This is merely the closest reusable substrate found in the pinned
environment: it defines neither a symplectic four-manifold nor a Spin-c structure, Seiberg-Witten
invariant, Taubes Gromov invariant, pseudoholomorphic-current count, or comparison theorem. Narrow
mathlib searches found none of those APIs. The probe therefore receives no statement or proof
credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Existing canonical `.lake` artifacts were read only;
no update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0614` | 0 | rank 650, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| repository search for the theorem ID, names, comparison terms, and source titles | 0 | only underspecified metadata, intake anchors, and separately owned related-target notes; no exact proposition |
| pinned-mathlib `rg` search for Taubes, Seiberg-Witten, Gromov invariant, Spin-c, monopole equations, and pseudoholomorphic terms | 1 | no matching comparison or gauge-theory API (`rg` exit 1 means no match) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0614/StatementProbe.lean` | 0 | elaborated the three general smooth-manifold substrate checks |
| `python3 -m json.tool Stage1_Instances/THM-M-0614/statement-blocker.json` | 0 | blocker JSON is syntactically valid |
| `git diff --check -- Stage1_Instances/THM-M-0614` | 0 | no whitespace errors |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary-source edition, select
and transcribe the exact comparison theorem with all incorporated definitions and assumptions,
crosswalk every direction-specific paper, dispose of errata, and independently approve the mapping.
A later statement worker can then define or integrate the necessary formal objects, encode the same
claim, minimize pinned imports, serialize and hash the elaborated expression, check alternate
transports, and run all required statement mutations.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
