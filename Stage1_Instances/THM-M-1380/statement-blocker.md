# THM-M-1380 exact-statement gate: blocked

- Item: `S56-M-1380-STATEMENT`
- Base revision: `b1a4a17bfdfd6017fdd207976661c2c83972f96a` (tree
  `93a1f5755e2a734de8e46cd6125a2566eb8a7892`)
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt, worker `[_]`, or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully entered from the authoritative record. The mathematics catalog supplies only the name
"Jacobi theorem," the attribution and year, and the gloss "a complete solution of the
Hamilton-Jacobi equation." It gives no formula, cited truth-valued proposition, incorporated
definitions, ordered binders, hypotheses, conclusion, or boundary cases. Stage0 explicitly leaves
the precise definitions, premises, equivalent forms, axioms, machine status, and artifacts open.
The catalog's `已验证` value is untrusted metadata under rev-5.6.

The wording identifies a theorem family, not one theorem. It does not choose whether the root is a
complete-integral-to-Hamiltonian-trajectories theorem, a canonical-transformation theorem, the
chain-rule result for one Hamilton-Jacobi solution, an autonomous separated-solution theorem, an
existence theorem, or a reviewed conjunction. These alternatives require materially different
configuration and phase spaces, Hamiltonian and generating-function data, regularity,
time-dependence, parameter dimensions, mixed-derivative nondegeneracy, locality, sign conventions,
binders, hypotheses, and conclusions. Selecting one from convention would invent, narrow, broaden,
or substitute mathematics rather than elaborate the received target.

The intake's historical and modern discovery leads converge only on the general family. Jacobi's
1837 Crelle article, the Encyclopedia of Mathematics description, Samelson's 2001 article, and
Tong's notes do not constitute a catalog-selected, fully transcribed, correction-audited, and
independently reviewed exact source statement. Nor may "complete solution" silently become an
unconditional global-existence claim: global smooth complete integrals can fail due to
singularities, caustics, topology, or lack of integrability. A structure that assumes the complete
integral as data would only move the desired premise into an interface.

Consequently there is no canonical expression to elaborate, no honest minimal-import claim, and no
canonical expression or environment fingerprint. Checked transports and the required
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations are undefined
until a source-correct statement fixes binders and premises. The intake vector remains
`[H5, M4, R4]`; no debt change is proposed. No `Statement.lean`, axiom, placeholder, assumed
complete integral, or substituted theorem was introduced.

The intake prerequisite is only provisional `[_]`, and its worker receipt is not accepted. This
independently prevents statement-node acceptance. Its replay validator is also stale against the
current blueprint hash; this phase does not rewrite historical intake evidence to manufacture
freshness. The first statement-specific failure is the absent exact source proposition.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its four imports
expose adjacent smoothness, Frechet-derivative, product-map, and integral-curve APIs, and all seven
`#check` commands passed. The probe states no Hamilton-Jacobi proposition, and its imports cannot be
certified minimal for an unidentified target. This check receives no statement, anchor, or proof
credit.

A bounded case-insensitive search of repo-local Lean and pinned mathlib located no Hamilton-Jacobi
target. The only `complete integral` result was the unrelated commutative-algebra
`completeIntegralClosure` API. This is narrow feasibility evidence, not the downstream immutable
anchor audit or a global absence claim.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided
`Formalizations/Lean/.lake` symlink points to the canonical pinned artifacts and was used read-only.
No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown. Exact argument arrays and results are preserved in
`statement-blocker.json`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1380` | 0 | rank 990, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree are recorded above |
| scoped reads of the catalog, Stage0, target manifest, generated item projection, and six named intake artifacts | 0 | only a complete-solution family gloss is authoritative; every proposition-changing choice remains open |
| exact `sha256sum` invocation recorded in `statement-blocker.json` | 0 | current authority, source, intake, toolchain, manifest, and probe hashes are recorded |
| `python3 -B Stage1_Instances/THM-M-1380/check_intake.py` | 1 | historical intake replay stopped at its stale blueprint hash; this phase did not rewrite intake evidence |
| `cd Formalizations/Lean && lake env lean --version` and `lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | revision and tree agree with the fingerprint; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1380/IntakeProbe.lean` plus the exact combined-output hash pipeline | 0 each | all seven adjacent APIs elaborated; output SHA-256 `b319d6c1...f247`; no canonical target was stated |
| two bounded exact-topic `rg` searches recorded in `statement-blocker.json` | 0, 1 | the first found only unrelated commutative algebra; the second expected no-match result found no Hamilton/Jacobi co-occurrence |
| prohibited Lean construct scan over owned `*.lean` files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1380/statement-blocker.json` | 0 | structured blocker parses as JSON |
| scoped invariant and whitespace checks recorded in `statement-blocker.json` | 0 | identity, null target, undefined mutations, unchanged debt, false completion flags, exact path scope, absent self-test, and clean whitespace agree |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must then
preserve and hash one immutable primary or approved authoritative source, select and transcribe one
exact truth-valued claim and all incorporated definitions with pinpoint locators, audit corrections
and errata, reconcile the mathematical target with `THM-M-1379`, `THM-M-1547`, and neighboring
mechanics targets, and independently approve the source-to-statement mapping. The decision must
freeze the claim kind, time convention, configuration and phase spaces, Hamiltonian and generating-
function domains, complete-integral and derivative notions, regularity, nondegeneracy, ordered
binders, hypotheses, conclusion, every degenerate or boundary case, and every sign convention.

A later statement worker can then encode precisely that claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and run all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node.
`audit_complete` and `theorem_complete` remain false. Because the assigned phase is not genuinely
self-tested to its completion gate, no `.stage1-worker-selftest.json`, node receipt, worker `[_]`,
or master acceptance is claimed.
