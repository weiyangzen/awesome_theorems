# Exact-statement gate: blocked

Item: `S56-M-0610-STATEMENT`  
Theorem: `THM-M-0610`  
Base revision: `6930a74babf81271621795a2d247c6a48f1c432e`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
complete mathematical wording is "instanton Floer homology" / "an invariant of three-dimensional
manifolds". That names a theory, not one proposition. The intake proposes the historically
conservative root of well-definedness and orientation-preserving diffeomorphism invariance for
closed oriented integral homology 3-spheres, but explicitly leaves this interpretation subject to
pinpoint primary-source audit.

The proposed root still does not select the bundle and gauge group, treatment of reducibles,
coefficient ring, relative grading, allowed metrics and perturbations, or whether independence and
invariance produce equality, canonical isomorphism, graded isomorphism, chain-homotopy equivalence,
or functoriality. Later admissible-bundle, framed, singular, and equivariant variants have different
domains and conclusions. Choosing among these branches would invent missing mathematics; declaring
an abstract invariant as input would assume rather than formalize the claim.

Floer's 1988 paper is only a discovery citation in the intake. This dossier has no accepted
immutable edition, pinpoint result, definition and premise crosswalk, corrections review, or
independent source approval. Consequently there is no canonical claim from which to derive ordered
binders, minimal imports, an elaborated expression fingerprint, checked transports, or meaningful
removed-hypothesis, changed-domain, binder-scope, and boundary mutations. Machine state remains
`M4`; statement and theorem completion are false.

## Pinned Lean boundary

`StatementProbe.lean` imports only `Mathlib.Geometry.Manifold.Diffeomorph` and checks mathlib's
general `Diffeomorph`, `Diffeomorph.refl`, and `Diffeomorph.trans` declarations. Narrow searches of
the pinned mathlib tree found no instanton Floer homology, instanton moduli-space, gauge-theoretic
chain complex, or integral-homology-sphere API. The probe is therefore only a checked boundary on
available smooth-manifold substrate. It is not the canonical target and receives no statement or
proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Existing canonical `.lake` artifacts were used read
only; no update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0610` | 0 | rank 647, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes recorded in `statement-blocker.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| repository search for the theorem ID, Chinese/English names, and source phrase | 0 | only underspecified metadata and intake discovery material; no exact proposition |
| pinned-mathlib search for instanton Floer, instantons, gauge groups, and homology spheres | 1 | no matching theory API; exit 1 is ripgrep's no-match result |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0610/StatementProbe.lean` | 0 | all three substrate declarations elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0610/statement-blocker.json` | 0 | structured blocker is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0610` | 0 | no whitespace errors |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary-source edition, select
and transcribe one exact result with all incorporated definitions and assumptions, dispose of
corrections, and independently approve the mapping. A later statement worker can then encode that
same claim with real Lean definitions, minimize pinned imports, serialize and hash the elaborated
expression, check alternate transports, and run all four statement mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
