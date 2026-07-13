# Exact-statement gate: blocked

Item: `S56-M-0054-STATEMENT`

Theorem: `THM-M-0054`

Base revision: `a16267e7165144d202080fb647261658fa75ceb2` (tree
`6edd90c440309a0c5ba277ef62d1733b4b9c05b1`).

## Decision

The statement item remains `[ ]`. Rev-5.6 section 10.2 permits dependency-ordered preparation
while `S56-M-0054-INTAKE` is only provisional worker state `[_]`. Its receipt declares
`accepted: false`, has no accepted receipt ID, and intentionally leaves the canonical human and
Lean statements null. Master acceptance of that dependency remains necessary before any later
statement transition can be accepted.

Independently and decisively, the received record cannot identify one exact proposition. The
repository supplies only the gloss "spectral properties of nonnegative matrices," the compound
Perron-Frobenius name, the year 1907, and an untrusted `verified` label. It contains no formula,
definition chain, ordered binders, hypotheses, conclusion bundle, source theorem locator, proof
boundary, correction history, or accountable review.

The proposition-changing choices left open include:

- an arbitrary nonnegative, irreducible nonnegative, primitive nonnegative, or entrywise-positive
  square matrix;
- the scalar field, finite index type, nonempty or positive-dimension convention, and entrywise
  order encoding;
- a left or right eigenvector and whether it is nonzero, nonnegative, strictly positive,
  normalized, or only projectively specified;
- whether the Perron value is stated as a real eigenvalue, a complex spectral element, or the
  spectral radius, and which bridges among these representations belong to the target;
- algebraic simplicity, geometric simplicity, weak spectral dominance, strict dominance, or a
  source-selected conjunction; and
- cyclic peripheral spectrum, periodicity, and the zero-dimensional, zero-matrix, reducible,
  imprimitive, identity, and one-by-one boundary cases.

Perron's 1907 paper *Zur Theorie der Matrices*, DOI `10.1007/BF01449896`, is a credible historical
lead, not an admitted exact statement. No lawful complete edition, pinpoint proposition,
incorporated definition chain, correction audit, or independent review is present. The applicable
Frobenius extension source has not been identified at all. The separate out-of-scope physics record
about a positive matrix's largest eigenvalue is narrower and cannot be substituted for this target.

Choosing any familiar Perron-Frobenius variant would therefore invent, narrow, broaden, or replace
the received theorem. Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression
fingerprint hard blockers. There is no honest canonical target whose imports can be minimized, no
credited alternate encoding for a checked transport, and no meaningful removed-hypothesis,
changed-domain, changed-binder-scope, or boundary-case mutation. The canonical root vector remains
unclassified; the intake's provisional theorem-family assessment remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with four direct imports from the pinned dependency
closure. It checks eight adjacent APIs for nonnegative-matrix irreducibility and primitivity,
matrix spectrum and eigenvalues, and generic spectral radius results. The complete probe output has
SHA-256 `ed5dadabeefa5fc6d9c575d4b6928a499e8d11b29dea235a5f6c405181c45c86`.

This is real substrate validation only. The probe declares no canonical Perron-Frobenius target,
checked transport, or proof body. A bounded search found only an irreducibility-file topic tag and
a root-system TODO mentioning that Perron-Frobenius could prove another fact. It found no spectral
theorem joining the checked APIs. This search is discovery evidence, not the downstream anchor
audit or a proof of global absence. The probe's imports cannot be certified minimal for an absent
canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0054` | 0 | rank 1091; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| `git blame -L 405,410 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake env lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0054/IntakeProbe.lean` | 0 | eight adjacent pinned APIs elaborated; no canonical target or proof body; stdout hash recorded above |
| bounded Perron-Frobenius/nonnegative-matrix spectral search in pinned mathlib and repo-local Lean | 0 | only the probe disclaimer, one topic tag, and one unrelated TODO matched; no exact target declaration identified |
| `python3 -B Stage1_Instances/THM-M-0054/check_intake.py` | 1 | historical intake validator expects its intake item still to be `[ ]`; the integrated authority now records provisional `[_]`, so it is stale and is not statement evidence |
| prohibited-declaration scan of owned Lean files | 0 | the inner `rg` returned expected no-match exit 1; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration was found |
| `python3 -m json.tool Stage1_Instances/THM-M-0054/statement-blocker.json` plus scoped `jq -e` invariants | 0 | valid JSON; item/base identity, blocked/open state, null target/import/hash/fingerprint, unclassified root, unchanged provisional family vector, four undefined mutations, false completion fields, and no-receipt/no-self-test boundary agree |
| `git diff --check -- Stage1_Instances/THM-M-0054` plus per-new-file `git diff --no-index --check /dev/null ...` | 0 | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker is bound to intake-time state and deliberately was not modified to make a
statement attempt pass. The statement blocker is validated separately below; the generated
blueprint, authoritative execution DAG, intake instance, intake receipt, and open task DAG remain
unchanged.

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash complete Perron and applicable Frobenius
source editions, select and independently approve one exact proposition and proof boundary, and
transcribe every incorporated definition, ordered binder, hypothesis, conclusion, correction,
erratum, historical transport, normalization, and boundary case. They must explicitly resolve the
matrix variant, domain, Perron-root encoding, eigenvector orientation and normalization, simplicity
and dominance meanings, peripheral-spectrum clauses, and all degenerate cases.

A fresh statement run can then encode exactly that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile each credited transport, and
execute all four required mutation classes. The integration lane must also revalidate and
master-accept the intake dependency before accepting that future statement transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no root classification or debt-vector change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, expression fingerprint, proof credit, or master acceptance is claimed.
