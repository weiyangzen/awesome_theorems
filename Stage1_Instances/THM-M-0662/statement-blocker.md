# Exact-statement gate: blocked

Item: `S56-M-0662-STATEMENT`  
Theorem: `THM-M-0662`  
Base revision: `a74bf62e5952864a45901ffdf9160b000ba3fd01`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is "simple theories" / "classification of simple theories". This
names a branch of model theory, not one proposition, and supplies no ordered binders, hypotheses,
or conclusion. The accepted intake therefore leaves the canonical claim and formal target null.

Choosing a familiar formulation would invent missing mathematics. The label could refer to the
absence of a tree property, an equivalent characterization using dividing or forking, symmetry or
local character of independence, an independence theorem, a rank result, or a classification or
counting theorem under additional hypotheses. These choices differ in the language and theory
assumptions, historical versus modern tree-property convention, parameter and base domains,
saturation and cardinal hypotheses, real versus imaginary sorts, binder order, and conclusion. A
definition of a predicate called `Simple` would also not be a theorem classifying simple theories.

The intake identifies Saharon Shelah's 1980 paper *Simple unstable theories* only as a discovery
anchor. No immutable edition has been preserved and hashed, no exact theorem/page and incorporated
definitions have been selected, no errata have been disposed of, and no independent source review
has approved a crosswalk. Stage0 explicitly leaves precise definitions and prerequisites, proof
process, dependencies, axioms, and machine artifacts to be supplied. Its `已验证` label is untrusted
metadata under rev-5.6. Consequently the phase fails at exact human-claim identity, before minimal
imports, expression fingerprinting, transports, or proposition-changing mutations can be validly
determined. Machine state remains `M4`; statement and theorem completion are false.

## Pinned Lean boundary

`StatementProbe.lean` imports only `Mathlib.ModelTheory.Types` and checks generic first-order
theories, completeness, satisfiability, formulas, complete types, and `typeOf`. Narrow searches of
the pinned `Mathlib/ModelTheory` tree found no simple-theory, tree-property, model-theoretic
dividing/forking, or independence-theorem declaration. This generic substrate cannot encode the
missing source proposition and receives no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing canonical `.lake` artifacts were used
read only. No update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0662` | 0 | rank 706, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8a...b1d2` and `321626...2d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision recorded above |
| repository `rg` search for the theorem ID, Chinese/English labels, source title, tree property, forking, dividing, and independence theorem | 0 | only underspecified metadata, the intake dossier, and unrelated material; no exact root proposition |
| pinned-mathlib `rg` search for simple theories, tree property, model-theoretic dividing/forking, and independence theorem | 1 | no matching declaration (`rg` exit 1 means no match) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0662/StatementProbe.lean` | 0 | elaborated only the six generic model-theory substrate checks |
| `python3 -m json.tool Stage1_Instances/THM-M-0662/statement-blocker.json` | 0 | blocker JSON is syntactically valid |
| `git diff --check -- Stage1_Instances/THM-M-0662` | 0 | no whitespace errors |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary-source edition, select
and transcribe one exact theorem with all incorporated definitions and assumptions, dispose of
errata, and independently approve the mapping. A later statement worker can then encode that same
claim with real Lean definitions, minimize pinned imports, serialize and hash the elaborated
expression, check alternate transports, and run all required statement mutations.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
