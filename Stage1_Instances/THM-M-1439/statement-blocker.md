# Exact-statement gate: blocked

Item: `S56-M-1439-STATEMENT`

Theorem: `THM-M-1439`

Base revision: `a8aba97a7ef2ff387e7814fe517e1b35524a04dc` (tree
`495e962862c2e7bc7c33c880c06fe39b2cb75db6`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1439-INTAKE` has provisional worker
state `[_]`; that permits this statement attempt, but master acceptance remains required before
any eventual accepted statement transition.

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The record supplies only the proof label `Lyubich证明` ("Lyubich proof"), Mikhail Lyubich, the year
1999, and the gloss `Feigenbaum猜想的解析证明` ("an analytic proof of the Feigenbaum conjecture"). It
supplies no truth-valued proposition, citation, definition chain, ordered binders, hypotheses, or
conclusion. The catalog status `已验证` is untrusted metadata under rev-5.6.

The exact-match source identified at intake is Mikhail Lyubich, *Feigenbaum-Coullet-Tresser
universality and Milnor's Hairiness Conjecture*, *Annals of Mathematics* (2) 149 (1999), 319-420,
DOI `10.2307/120968`, arXiv `math/9903201v1`. The intake records an immutable PDF SHA-256 of
`8e32496391ceed7fa03e5ac5846ded6ecff1b379a01032444fac05c649bca9e0`. That source confirms the
result family, but it does not resolve which member the catalog intends.

In particular, the paper distinguishes at least these inequivalent candidate roots:

- the three-clause Hyperbolicity Theorem for the real bounded-type renormalization horseshoe;
- the stationary fixed-point and hyperbolicity result, including its original period-doubling
  specialization;
- a stationary Universality Theorem for asymptotic scaling in transverse analytic families;
- a separate bounded-combinatorics scaling and transverse-family result; and
- a larger package containing hairiness, self-similarity, universality, Hausdorff-dimension, and
  quasiconformal conclusions.

The Hyperbolicity Theorem itself includes shift conjugacy and uniform hyperbolicity, stable leaves
identified with codimension-one hybrid classes, and analytic unstable curves transverse to the real
hybrid classes other than the cusp. The Universality statements instead quantify parameter
families and assert asymptotic scaling. Selecting one, one clause, or their conjunction changes the
root, definitions, binders, assumptions, conclusions, and boundary cases. It could also merge this
target with `THM-M-1437` (Feigenbaum universality) or `THM-M-1438` (Lanford proof).

No accountable source correction or independent review has selected a canonical root, mapped all
incorporated definitions and assumptions, checked corrections and errata, or approved the neighbor
boundaries. Choosing from memory would therefore invent or substitute missing mathematics.

Section 5 of the rev-5.6 standard makes statement ambiguity and a missing expression fingerprint
hard blockers. Without a canonical proposition, there is no exact Lean expression on which to
certify minimal imports, serialize an elaborated expression and environment fingerprint, compile
alternate transports, or run the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations. Those four mutation classes are undefined, not
passed. No surrogate theorem, convenient special case, axiom, placeholder, broadened interface, or
proof body was added.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` directly imports five pinned mathlib modules and successfully
re-elaborates eleven adjacent complex, analytic, iteration, semiconjugacy, compactness,
connectedness, and continuous-linear-map interfaces. It defines no quadratic-like germ, hybrid
class, or renormalization operator and states no Lyubich theorem. Its imports therefore cannot be
called minimal for an unknown target, and the successful run supplies no statement, anchor, or
proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The `lean-toolchain`, `lake-manifest.json`, target
manifest, current blueprint, execution DAG, execution skill, and probe SHA-256 values are recorded
in `statement-blocker.json`.

The automation-provided `Formalizations/Lean/.lake` link points to the canonical pinned artifacts
and was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1439` | 0 | rank 937, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all; git rev-parse HEAD; git rev-parse 'HEAD^{tree}'; readlink Formalizations/Lean/.lake` | 0 | only the automation-provided `.lake` link was untracked; the recorded base revision and tree were otherwise clean |
| source record, Stage0, manifest, blueprint, and intake dossier inspection | 0 | only a proof label and gloss exist; the intake leaves the canonical claim and formal target null and records inequivalent source-result roots |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1439/IntakeProbe.lean` | 0 | all eleven adjacent pinned APIs elaborated; no canonical target was stated |
| pinned mathlib revision, tree, and status inspection | 0 | revision and tree match the recorded fingerprint; package worktree clean |
| bounded Feigenbaum/Coullet/Tresser/Lyubich/quadratic-like/hybrid-class name search in repo-local and pinned-mathlib Lean sources | 1 | expected no-match exit; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-1439/check_intake.py` before adding blocker artifacts | 1 | known phase-evolution failure at its first assertion: the historical intake checker expects the execution-DAG intake item to remain `[ ]`, while the current blueprint and execution DAG record provisional `[_]`; its closed inventory would also reject later-phase artifacts |
| `python3 -m json.tool Stage1_Instances/THM-M-1439/statement-blocker.json` | 0 | structured blocker parsed as JSON |
| `python3 - Stage1_Instances/THM-M-1439/statement-blocker.json` with the recorded inline JSON assertions | 0 | item identity, null target and imports, four undefined mutations, unchanged debt vector, false completion flags, changed paths, and no-self-test boundary agree |
| prohibited Lean proof-escape scan over `Stage1_Instances/THM-M-1439` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped tracked and added-file whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

The historical `check_intake.py` is intake-only evidence. This statement run does not rewrite its
expected DAG state, closed file inventory, historical receipt, or input hashes merely to
manufacture agreement.

## Retry Condition And Status Boundary

The integration lane must accept the intake dependency before an eventual accepted statement
transition. Accountable reviewers must preserve the immutable primary edition, select and
transcribe one exact catalog-root proposition and every incorporated definition with pinpoint
locators, freeze every stationary or bounded-type, quadratic-like-germ, renormalization,
hyperbolicity, hybrid-class, transversality, scaling, binder, conclusion, and boundary choice,
check corrections and errata, justify separation from `THM-M-1437` and `THM-M-1438`, and
independently approve the source-to-target mapping. A later statement worker can then encode that
same claim, minimize its pinned imports, serialize and hash the elaborated expression and
environment, check alternate transports, and run all four required mutation classes.

The first failed gate is exact source-statement identity. The root remains `[H5, M4, R4]`, with
`audit_complete: false` and `theorem_complete: false`; no debt-vector change is proposed. This is
blocked-attempt evidence, not completion of the statement node or any downstream node. Because the
assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted and no statement receipt, worker `[_]`, or master
acceptance is claimed.
