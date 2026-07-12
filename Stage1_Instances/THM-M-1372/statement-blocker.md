# Exact-statement gate: blocked

Item: `S56-M-1372-STATEMENT`

Theorem: `THM-M-1372`

Base revision: `7a489588a59dbd7cca44de7e3b8c3bafcb7448f5` (tree
`54d558bf8ed3ea71536ff6a7e6ac7ee67cccfe98`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
That record supplies only `Nekhoroshev estimate`, Nikolai Nekhoroshev, 1977, and the gloss
`exponential stability of nearly integrable systems`. It supplies no cited proposition,
definition, ordered binder, hypothesis, conclusion, proof boundary, correction, or boundary case.
Stage0 explicitly leaves the formal system, exact definitions and premises, proof route,
equivalent statements, axioms, machine status, and artifacts open. The catalog value `verified` is
untrusted metadata under rev-5.6.

The wording identifies a theorem family, not one proposition. Nekhoroshev's 1977 main Theorem 4.4
is the historically matching primary lead, but it has a detailed analytic steep-Hamiltonian
contract and a proof boundary extending into Part II. Its introductory Theorem 1.4 expressly says
it is not completely accurate. Poeschel's analytic quasi-convex theorem, later analytic or Gevrey
quasi-convex estimates, and finitely differentiable variants use materially different
nondegeneracy, domain, norm, radius, and time contracts. The catalog neither cites the 1977 paper
nor selects any of these results.

There is also a non-covered physics record, `THM-P-0775`, with the stronger but still incomplete
wording that actions remain stable for exponentially long times. No accepted alias,
deduplication, or canonical-root ownership decision exists. It cannot select the statement or
transfer source, machine, or readability credit.

Choosing the original main theorem, its approximate introduction, a quasi-convex or weaker-
regularity variant, or the duplicate's wording would invent, narrow, broaden, or substitute
mathematics rather than elaborate the exact received target. The intake therefore correctly leaves
the canonical human statement, Lean module and expression, minimal imports, and canonical
expression and environment fingerprints null at `[H1, M4, R4]`. Without a canonical target,
checked alternate transports and the required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary-case mutations are undefined rather than passed. No
`Statement.lean`, axiom, placeholder, assumed stability field, weakened special case, or broadened
theorem was introduced.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated with the pinned environment. Its four direct
imports expose five adjacent analyticity, integral-curve, global-flow, real-power, and exponential
interfaces, all of which elaborate. The probe defines no action-angle Hamiltonian, analytic
complex domain, perturbation norm, steepness or quasi-convexity contract, Hamiltonian trajectory,
action-drift estimate, or source-selected conclusion. Its imports therefore cannot be certified
minimal for an absent canonical target, and the successful check receives no statement, anchor, or
proof credit.

A bounded exact-topic search in repo-local Lean and pinned mathlib found no Nekhoroshev declaration
under the recorded spellings. This is narrow discovery evidence, not the downstream immutable
anchor audit or a claim of global absence.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The `lean-toolchain`,
`lake-manifest.json`, and probe SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`,
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`, and
`895c56da5ae725af1c409168a3f7c729332cd5b1a68d2b220660e6fea8f11de9`.

The automation-provided `Formalizations/Lean/.lake` link points to canonical pinned artifacts and
was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1372` | 0 | rank 982, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped catalog, Stage0, manifest, DAG, intake, crosswalk, scope, and source-lead inspection | 0 | only the theorem-family label and gloss are authoritative; all proposition-changing choices remain open |
| `sha256sum` over authority, intake, toolchain, and pinned mathlib inputs | 0 | hashes agree with `statement-blocker.json` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| pinned mathlib revision, tree, and worktree inspection | 0 | revision and tree agree with the fingerprint; the package worktree was clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1372/IntakeProbe.lean` | 0 | five adjacent APIs elaborated; no canonical target or proof body was declared; stdout SHA-256 `eaa5a19a23fe7d1a5ab1d305b0692aa635d17edb13c93b39c6d4b095c2639128` |
| bounded repo-local and pinned-mathlib Lean search for Nekhoroshev spellings | 1 | expected no-match exit; discovery only, not an anchor audit |
| `python3 -B Stage1_Instances/THM-M-1372/check_intake.py` | 1 | the historical intake receipt pins an older blueprint hash; this phase records rather than rewrites historical evidence |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-1372` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1372/statement-blocker.json` | 0 | the finalized structured blocker parsed as JSON |
| scoped statement-blocker invariant assertions | 0 | IDs, open state, null target and imports, four undefined mutations, unchanged debt, false completion flags, exact paths, and absent self-test agree |
| whitespace checks for both added blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

The intake prerequisite has provisional worker state `[_]`, not master-accepted state `[x]`. Its
receipt explicitly has `accepted: false` and no accepted receipt ID. Rev-5.6 section 10.2 permits
this dependency-ordered attempt, but dependency acceptance independently remains necessary before
a future statement transition can be accepted. The first substantive failure is the missing exact
source statement and variant selection.

## Retry condition

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
preserve and hash one lawful complete primary or authoritative source, select and independently
approve one exact proposition, and issue an accepted `THM-P-0775` identity and canonical-root
ownership decision. They must transcribe every incorporated definition, ordered binder,
Hamiltonian and domain hypothesis, regularity and nondegeneracy contract, perturbation norm and
threshold, trajectory convention, constant dependency, exact drift and time conclusion, complete
Part I/II proof boundary, correction, and boundary case.

A later statement worker can then encode that same claim using real Lean definitions, minimize its
pinned imports, serialize and hash the elaborated expression and environment, check every credited
transport, and run all four mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H1, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, node receipt, worker `[_]`, or master acceptance is claimed.
