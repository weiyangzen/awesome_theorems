# Exact-statement gate: blocked

Item: `S56-M-0913-STATEMENT`

Theorem: `THM-M-0913`

Base revision: `fcabbf1e0ad9507eebe91663bccabfa87d22813e` (tree
`873e589c594454b7f263c7ed2342089a4d15e842`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0913-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. Rev-5.6 section 10.2 permits this investigation while
concurrency is enabled, but the intake receipt declares `accepted: false`, contains no accepted
receipt ID, and deliberately leaves the canonical mathematical statement and formal target null.
Master closure remains dependency ordered.

Independently and decisively, the exact-statement gate fails. The repository record supplies only
the title "inclusion-exclusion principle," the attribution "many mathematicians," the period
"19th century," and the gloss "a formula for the number of elements in a union." It contains no
formula, bibliography, exact theorem locator, definitions, ordered binders, hypotheses, conclusion,
proof boundary, correction history, or boundary convention. The catalog's `verified` label is
untrusted under rev-5.6, and Stage0 explicitly leaves precise definitions and premises open.

The wording does not decide:

- a two-set, fixed-arity, or arbitrary finite-family formula;
- `Finset`, finite `Set`, `Fintype`, measure, or probability encoding;
- natural subtraction, a rearranged natural equality, or an integer alternating sum;
- the index and element domains, universes, finiteness and decidable-equality assumptions;
- the union and nonempty-subfamily intersection conventions; or
- empty families, singleton families, empty members, duplicate indexed sets, empty element types,
  alternate complement or weighted forms, and other degenerate cases.

These choices change the proposition. In particular, pinned mathlib's
`Finset.inclusion_exclusion_card_biUnion` is a strong arbitrary-finite-family cardinality
candidate, but choosing it now would add a finite index support, finite member sets, decidable
equality, an integer codomain, alternating coefficients, a powerset of nonempty index subfamilies,
and a specific intersection and empty-family convention. The intake explicitly withholds that
normalization pending an immutable exact source proposition or independent scope approval.
Likewise, the two-set identity `Finset.cast_card_union`, the weighted-sum theorem, complement
identities, and measure variants cannot silently replace the unidentified root.

Sections 5 and 5.1 make statement ambiguity, unresolved target choices, and a missing expression
fingerprint hard blockers. There is therefore no honest canonical expression for which minimal
imports, an environment-expression fingerprint, checked alternate transports, or the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can be
certified. Those four mutation classes are undefined, not passed. No `Statement.lean`, proof body,
axiom, placeholder, weakened special case, or broadened substitute was added. The root remains
`[H5, M3, R4]`; `H5` classifies the received gloss as not one stable proposition, not the
source-selected classical mathematics as false or open.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` re-elaborates under the pinned environment. It
checks six adjacent interfaces: the indicator, weighted finite-union, finite-family cardinality,
two complement, and two-set cardinality variants. It also prints the axioms reported for the
finite-family and two-set candidates. All checks pass, and both printed candidates report
`propext`, `Classical.choice`, and `Quot.sound`.

The probe directly imports `Mathlib.Combinatorics.Enumerative.InclusionExclusion` and
`Mathlib.Data.Finset.CastCard` because it surveys multiple candidate roots. The first import alone
exposes `Finset.inclusion_exclusion_card_biUnion`; the second is for the two-set alternative. Since
the probe declares no canonical target or source transport, neither this pair nor the candidate's
single import is a minimal-import certificate for the absent source-approved proposition. The
successful elaboration receives interface-feasibility evidence only, with no statement or proof
credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0913` | 0 | rank 1455; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; the base identifiers appear above |
| scoped catalog, Stage0, manifest, blueprint, skill, and complete intake-dossier inspection | 0 | confirmed the sparse family gloss, explicit null target, pinned uncredited candidates, and open proposition-changing decisions |
| `sha256sum` and canonical excerpt/JSON hashing over authority, source, intake, probe, toolchain, lockfile, and relevant pinned mathlib inputs | 0 | exact hashes are recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0913/check_intake.py` | 1 | the historical intake checker stops because it expects the intake authority state `[ ]`, while the current integrated DAG records provisional `[_]`; this phase records rather than rewrites historical evidence |
| `cd Formalizations/Lean && lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0913/IntakeProbe.lean` | 0 | six adjacent interfaces elaborated; complete output is 1776 bytes over 17 lines with SHA-256 `09ddedb9bf141520d987894a79fc381c8916f0765a42022067d77e31135bd55c`; no canonical target or proof body |
| bounded inclusion-exclusion search over pinned mathlib and repository-local Lean | 0 | located the dedicated finite-family module, two-set identity, and other variants; discovery-only evidence, not the downstream anchor audit |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, scoped invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
lawfully preserve and hash an immutable primary or accepted authoritative source, or explicitly
approve a finite-family normalization. They must independently review and freeze the exact formula,
arity, domains, universes, set and index encodings, finiteness assumptions, coefficient and
subtraction convention, union and intersection convention, ordered binders, hypotheses,
conclusion, alternate forms, proof boundary, corrections, errata, and degenerate cases.

A fresh statement worker can then encode precisely that approved claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
