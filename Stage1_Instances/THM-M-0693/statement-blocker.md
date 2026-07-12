# Exact-statement gate: blocked

Item: `S56-M-0693-STATEMENT`  
Theorem: `THM-M-0693`  
Base revision: `6d9089613f4343925b2ff1ec1a221f0575a93b5f`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record names `相继式演算` (sequent calculus) and supplies only the gloss `证明的形式系统` ("a
formal system of proof"). The related classification note displays the schema `Gamma |- Delta`
and informal identity, cut, and left/right rule examples. These describe a family of proof systems;
they do not state a proposition.

The missing choices are mathematically material. The record does not select propositional or
first-order syntax, classical LK or intuitionistic LJ, one-sided or two-sided sequents, single or
multiple conclusions, or list/multiset/set contexts. It does not give a complete structural and
logical rule set, exchange and multiplicity conventions, quantifier eigenvariable conditions, or
the status of cut. Even after choosing a calculus, it does not choose a truth-valued root such as
soundness, completeness, consistency, admissibility, decidability, or equivalence with another
system. The separately scheduled `THM-M-0692` owns the generic cut-elimination label.

Selecting any one of those calculi or metatheorems would invent or substitute mathematics. An
inductive declaration of a convenient calculus would elaborate only a definition, not the absent
theorem. Consequently there is no canonical human claim, Lean expression, or expression hash, and
no sound removed-hypothesis, changed-domain, binder-scope, or boundary mutation test. The rev-5.6
Lean statement gate fails before proof evidence may be inspected. Machine state remains `M4`;
statement acceptance and theorem completion are false.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports only `Mathlib.ModelTheory.Syntax` and checks generic
first-order language, bounded-formula, theory, list, and membership APIs. It elaborates in the
pinned environment, showing that the toolchain is usable and that some possible encoding
ingredients exist. It is not a sequent calculus or metatheorem and receives no statement or proof
credit. A narrow pinned-mathlib name search found no theorem-specific sequent-calculus, Gentzen,
cut-elimination, LK, or LJ declaration; incidental local identifiers named `LK` or `LJ` were
unrelated.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The existing canonical `.lake` artifacts were used
read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0693` | 0 | rank 734; planned; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| repository `rg` search for the theorem ID, Chinese/English names, and source gloss | 0 | found only the topic/gloss, informal rule description, adjacent cut-elimination material, and intake dossier; no target-local proposition |
| pinned-mathlib `rg` search for sequent calculus, Gentzen, cut elimination, LK, and LJ | 0 | only unrelated substring/local-identifier matches; no theorem-specific calculus module or declaration |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0693/IntakeProbe.lean` | 0 | the five generic syntax/context API checks elaborated; no canonical theorem asserted |
| `python3 -m json.tool Stage1_Instances/THM-M-0693/instance.json` | 0 | intake JSON is syntactically valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0693/task-dag.json` | 0 | task DAG JSON is syntactically valid |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0693 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary-source edition, select
and transcribe one exact proposition, fix the object logic and complete calculus with all side
conditions and boundary cases, dispose of errata, and independently approve the source mapping.
Only then can a later statement run choose minimal pinned imports, elaborate and fingerprint that
same claim, compile checked transports, and execute all four required mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The root
remains `[H3, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`. The assigned
phase is not genuinely self-tested to its completion gate, so no `.stage1-worker-selftest.json` is
emitted.
