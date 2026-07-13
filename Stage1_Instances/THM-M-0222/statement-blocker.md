# Exact-statement gate: blocked

Item: `S56-M-0222-STATEMENT`

Theorem: `THM-M-0222`

Base revision: `bd81d4853a030765585ef6fed4310484ceb1e458` (tree
`fb92fc7476bff9a2ce8c20f1d7be34c6655ca6b4`).

## Decision

The statement item remains `[ ]`. Its prerequisite, `S56-M-0222-INTAKE`, is projected as
provisional worker state `[_]`, not master-accepted `[x]`; its receipt is unsigned, mutable,
non-content-addressed, and explicitly `accepted: false`. The historical intake checker also
expects the pre-integration execution-DAG state and therefore no longer replays at this revision.
Those dependency facts prevent an accepted statement transition, but they are not the decisive
mathematical blocker.

The repository record supplies only the name "Cauchy integral formula," the attribution to
Augustin Cauchy in 1831, and the gloss that a holomorphic function is represented by its boundary
values. It gives no bibliography, formula, definition chain, ordered binders, hypotheses,
conclusion, proof boundary, corrections, errata, or independent review. The `verified` source
label is untrusted under rev-5.6.

The intake's modern source lead, NIST DLMF 1.9.E30, gives a scalar formula for a positively
oriented simple closed contour; 1.9.E31 adds higher derivatives. Pinned mathlib instead exposes
several circle formulas, including Banach-valued and off-countable differentiability variants.
The catalog does not select among scalar and Banach-valued codomains, general contours and
circles, regularity packages, exceptional sets, winding and orientation conventions,
normalizations, evaluation points, or value-only and derivative conclusions. Each choice changes
the proposition. The DLMF lead is not the catalog's cited source or an accepted historical 1831
statement, so choosing it, or choosing the most convenient mathlib theorem, would silently narrow,
broaden, or substitute the received target.

Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing elaborated-expression
fingerprint hard blockers. There is consequently no honest canonical Lean expression whose import
can be certified minimal, no credited alternate encoding, and no meaningful removed-hypothesis,
changed-domain, changed-binder-scope, or boundary-case mutation suite. No mathematical or Lean
statement was added. The lifecycle stays `planned`, and the root vector stays `[H1, M3, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` re-elaborates with the one direct import
`Mathlib.Analysis.Complex.CauchyIntegral`. It authenticates six adjacent APIs, including:

```text
Complex.two_pi_I_inv_smul_circleIntegral_sub_inv_smul_of_differentiable_on_off_countable
Complex.circleIntegral_sub_inv_smul_of_differentiable_on_off_countable
DiffContOnCl.two_pi_i_inv_smul_circleIntegral_sub_inv_smul
DifferentiableOn.circleIntegral_sub_inv_smul
Complex.circleIntegral_div_sub_of_differentiable_on_off_countable
```

The normalized candidate assumes `w` lies in `ball c R`, continuity of `f` on the closed ball,
and differentiability in the open ball away from a countable set, then concludes

```text
(2 * pi * I)^-1 • integral_C(c,R) ((z - w)^-1 • f z) = f w.
```

The scalar candidate instead uses division and an unnormalized conclusion. Representative axiom
reports list `propext`, `Classical.choice`, and `Quot.sound`. These checks are statement-feasibility
evidence only: the probe declares no target, compiles no source transport or mutation, and receives
no proof credit. Its import cannot be called minimal for an absent canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone, fetch,
or other dependency mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0222` | 0 | rank 1235; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| source blame, blob, and excerpt-hash checks | 0 | all six uncited catalog lines originate at `bcf3f9fa...`; catalog excerpt SHA-256 `1c312315...cf92`; the Stage0 excerpt SHA-256 is `e814dbdf...cf0` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| pinned mathlib revision/tree/status checks | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0222/IntakeProbe.lean` | 0 | six candidate signatures and two axiom reports elaborated; complete output SHA-256 `08510af8...aad6`; no target declaration |
| bounded Cauchy-formula search in pinned mathlib and repo-local Lean | 0 | found the candidate family and foreign `THM-M-1559` wrapper; output SHA-256 `0936432a...90f`; no source selection or ownership transfer |
| `python3 -B Stage1_Instances/THM-M-0222/check_intake.py` | 1 | historical checker expects intake state `[ ]`, attempts 0, while integrated authority projects `[_]`, attempts 1; the historical artifact was not rewritten |
| JSON parse and scoped blocker-invariant checks | 0 | structured blocker identity, null target/import/fingerprints, unchanged vector, four undefined mutations, false completion flags, and blocked state agree |
| declaration-position prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |
| per-new-file no-index whitespace checks; scoped tracked diff check | 1 for each new file; 0 scoped | expected added-file difference status with no whitespace diagnostics; no tracked whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must master-accept refreshed intake evidence before accepting a future
statement transition. Accountable reviewers must preserve and hash a lawful immutable primary or
approved authoritative source, select and independently approve its exact value or derivative
formula, and transcribe every incorporated definition, ordered binder, hypothesis, contour/domain,
codomain, regularity condition, orientation and winding convention, normalization, conclusion,
proof boundary, correction, erratum, transport, and boundary case. A later statement run can then
encode only that claim, minimize pinned imports, serialize the elaborated expression and
environment, compile each credited transport, and run all four mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
`audit_complete: false` and `theorem_complete: false`; no debt change is proposed. Because the
exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt,
worker `[_]`, or master acceptance is claimed.
