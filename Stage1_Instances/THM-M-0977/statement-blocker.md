# Exact-statement gate: blocked

Item: `S56-M-0977-STATEMENT`

Theorem: `THM-M-0977`

Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d` (tree
`0d6c1fdf06d1573c256af331c6b198e5a787af43`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0977-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`. The intake receipt is unaccepted and
non-content-addressed, contains no accepted receipt ID, and deliberately leaves the canonical
mathematical statement and Lean target null. Dependency-ordered inspection is possible, but no
accepted statement transition can precede refreshed intake validation and master acceptance.

Independently, the exact-statement gate cannot pass from the received repository claim. The catalog
supplies only the name "Chernoff bound," Herman Chernoff/1952 attribution, and the gloss "tail
probabilities for sums of independent random variables." It gives no formula and does not select:

- an upper, lower, two-sided, or bundled tail;
- general, bounded, Bernoulli, binomial, or identically distributed summands;
- finite or asymptotic indexing and the exact independence and moment assumptions;
- fixed-tilt MGF, CGF, optimized, entropy, additive, multiplicative, or rate-function form; or
- binder order, event convention, parameter domains, and degenerate cases.

The catalog separately assigns `THM-M-0993` to the translated title `切尔诺夫界` with the same
author, year, gloss, importance, and status. Its provisional artifacts select a positive-tilt,
finite-family, product-MGF upper-tail proposition, but no accepted identity, allocation, merge, or
evidence-sharing decision authorizes importing that choice. The legacy `S1_M_273` six-part MGF/CGF
package is likewise discovery input only. Choosing either target, or any familiar mathlib variant,
would invent, narrow, broaden, or substitute proposition-changing mathematics.

The plausible source lead is Herman Chernoff, *A Measure of Asymptotic Efficiency for Tests of a
Hypothesis Based on the Sum of Observations*, *Annals of Mathematical Statistics* 23(4) (1952),
493-507, DOI `10.1214/aoms/1177729330`. Intake observed bibliographic metadata, but the article
endpoints returned access-control HTML. No pinpoint result, definitions, assumptions, proof
passage, correction or errata audit, modern-name mapping, immutable source packet, or independent
review is admitted. The source therefore identifies a family, not one exact proposition.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard
blockers. There is consequently no canonical expression for which minimal imports, checked
transports, or the required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations can be certified. All four mutation classes are undefined, not passed.
No `Statement.lean`, proof body, weakened special case, broadened interface, or circular premise was
added. The root remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with the single direct import
`Mathlib.Probability.Moments.Basic`. It exposes four fixed-tilt upper/lower MGF/CGF inequalities and
three finite independent-sum interfaces:

- `ProbabilityTheory.measure_ge_le_exp_mul_mgf` and `measure_le_le_exp_mul_mgf`;
- `ProbabilityTheory.measure_ge_le_exp_cgf` and `measure_le_le_exp_cgf`; and
- `ProbabilityTheory.iIndepFun.integrable_exp_mul_sum`, `mgf_sum`, and `cgf_sum`.

All seven signatures elaborate. Each axiom report lists
`[propext, Classical.choice, Quot.sound]`, and the exact probe output has SHA-256
`618599c0352f40ad75934e61ed256b1f31a9db2a7632fa14a5646cbd1db3c47e`. The import exposes strong
exact-topic candidates, but it cannot be certified minimal for an absent canonical target. The
probe declares no target, checked source transport, mutation fixture, or proof body.

A bounded search over the owned path, pinned mathlib, repository-local Lean, and separately owned
`THM-M-0993` located these interfaces and foreign wrappers. The `LC_ALL=C` sorted output SHA-256 is
`9dc2907017c64b1a6d2a4f85dd02362355edab4af7538e28462eec6682689baa`. This is discovery-only
evidence, not the downstream immutable anchor/provenance audit or a source-identity result.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No dependency update, build, clone, fetch,
or other `.lake` mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0977` | 0 | rank 1511; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| scoped `sed`, `rg`, `find`, and JSON inspection of the blueprint, skill, guidelines, catalog, Stage0, manifest, execution DAG, intake, duplicate, legacy, and pinned candidates | 0 | confirmed the null target, proposition-changing choices, and unresolved duplicate ownership |
| `git blame -L 7134,7139` and `git blame -L 7259,7264` on the catalog | 0 | both six-line records originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` with the exact authority, intake, source, toolchain, lockfile, and pinned mathlib paths listed in `statement-blocker.json` | 0 | exact hashes are recorded in the structured blocker |
| `python3 -B Stage1_Instances/THM-M-0977/check_intake.py` | 1 | historical intake checker expects authoritative intake `[ ]` with zero attempts; integration records provisional `[_]` with one attempt; prior evidence was not rewritten |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree and package-status checks | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0977/IntakeProbe.lean` | 0 | seven exact-topic interfaces and axiom reports elaborated; stdout hash recorded above; no canonical target declared |
| `rg -n -i --glob '*.lean' 'Chernoff\|measure_ge_le_exp_(mul_mgf\|cgf)\|measure_le_le_exp_(mul_mgf\|cgf)\|iIndepFun\\.(integrable_exp_mul_sum\|mgf_sum\|cgf_sum)' ... \| LC_ALL=C sort \| sha256sum` | 0 | located exact-topic candidates and separately owned wrappers; exact roots and sorted-output hash are in the JSON; discovery only |
| `rg -n --glob '*.lean' '\\b(sorry\|admit)\\b\|\\bsorryAx\\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0977` | 1 | expected no-match result; no prohibited declaration |

Final JSON, scoped invariant, whitespace, final-newline, and absent-self-test checks are recorded in
the structured blocker beside this report.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence and resolve the
`THM-M-0977`/`THM-M-0993` identity and root ownership. Accountable reviewers must preserve and hash
a lawful immutable primary or approved authoritative source, adopt and independently approve one
exact theorem passage, and map every incorporated definition, ordered binder, universe, premise,
conclusion, proof boundary, correction, erratum, modern-name relationship, transport, and boundary
case. The decision must explicitly settle tail direction, variable class, index model, independence
and moment premises, parameters, event convention, formula family, and degenerate cases.

A fresh statement worker can then encode only that reviewed claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
