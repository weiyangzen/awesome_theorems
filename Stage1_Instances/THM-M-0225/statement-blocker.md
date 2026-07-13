# Exact-statement gate: blocked

Item: `S56-M-0225-STATEMENT`

Theorem: `THM-M-0225`

Base revision: `d257e1e5e5fa003d6e1f26344c0331bf99374fa9` (tree
`fa06b50b528e038d182d5479a18296f63fa5eae5`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-0225-INTAKE` is provisional `[_]`, not
a master-accepted receipt. More importantly, the authoritative repository record does not identify
one exact true proposition that can be encoded without inventing missing mathematics.

The record supplies only the title maximum modulus principle, Karl Weierstrass, 1875, and the gloss
"the modulus of a holomorphic function cannot attain a maximum in the interior." The literal gloss
is false: every constant holomorphic function attains its modulus maximum at every interior point.
It contains no bibliography, exact theorem, incorporated definitions, ordered binders, proof
boundary, corrections or errata, or independent source review.

The following unresolved choices change the proposition:

- impossibility for a nonconstant function versus rigidity concluding constancy;
- a local maximum at one point versus a maximum on an open connected domain;
- scalar maps on subsets of `Complex` versus maps between complex normed spaces;
- differentiability near a point versus differentiability on a set;
- explicit openness, membership, nonemptiness, and preconnectedness assumptions;
- constancy of values versus constancy only of norms; and
- an interior-rigidity theorem versus a bounded-domain frontier theorem.

The immutable Encyclopedia of Mathematics revision inspected at intake distinguishes local,
global-supremum, and boundary versions and cites Ahlfors (1979), page 241. It is a useful secondary
source lead, not an admitted exact source packet or independent review. Selecting a familiar form
from mathematical memory or choosing whichever pinned theorem is easiest would silently repair and
complete the catalog claim.

Rev-5.6 section 5 makes statement ambiguity and a missing elaborated-expression fingerprint hard
blockers. Consequently there is no canonical expression for which minimal imports, checked
alternate transports, or the required removed-hypothesis, changed-domain, changed-binder-scope,
and boundary-case mutations can be certified. Those mutations are undefined, not passed. The root
remains `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with its sole direct import
`Mathlib.Analysis.Complex.AbsMax`. The pinned module itself warns that several materially different
statements are called the maximum modulus principle. The probe checks:

- local norm constancy: `Complex.norm_eventually_eq_of_isLocalMax`;
- local value constancy with strict convexity: `Complex.eventually_eq_of_isLocalMax_norm`;
- connected-domain norm constancy: `Complex.norm_eqOn_of_isPreconnected_of_isMaxOn`;
- connected-domain value constancy with strict convexity:
  `Complex.eqOn_of_isPreconnected_of_isMaxOn_norm`; and
- two boundary variants: `Complex.exists_mem_frontier_isMaxOn_norm` and
  `Complex.norm_le_of_forall_mem_frontier_norm_le`.

All six interfaces elaborate in the pinned environment. Four representative declarations report
`[propext, Classical.choice, Quot.sound]`. Their inequivalent hypotheses and conclusions confirm
the source-selection problem; they do not resolve it. The import is the smallest located module
for these Euclidean candidates, but it cannot be certified minimal for an absent source-selected
root. The probe declares no canonical target, transport, or proof body and receives no statement,
anchor-audit, or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only, and the mathlib package worktree remained clean. No update, build, clone, fetch, or
other dependency mutation was run.

## Validation Record

Commands ran in the isolated worker checkout on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0225` | 0 | rank 1238; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (pre-edit); `git rev-parse HEAD 'HEAD^{tree}'` | 0 each | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| `git blame -L 1626,1631 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 and Lake 5.0.0 at the revisions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}' 'HEAD:Mathlib/Analysis/Complex/AbsMax.lean`; package `status --short` | 0 each | pinned revision, tree, and source blob `e8ff6a7da9e9b0324d2928a77d464b7fd40ff5fa`; package status empty |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0225/IntakeProbe.lean` | 0 | six direct named candidates elaborated; four axiom reports were `[propext, Classical.choice, Quot.sound]`; stdout SHA-256 `d1e9e19f8ffb30b45cf3156ce1e91b152172e2faa816b9942c2402c8b3cd8255` |
| bounded exact-topic `rg` search recorded in `statement-blocker.json` | 0 | pinned local, global, norm, value, and boundary variants were found; no source-selected repo-local root was found; discovery only |
| `python3 -B Stage1_Instances/THM-M-0225/check_intake.py` | 1 | known historical-intake replay boundary: the checker expects intake `[ ]`, while integrated authority records provisional `[_]`; historical evidence was not rewritten |
| `python3 -m json.tool Stage1_Instances/THM-M-0225/statement-blocker.json`; scoped JSON invariant check | 0 each | identity, null target and imports, four undefined mutations, unchanged vector, false completion flags, two-file scope, and no-self-test boundary passed |
| prohibited-declaration scan over owned Lean files | 1 | expected no match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0225`; separate new-file checks recorded in the JSON | 0 / 1 each | no whitespace diagnostics; each no-index exit 1 is only the expected added-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The historical intake checker is bound to intake-time authoritative state and its earlier
repository revision. Its failure after integration is not a statement validation failure to patch
around, and modifying that historical artifact is outside this phase.

## Retry Condition And Status Boundary

The integration lane must first master-accept the intake before any accepted statement transition.
Accountable reviewers must then preserve and hash a lawful immutable primary or authoritative
source, select and independently approve its exact local, global, or other form, and crosswalk every
incorporated definition, ordered binder, hypothesis, constant exception, conclusion, proof
boundary, correction, erratum, transport, and boundary case. A later statement worker can encode
only that claim, minimize its pinned imports, serialize and hash the elaborated expression and
environment, compile every credited transport, and run all four mutation classes.

This records the first failed gate. It does not complete the statement node or any downstream node.
The root remains `[H1, M3, R4]`; `audit_complete` and `theorem_complete` remain false, and no debt
change is proposed. The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json`, node-specific completion receipt, worker `[_]`, proof credit, or
master-acceptance claim is emitted.
