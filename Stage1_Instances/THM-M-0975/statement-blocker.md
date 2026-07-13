# Exact-statement gate: blocked

Item: `S56-M-0975-STATEMENT`

Theorem: `THM-M-0975`

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b` (tree
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`).

## Decision

The statement item remains `[ ]`. Its prerequisite, `S56-M-0975-INTAKE`, has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt declares `accepted: false`, is
non-content-addressed, has no accepted receipt ID, and deliberately leaves both the canonical
mathematical statement and canonical Lean expression null. Its dossier may be inspected in
dependency order, but it is not accepted statement authority.

Independently, the repository record does not determine one proposition. Its entire mathematical
claim is `鞅差序列的集中` ("concentration of martingale difference sequences"), with the title
"Azuma-Hoeffding inequality," joint attribution to Kazuoki Azuma and Wassily Hoeffding, and the
year 1967. The record occurs twice verbatim. A separate manifest target, `THM-M-1080` (Azuma's
inequality), owns the same gloss. None of these records gives a formula, source locator,
definitions, ordered binders, hypotheses, conclusion, proof boundary, correction history,
boundary policy, or reviewer. The catalog's `已验证` label is explicitly untrusted by rev-5.6.

The intake inspected Azuma's 1967 paper *Weighted sums of certain dependent random variables*.
Printed pages 357-358 define bounded martingale differences and the conditional MGF properties
`[G]` and `[M]`; Lemma 1 proves a weighted MGF bound, and Remark 1 derives `[G]` from bounded
martingale differences. The paper's numbered theorems are asymptotic weighted-sum results, not the
familiar finite-horizon tail bound verbatim. The scan is a strong H1 source lead, but the exact
catalog root, complete definition and proof mapping, Hoeffding genealogy, corrections and errata,
lawful immutable admission, and independent review remain open.

The unresolved choices change the proposition rather than its notation:

- finite-horizon tail bound versus an original weighted-sum MGF or asymptotic result;
- a martingale, its increment sequence, or a strongly adapted process as the root object;
- almost-sure bounded increments versus conditional sub-Gaussian MGF hypotheses and their exact
  checked conversion and parameter squaring;
- weighted versus unweighted sums, the initial-term convention, and finite indexing;
- one-sided upper or lower tail versus a two-sided absolute tail and its constant;
- probability versus zero-or-probability measure assumptions and the precise event encoding; and
- the empty horizon, zero threshold, zero variance proxy, zero bounds, and almost-sure scopes.

Selecting a familiar modern form would therefore invent proposition-changing mathematics. In
particular, copying `THM-M-1080/Statement.lean` would violate the sibling-target ownership firewall,
and treating a conditional sub-Gaussian premise as a bounded-increment premise would skip an
unproved transport. Rev-5.6 sections 5 and 5.1 make this ambiguity and the absent expression
fingerprint hard blockers. There is no canonical target for which imports can be certified minimal,
alternate encodings transported, or removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations executed. Those tests are undefined, not passed. The root remains
`[H1, M3, R4]` because a pinned exact-topic candidate exists but is not the selected root.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` imports `Mathlib.Probability.Moments.SubGaussian` and re-elaborates
the exact-topic declaration
`ProbabilityTheory.measure_sum_ge_le_of_hasCondSubgaussianMGF`. It bounds the upper tail of a finite
sum of a strongly adapted real process whose initial term is sub-Gaussian and whose later terms are
conditionally sub-Gaussian. Its companion MGF aggregation theorem and ordinary bounded centered
Hoeffding lemma also elaborate. The two printed proof declarations report only `propext`,
`Classical.choice`, and `Quot.sound`.

That module is minimal only for the discovery probe; it cannot be certified as the minimal import
for an absent canonical target. The repo-local wrapper
`AwesomeTheorems.Stage1.S1_M_276.azuma_hoeffding_tail_bound` and `THM-M-1080` artifacts are owned by
other targets and supply no statement identity, transport, receipt, or proof credit here.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink exposed the canonical pinned artifacts and was used read-only.
No update, build, clone, fetch, or other dependency mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0975` | 0 | rank 1509; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped manifest, blueprint, skill, guideline, catalog, Stage0, and intake inspection | 0 | confirmed target membership, provisional prerequisite, duplicated gloss, null canonical target, sibling firewall, and open proposition-changing choices |
| `git blame` for both catalog copies and `THM-M-1080`'s same gloss | 0 | all three sparse records originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0975/IntakeProbe.lean` | 0 | seven conditional sub-Gaussian and filtration interfaces elaborated; stdout SHA-256 `bad24eed3956142a6a048a339d1e0a23620950a9b9732373eb8b03a1c359f3cc`; empty stderr; no canonical target or proof body |
| bounded search for Azuma-Hoeffding declarations in pinned mathlib and repo-local Lean | 0 | found the exact-topic mathlib theorem, a foreign legacy wrapper, sibling artifacts, and this probe; none selects the `THM-M-0975` root |
| `python3 -B Stage1_Instances/THM-M-0975/check_intake.py` | 1 | historical intake checker expects the authoritative intake row at `[ ]`; integration now records provisional `[_]`; stale historical evidence, not statement validation |

Final JSON, invariant, prohibited-construct, whitespace, and absent-self-test checks are recorded in
the structured blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must first master-accept refreshed intake evidence. Accountable source and
scope reviewers must lawfully preserve and hash an immutable primary or approved authoritative
source, select one exact theorem, resolve why `THM-M-0975` remains distinct from `THM-M-1080`, and
independently approve every incorporated definition, ordered binder, hypothesis, conclusion, proof
boundary, attribution, correction, erratum, normalization, tail direction, index convention, and
degenerate case. Any bounded-increment to conditional-MGF bridge used in the root must be stated
and checked rather than inferred.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, proof
credit, or master acceptance is claimed.
