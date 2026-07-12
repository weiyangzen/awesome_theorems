# Exact-statement gate: blocked

Item: `S56-M-0899-STATEMENT`

Theorem: `THM-M-0899`

Base revision: `3815f6945257af057dfb5e6b6dfe2be5b6f451d9`

Base tree: `21a4f0ff758e83ab68c05b7741cdc4720f95cb1c`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is the title `Wilson定理`, the attribution Richard Wilson, the year
1972, and the gloss `t-设计的存在性` (existence of `t`-designs). It gives no source, definition,
parameters, ordered quantifiers, admissibility conditions, threshold, exceptions, or conclusion.

Those omissions do not have a unique conventional completion. Plausible readings include an
eventual pairwise-balanced-design theorem for a fixed allowed block-size set, a BIBD or `2`-design
specialization, a general `t-(v,k,lambda)` existence theorem, or a fixed construction or exact
classification. These readings have different binders and hypotheses. The intake's bibliographic
discovery also exposes a material conflict: Wilson's PBD papers I and II date to 1972, while part
III is titled *Proof of the existence conjectures* and dates to 1975; none is cited by the catalog,
and their titles do not establish the catalog's arbitrary-`t` wording.

Selecting one reading would therefore invent, narrow, broaden, or substitute mathematics. It could
also duplicate the separately owned asymptotic-design target `THM-M-0900`. The unrelated
factorial/primality Wilson theorem in mathlib is excluded by the catalog's subject, author, year,
and gloss.

The intake correctly leaves its canonical human claim, Lean module and expression, expression
hash, target environment fingerprint, binders, and hypotheses null or empty. Its receipt is only a
provisional worker report with `accepted: false`, and the authoritative intake state is `[_]`, not
master-accepted `[x]`. Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a
missing expression fingerprint hard blockers. Minimal imports, transports, and the four required
statement mutations are undefined until one exact proposition is accepted. The root remains
`[H5, M4, R4]`; no statement or theorem completion is claimed.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates under the pinned environment with the single direct
import `Mathlib.Data.Finset.Powerset`. It checks five fixed-cardinality finite-subset and binomial
coefficient APIs. They define no PBD, BIBD, or `t`-design, choose no parameters or admissibility
contract, and state no existence theorem. The probe import therefore cannot be certified minimal
for the absent canonical target and receives no statement or proof credit.

A bounded exact-name search found no `BlockDesign`, `BalancedIncompleteBlockDesign`,
`PairwiseBalancedDesign`, `CombinatorialDesign`, `SteinerSystem`, `SteinerTripleSystem`, or
`TDesign` declaration in pinned mathlib, repository-local Lean, or the Stage1 Lean probes. This is
only feasibility evidence for this blocker, not the downstream anchor audit or a global absence
claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` link to the canonical
pinned artifacts was reused without an update, build, clone, fetch, or dependency mutation.

## Validation Evidence

Commands ran in this worker clone on `2026-07-13` (`Asia/Shanghai`). Lean commands ran from
`Formalizations/Lean`; all others ran from the repository root unless noted.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0899` | 0 | rank 1041; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` before edits | 0 | only the automation-provided `.lake` link was untracked; base revision and tree appear above |
| scoped reads and SHA-256 checks over the blueprint, skill, manifests, source record, Stage0 projection, and complete intake dossier | 0 | the gloss and discovery records do not select one exact proposition; exact current hashes are in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0899/check_intake.py` | 1 | historical intake replay stops because it expects intake `[ ]` while shared authority now records provisional `[_]`; its stored authority hashes and intake-only inventory are also historical and were not rewritten |
| `lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib revision, tree, and status checks | 0 | pinned revision and tree recorded above; package worktree clean |
| `lake env lean ../../Stage1_Instances/THM-M-0899/IntakeProbe.lean` | 0 | five generic APIs elaborated; stdout SHA-256 `2514bbeb6e9ac4190163b459b04953a7ea56ce7f4013c443c905630bb70a797d`; no target or proof body |
| bounded exact-design declaration search | 1 | expected no-match exit; discovery-only feasibility evidence |
| prohibited-construct scan over owned Lean files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| JSON parse, scoped blocker invariants, and scoped whitespace checks | 0 | blocker identity, null target/imports, unchanged vector, four undefined mutations, exact two-file scope, and no-self-test boundary agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker is historical evidence for the earlier intake attempt. Shared integration later
changed the authoritative intake state and authority-file bytes, and this phase adds two files
beyond its frozen intake-only inventory. This worker records those facts rather than modifying the
intake checker, receipt, instance, local task DAG, generated blueprint, or authoritative DAG to
manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must refresh and master-accept the intake. Accountable reviewers must then
preserve and hash an immutable primary or authoritative source, select and independently approve
one exact Wilson result, reconcile the 1972/1975 and PBD/BIBD/general-`t` boundaries, and freeze all
incorporated definitions, ordered binders, hypotheses, conclusion, proof boundary, corrections,
and degenerate cases. They must also decide the ownership boundary with `THM-M-0900`.

A fresh statement worker can then encode precisely that source-selected claim, minimize pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute the removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`. Because exact-target elaboration did not pass, no
`.stage1-worker-selftest.json`, node receipt, worker `[_]`, or master acceptance is claimed.
