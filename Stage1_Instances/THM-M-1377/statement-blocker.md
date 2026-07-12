# Exact-statement gate: blocked

Item: `S56-M-1377-STATEMENT`

Theorem: `THM-M-1377`

Base revision: `1fc66febfddf404bb914cec34962d66862b96f2b` (tree
`49ae48302378d63f3c54b2a43eeca26433c6b7c5`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only the field label `变分法` (calculus of variations), a collective
seventeenth-century attribution, and the gloss `泛函极值的必要条件` (necessary conditions for
extrema of functionals). It contains no citation, formula, truth-valued proposition, definition,
ordered binder, hypothesis, conclusion, proof boundary, correction, or boundary convention. The
catalog value `已验证` is untrusted metadata under rev-5.6. Stage0 repeats the gloss while explicitly
leaving the formal system, precise definitions and premises, proof route, equivalent statements,
axioms, machine status, and artifacts open.

The omissions are proposition-changing. The record does not fix:

- the functional's domain and codomain, scalar field, ambient topology or smooth structure, or
  admissible class;
- local or global, minimum or maximum, strict or non-strict, interior or boundary extremum
  semantics;
- Frechet, Gateaux, directional, weak, first-variation, or nonsmooth differentiability;
- variations, regularity, constraints and qualification conditions, endpoint or boundary data, or
  quantifier order; or
- derivative-zero, vanishing-first-variation, Euler-Lagrange, multiplier, natural-boundary,
  transversality, subgradient, or another necessary-condition conclusion.

These choices distinguish inequivalent theorems. In particular, the generic Fermat theorem for a
real-valued functional on a normed space, a fixed-endpoint first-variation theorem, a classical
Euler-Lagrange equation, and a nonsmooth multiplier theorem are not alternate spellings of one
claim. `THM-M-1378` separately owns the Euler-Lagrange target, while the direct-method, Tonelli,
least-action, variational-PDE, and mechanics records have their own boundaries. Adopting any such
result would invent, narrow, broaden, or substitute mathematics rather than elaborate this target.

The intake therefore correctly leaves the canonical mathematical statement, Lean module and
expression, minimal imports, expression hash, and target-environment fingerprint null at
`[H5, M4, R4]`. Without a canonical proposition, checked alternate transports and the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined
rather than passed. Creating a predicate or structure field that contains stationarity or the
desired condition would only hide the missing mathematics. No `Statement.lean`, theorem
declaration, axiom, placeholder, assumed condition, weakened special case, or broadened theorem was
introduced. The statement node remains open.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` imports only
`Mathlib.Analysis.Calculus.LocalExtr.Basic`. Re-elaboration checked six adjacent local-extremum and
Frechet-derivative APIs, including `IsLocalMin.hasFDerivAt_eq_zero` and
`IsLocalExtr.fderiv_eq_zero`. It declares no canonical target and has no source-approved transport
from the catalog record. Its successful check is discovery-only environment evidence; the import
cannot be certified minimal for a nonexistent target and receives no statement, anchor, or proof
credit.

A bounded source search found no terminal declaration documented under `calculus of variations`,
`first variation`, or `Euler-Lagrange` in pinned mathlib. Repo-local hits are neighboring legacy
planning and theorem-specific surfaces, including Tonelli and least-action material; none is
source-identical evidence for this target. This is a narrow statement-boundary observation, not the
later immutable anchor audit or a claim of global formal absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The `lean-toolchain`, `lake-manifest.json`, and
`IntakeProbe.lean` SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`861301c97438edfd6fc1c3fd3cd809295550edae5ff47df924b828b70b7ff661`.

The automation-provided `Formalizations/Lean/.lake` link points to canonical pinned artifacts and
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1377` | 0 | rank 987, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped catalog, Stage0, manifest, DAG, intake, crosswalk, scope, and source-history inspection | 0 | only the theorem-family label and gloss are authoritative; all proposition-changing choices remain open |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision, tree, and worktree inspection | 0 | revision and tree agree with the fingerprint; the package worktree was clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1377/IntakeProbe.lean)` | 0 | six adjacent APIs elaborated; no canonical target or proof body was declared; complete output SHA-256 `692f59a579b5b798d94f78d0e08a8fc0225da40d797833f10bba1d4e9d8e07b9` |
| bounded pinned-mathlib Lean search for `calculus of variations`, `first variation`, or `Euler-Lagrange` | 1 | expected no-match exit; discovery only, not an anchor audit |
| bounded repo-local Lean search for the same terms | 0 | found neighboring legacy planning surfaces, not a source-identical target |
| `python3 -B Stage1_Instances/THM-M-1377/check_intake.py` | 1 | the historical intake receipt pins an older blueprint hash; this phase records rather than rewrites historical intake evidence |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-1377` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1377/statement-blocker.json` | 0 | the structured blocker parsed as valid JSON |
| scoped blocker invariant assertions | 0 | IDs, base, open blocked state, null target fields, four undefined mutations, unchanged `H5/M4/R4`, false completion flags, exact two-file scope, and absent self-test agree |
| `git diff --check` plus per-added-file `git diff --no-index --check` | 0 | no whitespace diagnostics in either blocker artifact |
| `test ! -e .stage1-worker-selftest.json` | 0 | the worker self-test manifest is intentionally absent because the exact-statement deliverable did not pass |

The intake prerequisite is provisional worker state `[_]`, not master-accepted `[x]`: its receipt is
unsigned, non-content-addressed, declares `accepted: false`, and has no accepted receipt ID. This
statement attempt is dependency ordered, but dependency acceptance independently remains required
before any future statement transition can be accepted. The historical intake checker now exits at
its stale `Docs/Stage1_Blueprint_rev-5.6.md` receipt hash; adding these blocker artifacts also makes
its intake-only nine-file inventory historical. Neither condition was concealed or repaired by
rewriting the accepted-history surfaces.

## Retry Condition And Status Boundary

First master-accept refreshed intake evidence. Then an accountable source and scope decision must
preserve and hash one immutable theorem-bearing edition, select and independently approve one exact
truth-valued necessary-condition proposition, and transcribe every incorporated definition,
ordered binder, functional and admissibility hypothesis, extremum and differentiability notion,
variation and constraint condition, regularity and boundary datum, conclusion, proof boundary,
correction, erratum, exceptional case, and neighboring-target relationship.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run all four required mutation classes.

First failed gate: exact source-statement identity under rev-5.6 sections 5 and 5.1. This is a
blocked-attempt record, not completion of the statement node or a node-specific receipt. The root
remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt change,
proof credit, worker `[_]`, downstream completion, or master acceptance is claimed. Because the
assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted.
