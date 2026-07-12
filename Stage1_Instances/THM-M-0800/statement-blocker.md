# Exact-statement gate: blocked

Item: `S56-M-0800-STATEMENT`  
Theorem: `THM-M-0800`  
Worker base revision: `8f8873f36acbc62e9b41b932a8bb65bf355c8ccf`

## Gate decision

The repository does not contain an exact mathematical proposition that can be truthfully
elaborated as the canonical Lean 4 target. Its statement-bearing metadata consists only of the
topic `Ramsey cardinal` / `拉姆齐基数` and the phrase `拉姆齐基数的性质` ("properties of Ramsey
cardinals"). Stage0 explicitly leaves the exact definition, premises, proof, dependencies, logical
foundation, and machine-checked artifact open.

This wording does not choose even the defining partition convention. Compatible readings quantify
over all finite subsets simultaneously or separately over each finite arity; use two, finitely
many, or countably many colors; and require one common homogeneous set or an arity-dependent set.
It also does not say which "property" is the conclusion. Regularity, inaccessibility,
indescribability, a partition characterization, and a model-theoretic characterization would be
different theorem roots. Choosing any one of them would invent or substitute mathematics.

Consequently the ordered binders, hypotheses, conclusion, universe representation, zero-arity and
small-cardinal boundaries, and canonical expression are all unresolved. There is no expression to
serialize or hash and no sound removed-hypothesis, changed-domain, changed-binder-scope, or boundary
mutation test. The rev-5.6 section 5 intake contract and section 5.1 Lean statement gate therefore
fail before proof evidence may be inspected.

## Pinned Lean boundary

The accepted intake's `IntakeProbe.lean` imports only
`Mathlib.Data.Set.PowersetCard` and `Mathlib.SetTheory.Cardinal.Cofinality`. It checks five nearby
encoding APIs. Re-elaboration proves that the pinned environment is usable; it does not define a
Ramsey cardinal, select a partition convention, state a property, or receive statement/proof
credit. No `sorry`, `admit`, or `axiom` occurs in the target's Lean source.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing canonical `.lake` link and artifacts were
used read-only. No update, build, dependency clone, or fetch was run.

## Exact validation record

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0800` | 0 | rank 804, planned, legacy artifacts unaccepted, theorem incomplete |
| repository `rg` search for the theorem ID and Chinese/English names | 0 | only the ambiguous inventory metadata, Stage0 open fields, manifest entry, and this dossier were found |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions above |
| `(cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json)` | 0 | hashes `651c8a...1d2` and `321626...d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0800/IntakeProbe.lean)` | 0 | all five substrate API checks elaborated; no canonical target asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0800 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `python3 -m json.tool Stage1_Instances/THM-M-0800/instance.json` | 0 | intake JSON is syntactically valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0800/task-dag.json` | 0 | task DAG JSON is syntactically valid |

## Retry condition and status boundary

An accountable source reviewer must preserve and hash an immutable statement-bearing source,
select and transcribe one exact proposition with all incorporated definitions, notation,
assumptions, and boundary conventions, audit errata, and independently approve its mapping to this
repository entry. A later statement run can then encode that same claim, minimize imports,
fingerprint the elaborated expression, check alternate transports, and execute all four required
mutation classes.

This is the first failed gate. The statement node remains `[ ]`, the root remains
`[H3, M4, R4]`, and `audit_complete` and `theorem_complete` remain false. No worker self-test
manifest is emitted because the assigned statement deliverable did not pass its gate.
