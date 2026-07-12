# Exact-statement gate: blocked

Item: `S56-M-0192-STATEMENT`  
Theorem: `THM-M-0192`  
Base revision: `84f6634930ba233d7af5d4bce1b8b102c849e30e`

## Decision

The exact Lean 4 target cannot yet be truthfully elaborated. The accepted intake identifies the
intended result as Deligne's smooth-projective weight/Riemann-hypothesis theorem in *La conjecture
de Weil. I* (1974), customarily cited as Theorem 1.6, but deliberately records that citation as
discovery evidence. It leaves the exact French transcription, ordered quantifiers, arithmetic or
geometric Frobenius, eigenvalue versus reciprocal-root convention, connectedness, coefficient
field, embeddings, and boundary cases for this phase. The primary-source PDF could not be fully
retrieved during this run, and there is no immutable, independently reviewed transcription in the
repository. Filling those choices from memory would not meet the exact-source gate.

There is a second, independent semantic blocker in the pinned Lean environment. Mathlib defines
`Scheme.EllAdicCohomology` as the pro-etale cohomology group `H^i(X, Z_l)` and provides smooth and
proper scheme-morphism predicates. The module itself says comparison with classical etale
cohomology is future work. Narrow searches found no rational ell-adic cohomology representation,
Frobenius action on it, characteristic polynomial or eigenvalue interface for that action, or
Deligne weight predicate. Thus the precise conclusion cannot even be typed using the currently
pinned domain API.

Introducing an abstract structure carrying a Frobenius action, eigenvalues, or purity conclusion
as unconstrained fields would erase the theorem's geometric content or assume the desired result
under another name. It would be a substituted target, which the scope map expressly excludes. No
such interface, axiom, placeholder, weakened special case, or broadened theorem was introduced.
Machine state remains `M4`; statement and theorem completion are false.

## Pinned Lean boundary

`StatementProbe.lean` uses the narrow available modules and checks only `Scheme`, `Smooth`,
`IsProper`, and `Scheme.EllAdicCohomology`. It is feasibility evidence, not the canonical target,
and receives no statement or proof credit. The existing canonical `.lake` artifacts were read
only; no update, build, clone, fetch, or dependency mutation was performed.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Validation evidence

Commands ran inside this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0192` | 0 | rank 678, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0192/StatementProbe.lean` | 0 | elaborated the four available substrate checks |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8a...b1d2` and `321626...2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| pinned-mathlib `rg` search for ell-adic cohomology and Frobenius/weight/eigenvalue APIs | 0/1 | found the integral cohomology definition but no target-level Frobenius weight surface; exit 1 on the narrow missing-API searches means no match |
| `python3 -m json.tool Stage1_Instances/THM-M-0192/statement-blocker.json` | 0 | blocker JSON is syntactically valid |
| `git diff --check -- Stage1_Instances/THM-M-0192` | 0 | no whitespace errors |

## Retry condition

An accountable reviewer must preserve and hash an immutable primary-source edition, transcribe the
exact result and incorporated definitions, settle the conventions above, audit errata, and obtain
independent approval. A pinned Lean dependency must also provide, or the repository must first
implement, the semantic Frobenius-on-rational-ell-adic-cohomology interface. Only then can a later
statement run encode the exact claim, minimize imports, print and hash its expression, check
alternate transports, and perform hypothesis/domain/binder/boundary mutations.

This is the first failed gate, not completion of the statement node or a later node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
