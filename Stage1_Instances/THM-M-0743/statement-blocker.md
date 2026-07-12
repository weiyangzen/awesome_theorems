# THM-M-0743 exact-statement gate: blocked

- Item: `S56-M-0743-STATEMENT`
- Base revision: `ec27eb0336c89f0aed87200fc7cbf03a09996597` (tree
  `3fe77e381bf94ce1ed347bed17c94af25de8d543`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be truthfully
completed from the authoritative repository record. The record supplies only the title
`不动点定理`, Stephen Kleene, 1938, and the gloss `递归函数的不动点` (a fixed point of recursive
functions). It supplies no formula, bibliography, result locator, effective-numbering convention,
ordered binders, hypotheses, conclusion, proof boundary, correction history, or independent
review. Stage0 explicitly leaves the precise definitions and premises open, and rev-5.6 treats the
catalog's `已验证` label as untrusted metadata.

The intake identifies a strong historical lead and two pinned Lean declarations, but they do not
resolve the target:

- the Spring 2024 Stanford Encyclopedia archive, section 3.4, Theorem 3.5, states the total
  computable index-transformer formulation: there is an index `n` such that the programs indexed by
  `n` and `f n` compute the same partial function;
- Kleene's 1938 paper *On notation for ordinal numbers* is recorded only as bibliographic metadata;
  no accepted immutable theorem passage, incorporated definitions, assumptions, proof, corrections,
  or errata were inspected; and
- pinned mathlib distinguishes `Nat.Partrec.Code.fixed_point`, labelled Rogers' fixed-point theorem,
  from `Nat.Partrec.Code.fixed_point₂`, labelled Kleene's second recursion theorem.

Those Lean declarations have different binders and conclusions. The first requires a total
computable transformation `f : Code → Code` and concludes `∃ c, eval (f c) = eval c`. The second
requires a partial-recursive family `f : Code → Nat →. Nat` and concludes `∃ c, eval c = f c`.
The neighboring target `THM-M-0742` separately names the recursion theorem and recursive-function
self-reference, while the outside-Stage1 `THM-C-0006` explicitly names Kleene's second recursion
theorem and glosses it as every computable function having a fixed point. No accepted decision
assigns one declaration to this target or establishes a checked relationship between the separate
catalog records.

Selecting `fixed_point` because its upstream name matches the catalog title would still choose a
code carrier, acceptable numbering, totality convention, evaluator, extensional-equality notion,
binder order, and target ownership not frozen by the source. Selecting `fixed_point₂` would risk
substituting the neighboring recursion/self-reference target. Neither a theorem name nor a secondary
source is sufficient statement identity under rev-5.6. Consequently there is no canonical
expression on which to certify minimal imports, serialize an elaborated-expression fingerprint,
compile checked alternate transports, or run the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations. Those tests are undefined, not passed. The root
remains `[H1, M4, R4]`.

The execution DAG projects the intake dependency as provisional `[_]`, but its worker receipt
declares `accepted: false`, is not content-addressed, and contains no accepted receipt ID. This
dependency-ordered attempt records the independent substantive blocker; eventual statement
acceptance also requires master-accepted intake evidence.

## Pinned Lean boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated using
`Mathlib.Computability.PartrecCode`. It checks the code and evaluator interfaces, `Computable`,
`Partrec₂`, s-m-n, and both fixed-point candidates, then reports their axioms as `propext`,
`Classical.choice`, and `Quot.sound`. It declares no canonical target or wrapper. Its successful
elaboration is therefore candidate-feasibility evidence only; its import is not a certified minimal
import for the unidentified target and neither upstream proof body receives statement or proof
credit here.

A bounded search over pinned mathlib, shared Lean source, and this dossier confirmed the distinct
upstream labels and exact candidate declarations. This is narrow feasibility evidence, not the
downstream immutable anchor audit or a global absence claim. The scoped Lean scan found no `sorry`,
`admit`, `sorryAx`, axiom, bodyless declaration, opaque declaration, or unsafe declaration in the
owned source.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided canonical `.lake` symlink
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0743` | 0 | rank 1061; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped reads of the blueprint, skill, guidelines, manifest, execution DAG, catalog, Stage0 record, and complete intake dossier | 0 | the source identifies a recursion-theoretic fixed-point family but supplies no binder-complete proposition; intake deliberately leaves the canonical statement, binders, imports, and fingerprints null |
| `git blame -L 5479,5484 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0743/IntakeProbe.lean` | 0 | seven interfaces/candidate declarations and two axiom reports elaborated; output 900 bytes, 10 lines, SHA-256 `166ccdfc7b3729b22340048e857bd80feb3614e0bedc6ee2d14f3cfeec9aadb4`; no canonical target was declared |
| bounded fixed-point declaration search in pinned mathlib, shared Lean source, and this dossier | 0 | confirmed mathlib's distinct Rogers `fixed_point` and Kleene `fixed_point₂` declarations; this is not an exhaustive anchor audit |
| `python3 -B Stage1_Instances/THM-M-0743/check_intake.py` before adding blocker artifacts | 0 | historical intake invariants passed for the original nine-file dossier; the checker freezes that inventory and becomes stale after this phase adds two owned artifacts |
| `rg -n --glob '*.lean'` prohibited-construct scan over `Stage1_Instances/THM-M-0743` | 1 | expected no-match exit; no prohibited Lean declaration or escape hatch found |
| `python3 -m json.tool Stage1_Instances/THM-M-0743/statement-blocker.json` and scoped blocker assertions | 0 | structured blocker syntax, identity, null target/imports/hashes, four undefined mutations, unchanged vector, false completion flags, exact two-file scope, and absent self-test agree |
| `git diff --check` plus per-added-file `git diff --no-index --check` | 0 aggregate | no whitespace diagnostics; each raw no-index command returned the expected new-file difference status 1 |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest exists because the exact-statement deliverable did not pass |

The intake validator is phase-local historical evidence: it freezes the original nine-file intake
inventory. Adding these statement-phase artifacts expands the target directory, so a final replay
is expected to fail at that inventory assertion. This attempt records the known phase-evolution
failure rather than changing the intake checker, receipt, task DAG, generated blueprint, or
authoritative execution DAG to manufacture freshness.

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
preserve and hash an immutable primary or approved authoritative source, pinpoint the exact
fixed-point result and every incorporated definition and assumption, audit corrections and errata,
and independently approve the source-to-statement mapping and ownership relationship with
`THM-M-0742` and `THM-C-0006`. That selection must freeze the effective numbering or code model,
universal evaluator, total versus partial-recursive transformer and its arity, ordered binders,
extensional-equality convention, exact conclusion, foundations, checked alternate transports, and
all boundary cases.

A fresh statement run can then encode precisely that claim, establish minimal pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes. Until then this node remains `[ ]`; `audit_complete`
and `theorem_complete` are false. Because the assigned phase did not pass its completion gate, no
`.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof credit, or master acceptance
is claimed.
