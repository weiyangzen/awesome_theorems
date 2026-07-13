# Exact-statement gate: blocked

Item: `S56-M-0230-STATEMENT`

Theorem: `THM-M-0230`

Base revision: `f294137feee7840fd105a4d3f6073d5cf45508ea` (tree
`234b8f273d252c2c42ce6860315ed973049c871a`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository record. The statement
item remains `[ ]`. Its prerequisite intake has provisional worker state `[_]`, not
master-accepted state `[x]`; its receipt has `accepted: false`, is not content-addressed, has no
accepted receipt ID, and deliberately leaves the canonical mathematical statement and Lean target
null.

Independently of that dependency boundary, the catalog supplies only the title Weierstrass
factorization theorem and the gloss "infinite-product representation of entire functions." It
contains no bibliography, exact proposition, incorporated definitions, ordered binders, complete
hypotheses, conclusion, proof boundary, correction or erratum mapping, translation review, or
independent source review. The catalog's `verified` label is untrusted metadata under rev-5.6.

The intake records a collected-work bibliographic lead, an associated erratum lead, and a modern
DLMF special-case product. None is an accepted source proposition. In particular, the catalog does
not select either of the two standard roots:

1. construct an entire function with a prescribed locally finite zero divisor; or
2. factor a given nonzero entire function into a power at zero, an exponential of an entire
   function, and a canonical product over its nonzero zeros.

These roots require different binders and conclusions, and their relationship has not been frozen
by a checked source transport. Material choices also remain open: the entire-function predicate;
the identically-zero function; the zero divisor, multiplicities, enumeration and local-finiteness
conditions; separation of the zero at the origin; the primary factor `E_p` and its `p = 0`
convention; the genus sequence and convergence criterion; pointwise versus locally uniform product
semantics; the residual zero-free factor; existence versus equality, converse or uniqueness; and
empty, finite, repeated-zero and accumulation-point boundary cases.

Selecting familiar textbook answers would invent or substitute mathematics rather than elaborate
the exact received target. Rev-5.6 sections 5 and 5.1 make statement ambiguity and a missing
expression fingerprint hard blockers. With no canonical proposition, there is no target import set
to minimize, no elaborated expression or environment-expression fingerprint, no credited
alternate transport, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation. Those outputs are undefined, not passed. The root
vector remains `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` was re-elaborated with its six pinned direct imports. Its nine
checks cover analytic zero order, isolated zeros, locally uniform products, differentiable limits,
finite-support zero/pole extraction, a disk canonical factor, Euler's sine product, `HasProd`, and
`tprod`. The two printed library declarations use only `propext`, `Classical.choice`, and
`Quot.sound`.

This probe defines no Weierstrass primary factor, zero-divisor model, canonical target, alternate
transport, or proof body. `MeromorphicOn.extract_zeros_poles` assumes finite divisor support,
`Complex.canonicalFactor` is a disk/Blaschke factor, and
`Complex.tendsto_euler_sin_prod` treats one special function. None is the unidentified universal
root. A bounded exact-topic search found no matching terminal declaration in pinned mathlib or the
repo-local Lean tree. This is discovery-only evidence, not the downstream immutable anchor audit
or a global absence claim. The probe imports therefore cannot be certified minimal for an absent
target and receive no statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided `.lake` symlink was used
read-only and the mathlib package worktree remained clean. No `lake update`, `lake build`,
dependency clone or fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`). Lean commands ran
from `Formalizations/Lean`; other commands ran from the repository root.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0230` | 0 | rank 1242; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| read-only catalog, Stage0, intake dossier, crosswalk and scope inspection | n/a | the gloss and source leads do not freeze one binder-complete, definition-complete, independently reviewed proposition |
| `lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | 0 | pinned mathlib revision and tree recorded above; package status output empty |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0230/IntakeProbe.lean` | 0 | nine adjacent APIs elaborated; 31 stdout lines, 2721 bytes, SHA-256 `533d3252d8320e72d4f8ec1928df18e4d4ee517f84a3a55a26f7f8d6165b4468`; empty stderr; no canonical target or proof body |
| bounded exact-topic `rg` search recorded in `statement-blocker.json` | 1 | expected no-match result; discovery evidence only, not an exhaustive external audit |
| `python3 -B Stage1_Instances/THM-M-0230/check_intake.py` | 1 | historical intake checker expects original authoritative intake state `[ ]` and attempts 0, while the integrated DAG records provisional `[_]` and attempts 1; historical intake evidence was not rewritten |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-0230/statement-blocker.json`; scoped `jq -e` invariant check | 0 each | structured blocker parses; identity, null target and imports, four undefined mutations, unchanged `H1/M4/R4`, false completion flags, open cut set, and absent self-test agree |
| authority, intake, toolchain, dependency and pinned-source `sha256sum` checks | 0 | fingerprints agree with `statement-blocker.json` |
| `git diff --check -- Stage1_Instances/THM-M-0230`; separate no-index checks for both new files | 0 / 1 each | no whitespace diagnostics; no-index exit 1 is only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest intentionally absent because the exact-statement deliverable did not pass |

## Retry Condition

The integration lane must master-accept refreshed intake evidence before accepting a later
statement transition. Accountable reviewers must preserve and hash a lawful immutable primary or
authoritative source, select one exact construction or given-function factorization proposition,
transcribe every incorporated definition, ordered binder, hypothesis, conclusion, proof boundary,
correction, erratum, translation and boundary case, reconcile the two standard roots, and obtain
independent approval of the source-to-target mapping.

A fresh statement run can then encode precisely that claim, minimize its pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and execute
all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change, statement receipt, worker `[_]`, proof credit, or
master acceptance is claimed. Because the exact-statement deliverable did not pass, no
`.stage1-worker-selftest.json` is emitted.
