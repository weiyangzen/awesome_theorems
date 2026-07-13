# Exact-statement gate: blocked

Item: `S56-M-0075-STATEMENT`

Theorem: `THM-M-0075`

Base revision: `cea7a197878ce23e819b006b2780b0bb1702fbbe` (tree
`079dc70c0b48278054700d1b4d45efee14a3bd04`).

## Decision

The statement item remains `[ ]`. Its prerequisite, `S56-M-0075-INTAKE`, has provisional state
`[_]`, not master-accepted state `[x]`; its provisional receipt is explicitly unaccepted. More
importantly, the intake found a proposition-changing conflict and deliberately left the canonical
mathematical statement and canonical Lean target null.

The received catalog gloss says only "about the linear independence of induced characters" and
attributes it to Emil Artin in 1931. It does not identify the group, finiteness premise, subgroup
family, duplicate/conjugacy convention, character object, induction map, coefficient ring, ordered
binders, hypotheses, conclusion, or boundary cases. The authoritative modern theorem lead inspected
at intake, Serre Chapter 9 Section 9.2 Theorem 17 and its corollary, instead concerns finite cokernel
and rational spanning by induced characters. That is materially different from linear independence.
Selecting standard Artin induction would therefore correct or substitute the catalog claim rather
than elaborate it.

Rev-5.6 sections 5 and 5.1 require the exact human claim to be fixed before the canonical expression,
minimal imports, expression hash, environment-expression fingerprint, checked transports, or
statement mutations can be credited. There is consequently no truthful Lean proposition to declare
for this run. The first failed gate is `canonical_statement_identity`. The root debt vector remains
`[H1, M4, R4]`; `audit_complete` and `theorem_complete` remain false.

## Source Boundary

The repository source record at `Docs/researches/math_theorems.md:554-559` contains only the name,
author, year, one-line independence gloss, importance, and an untrusted verified label. The record
origin is commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`, with source blob
`5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf`. The Stage0 projection at lines 2163-2188 explicitly
leaves the formal system, foundation, exact definitions and premises, proof path, equivalent forms,
axioms, and machine artifact open.

The intake records these uncredited leads:

- Jean-Pierre Serre, *Linear Representations of Finite Groups* (1977), Chapter 9, Section 9.2,
  Theorem 17 and corollary, printed page 70, DOI `10.1007/978-1-4684-9458-7`. The inspected
  university-mirrored scan had SHA-256
  `099bb953993bce35bcbdccd989140248e4db8dd066744a62830b7fe940627516`. Its result is finite
  cokernel/rational spanning, not the received independence claim.
- Emil Artin, "Zur Theorie der L-Reihen mit allgemeinen Gruppencharakteren," *Abhandlungen aus dem
  Mathematischen Seminar der Universitaet Hamburg* 8 (1931), 292-306, DOI
  `10.1007/BF02941010`. Only bibliographic metadata was inspected; no exact proposition, definitions,
  proof boundary, translation, correction history, or independent review was accepted.

Neither lead supplies authority to rewrite the received claim. Dedekind independence of monoid
homomorphisms, independence of irreducible characters, representation induction alone, Brauer
induction, or a finite/cyclic/special case is also outside the frozen target boundary.

## Lean Boundary

`IntakeProbe.lean` was re-elaborated under the pinned environment. It checks eight adjacent APIs:
`FDRep.character`, `FDRep.char_conj`, `FDRep.char_orthonormal`, `Representation.ind`,
`Rep.indFunctor`, `Rep.indResHomEquiv`, `Rep.indResAdjunction`, and
`linearIndependent_monoidHom`. These interfaces show that character, representation-induction, and
generic Dedekind-independence vocabulary is available. They do not define a virtual-character ring,
state Artin induction, relate induction to characters, identify a family of induced characters, or
state the catalog's independence claim. The probe therefore receives discovery-only evidence and
no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The toolchain file SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the Lake manifest SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. The automation-provided
`.lake` symlink and canonical pinned artifacts were used read-only. No update, build, dependency
clone, fetch, or dependency mutation ran.

Because the canonical target is absent, `minimal_imports_for_canonical_target`, the elaborated
expression hash, and the canonical environment-expression fingerprint remain null. No alternate
encoding is credited. Removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations are not meaningful until an exact source-selected proposition exists.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0075` | 0 | rank 1103; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; the base identifiers appear above |
| `python3 -B Stage1_Instances/THM-M-0075/check_intake.py` | 1 | known phase-evolution failure: the historical intake checker expects intake state `[ ]`, while the integration-updated execution DAG records provisional `[_]`; historical intake evidence was not rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean `4.29.0` at the recorded commit and Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | the recorded pinned revision and tree; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0075/IntakeProbe.lean` | 0 | all eight adjacent API checks elaborated; stdout was 1501 bytes/17 lines with SHA-256 `d34978c563908658aa27c9ab78bc83a477c2361d4245d55cbce6aa9f5ba1d2f0`; no canonical target was declared |
| bounded `rg` over repository-local and pinned-mathlib Lean for Artin induction and induced-character theorem spellings | 0 | found only unrelated `artinCharacter_one_eq_finrank` and legacy Artin-L-function/Brauer-induction audit text; no exact target declaration was identified; this is bounded discovery evidence, not a global absence claim |
| `rg -n --glob '*.lean' '\b(sorry|admit)\b|\bsorryAx\b|^[[:space:]]*(axiom|constant|opaque)\b|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-0075` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in owned Lean files |
| `git diff --check -- Stage1_Instances/THM-M-0075` plus `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0075/statement-blocker.md` | 0 wrapper result | no whitespace diagnostics; the raw new-file comparison returned only the expected difference status 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

Current authority fingerprints used for this run are: blueprint
`141d130db6cfdf9dc66b8c778af27fae86bacdbc9f9c7025e135a1bfe31b74a3`, target manifest
`02eec284de534dd78e1cf75f82a477ff477567dd682b7445cb7587abd137ab2c`, execution DAG
`e28e8337d911c72c9608200214ee84fd2b614f4f0271b5746c6f47ad394d4028`, and execution skill
`26d47a66c6535feabb8bbf1051fd55d76a53fe761f4b3d953f86b97ec86152b8` (all SHA-256). The intake
instance's older blueprint/DAG hashes are retained as historical intake evidence and were not
rewritten.

## Retry Condition And Status Boundary

An accountable source decision must either correct the catalog to a pinpointed Artin-induction
proposition or identify a genuine induced-character independence theorem. It must preserve an
immutable source edition, exact theorem/page, incorporated definitions, assumptions, conclusion,
proof boundary, translation, corrections and errata, and independent review. It must also fix the
group and finiteness convention, subgroup/index family, duplicate and conjugacy handling, character
and induction objects, coefficient ring, ordered binders, hypotheses, conclusion, and every boundary
case. A later run can then encode exactly that proposition, minimize pinned imports, serialize the
elaborated expression and environment fingerprint, check every credited transport, and run all four
required mutation classes.

This artifact is the truthful result of the assigned phase: blocked before exact target elaboration.
No statement receipt, worker `[_]` self-test, expression fingerprint, canonical obligation, proof
body, debt-vector change, audit completion, theorem completion, or master acceptance is claimed.
