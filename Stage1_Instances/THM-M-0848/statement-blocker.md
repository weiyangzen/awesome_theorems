# Exact-statement gate: blocked

Item: `S56-M-0848-STATEMENT`

Theorem: `THM-M-0848`

Base revision: `748243faadc15828fb087059337fd05b7be9fdeb` (tree
`e46d642646f80980838b6f016f5d69b817bd464d`).

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The record gives the label `Erdos-Renyi random graph`, attributes it to Erdos and Renyi in 1959,
and supplies only the gloss `basic theory of the random-graph model`. It cites no exact result and
provides no definition, ordered binder, hypothesis, conclusion, proof boundary, correction, or
erratum. Stage0 explicitly leaves precise definitions and premises open, and the catalog's
`verified` label is untrusted under rev-5.6.

The missing choices are proposition-changing. Erdos and Renyi's *On Random Graphs I* defines the
uniform fixed-edge model now written `G(n, m)` and states four distinct asymptotic result families.
The independent-edge `G(n, p)` law associated with Gilbert is also commonly called the
Erdos-Renyi model. A definition of either law, a singleton-mass or independence result, a coupling,
and the connectivity, component, or stopping-time conclusions are not interchangeable theorems.
The catalog selects none of them.

The repository also gives separate ownership to phase transition (`THM-M-0849`), the giant
component (`THM-M-0850`), the connectivity threshold (`THM-M-0851`), and the Hamilton-cycle
threshold (`THM-M-0852`). `THM-M-1112` is a separate near-duplicate unresolved random-graph record.
Selecting one of these conclusions, choosing `G(n, p)` because pinned mathlib exposes it, or
stating only that a graph law exists would substitute or narrow the assigned target.

Sections 5 and 5.1 of the rev-5.6 blueprint make statement ambiguity and a missing expression
fingerprint hard blockers. The intake therefore leaves the canonical human statement, Lean module
and expression, minimal imports, ordered binders and hypotheses, and expression/environment
fingerprints null at `[H5, M4, R4]`. Without a canonical target, checked alternate transports and
the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations
are undefined, not passed. No `Statement.lean`, theorem declaration, axiom, placeholder, assumed
random-graph property, broadened family assertion, or weakened special case was introduced.

The prerequisite `S56-M-0848-INTAKE` is also only provisional worker state `[_]`, not
master-accepted `[x]`. Rev-5.6 section 10.2 permits preparation of this later-node blocker, but
master closure remains dependency ordered.

## Pinned Lean Boundary

The existing `IntakeProbe.lean` directly imports
`Mathlib.Probability.Combinatorics.BinomialRandomGraph.Defs` and successfully re-elaborates nine
adjacent `G(V, p)` graph and measure interfaces. That pinned mathlib module itself notes that the
historical Erdos-Renyi model is closely related but different. The probe states no target theorem,
selects no source result, and contains no proof body. Its import is a discovery candidate only and
cannot be certified minimal for a target that does not exist.

A bounded search of repository-local and pinned-mathlib Lean sources located only this binomial
random-graph infrastructure and its unfinished desired edge-count result, not a source-frozen
`THM-M-0848` proposition. This is statement-feasibility evidence, not the downstream formal-anchor
audit or a global absence claim.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The SHA-256 values of `lean-toolchain`,
`lake-manifest.json`, the mathlib binomial-random-graph definitions, the intake probe, and the
probe's complete stdout are, respectively:

- `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`;
- `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`;
- `c8effb70a7e4605a077198e04a771ecc8cba255a2243de9cd76a162788766dc7`;
- `de1f34de50979dc6ae2fd26b5f0a69400e30c1912a28b88a806a25b0921f92df`; and
- `0872fce82a29f2fb8ce53604c2de1c8104d707b29f5ca1ccf3235b271c489215`.

The automation-provided `Formalizations/Lean/.lake` link points to the canonical pinned artifacts
and was used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake`
mutation was run.

## Validation Evidence

Commands ran in this worker clone on 2026-07-13 (Asia/Shanghai), from the repository root unless a
different working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0848` | 0 | rank 1403, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` link was untracked; base revision and tree are recorded above |
| scoped manifest, blueprint, skill, catalog, Stage0, intake, scope, and crosswalk inspection | 0 | only a model-family label and gloss are authoritative; every proposition-changing choice remains open |
| `sha256sum` over authority, intake, toolchain, lockfile, probe, and pinned mathlib inputs | 0 | current fingerprints were recorded in `statement-blocker.json` |
| `python3 -B Stage1_Instances/THM-M-0848/check_intake.py` | 1 | historical intake replay freezes the pre-integration authoritative intake state `[ ]`; the current DAG records `[_]`, so this phase records rather than rewrites that historical evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake agree with the pinned environment above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision and tree agree with the fingerprint; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0848/IntakeProbe.lean` | 0 | nine adjacent `G(V, p)` APIs elaborated; complete stdout SHA-256 is `0872fce...9215`; no canonical target was stated |
| bounded exact-topic search in pinned mathlib and repo-local Lean | 0 | only binomial-random-graph infrastructure and its unfinished desired result were located; discovery only |
| prohibited Lean construct scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, axiom, bodyless declaration, or unsafe declaration |
| JSON parse and scoped invariant check for `statement-blocker.json` | 0 each | IDs, open state, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact paths, and absent self-test agree |
| whitespace checks for both added blocker artifacts | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | no worker self-test manifest exists because the exact-statement deliverable is blocked |

## Retry Condition

The integration lane must first master-accept refreshed intake evidence. Accountable reviewers must
then preserve and hash one immutable primary or approved authoritative source, select and
independently approve one exact numbered result (or explicitly justify a different exact claim as
the catalog root), and transcribe every incorporated definition, ordered binder, hypothesis,
conclusion, limiting regime, proof boundary, correction, erratum, and boundary case. They must
resolve `G(n, m)` versus `G(n, p)`, labelled versus unlabelled graphs, probability encoding,
parameter ranges, equality versus isomorphism, small and endpoint cases, neighboring targets
`THM-M-0849` through `THM-M-0852`, and duplicate `THM-M-1112`.

A fresh statement worker can then encode precisely that source-selected claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This is a blocked-attempt record, not completion of the statement node or any downstream node. The
root remains `[H5, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`; no debt
change is proposed. Because the assigned phase is not genuinely self-tested to its completion gate,
no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or master acceptance is claimed.
