# Statement-phase blocker

Item: `S56-M-0705-STATEMENT`  
Theorem: `THM-M-0705`  
Worker base revision: `f4c286c4ebc4a8b1a5d0a746afd6fba9849e4c7c`

## Gate decision

The exact Lean 4 target cannot be elaborated truthfully from the repository source record. The
only theorem wording is `lambda calculus confluence` (`lambda calculus` is written with the lambda
symbol in the source files). Stage0 explicitly leaves the precise definitions and premises open.
The record supplies no immutable source passage, calculus grammar, variable/binding convention,
alpha-equivalence policy, substitution definition, reduction rules, closure convention, ordered
binders, or boundary policy.

Several inequivalent propositions remain consistent with that wording:

1. confluence of compatible one-step beta reduction after reflexive-transitive closure;
2. the Church-Rosser common-reduct property for beta convertibility;
3. either of those statements for beta-eta rather than beta reduction.

Even after choosing beta confluence, raw named terms modulo alpha-equivalence, de Bruijn terms, and
other binding encodings produce distinct formal domains whose correspondence needs checked
transport. Open terms versus closed terms is also unresolved. Selecting any one of these choices
without a source freeze would invent missing mathematics and could silently substitute a narrower
or different theorem.

Consequently there is no canonical Lean expression to serialize or hash, no source-mapped alternate
encoding to transport, and no sound set of removed-hypothesis, changed-domain, changed-binder-scope,
and boundary mutations. The rev-5.6 section 5 and 5.1 statement gate therefore fails before proof or
anchor evidence may be inspected. In particular, replacing the target with confluence of an
arbitrary relation, or assuming beta confluence as a hypothesis, is expressly rejected.

## Pinned environment probe

`IntakeProbe.lean` has the single direct import `Mathlib.Logic.Relation`. It was re-elaborated only
to distinguish an available pinned Lean environment from the absent lambda-calculus specification.
The probe confirms `Relation.ReflTransGen`, `Relation.Join`, and the generic sufficient-condition
theorem `Relation.church_rosser`; none defines lambda terms or beta reduction, and none is the target
of this item. The probe receives no statement or proof credit.

## Exact validation record

Validation date: `2026-07-12` (`Asia/Shanghai`). Commands ran in this worker clone. Lean commands
used the pre-existing pinned Lake environment read-only. No update, build, dependency fetch, clone,
or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0705` | 0 | rank 746; planned; legacy artifacts unaccepted; theorem_complete false |
| `rg -n -i 'THM-M-0705|Church.?Rosser|lambda calculus confluence' Docs/researches/math_theorems.md Docs/researches/cs_theorems.md Docs/Stage0_Blueprint.md Stage1_Instances/THM-M-0705` | 0 | only the terse confluence gloss, open Stage0 fields, and intake records were found; no exact source passage was present |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0705/IntakeProbe.lean)` | 0 | six generic relation APIs elaborated; no lambda-calculus proposition was asserted |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-0705/IntakeProbe.lean` | 0 | hashes `651c8acc...b1d2`, `321626c8...2d81`, and `ff8a3a4c...cc6b5` |
| `python3 -m json.tool Stage1_Instances/THM-M-0705/instance.json` | 0 | intake record is valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0705/task-dag.json` | 0 | open task DAG is valid JSON |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0705 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom was found |
| `git diff --check -- Stage1_Instances/THM-M-0705` | 0 | no whitespace errors |

## Required unblocker and status boundary

The first unblocker is an immutable, independently inspected source passage selecting one exact
Church-Rosser proposition. It must fix the term and binding representation, alpha-equivalence and
substitution policy, beta versus beta-eta rules, one-step and closure operators, domains, ordered
binders, and zero-step/open-term boundary cases. Only then can this node declare minimal imports,
elaborate and fingerprint the canonical expression, compile transports, and execute the four
required mutation classes.

This statement node remains `[ ]` and blocked at `M3`. The root remains `[H1, M3, R4]`, with
`audit_complete: false` and `theorem_complete: false`. No worker self-test manifest is emitted
because the assigned exact-statement deliverable did not pass its gate.
