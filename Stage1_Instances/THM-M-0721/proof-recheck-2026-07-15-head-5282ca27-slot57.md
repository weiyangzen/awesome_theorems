# THM-M-0721 proof recheck at `5282ca27` (slot57)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T15:45:33+08:00`

Base revision: `5282ca2773644716295f6f2c45f05b380aaa99a2`

Base tree: `ef4d75f68b707c441252dd5a67d8db151b5b4af3`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`.

The checked declaration `root_of_candidate_packages` is conditional composition only. It consumes,
but does not construct, the immediate root cut:

- `M0721-T-SAT-IN-NP`: a faithful binary SAT encoding, correct certificate verifier, polynomial
  certificate bound, and bundled polynomial-time TM2 verifier;
- `M0721-T-UNIVERSAL-HARDNESS`: arbitrary frozen-`InNP` verifier normalization, Cook-Levin
  tableaux, both correctness directions, and a bundled polynomial-time TM2 reduction.

Eleven frozen SAT and Cook-Levin obligations remain open. Their registry entries freeze planned
prose fingerprints rather than exact Lean declaration types; the only exact open terminal
interfaces are `CandidateMembership candidate` and `CandidateHardness candidate`. An append-only
registry refinement is therefore required before concrete leaf bodies can receive proof credit.

Pinned mathlib provides the `TM2ComputableInPolyTime` substrate and identity implementation, but no
NP, SAT-language, or Cook-Levin endpoint. Its apparent polynomial-time composition declaration is
source-level `proof_wanted`; trust-zero Lean reports the would-be constant as unknown. Repo-local and
pinned-mathlib searches found no implementation of either terminal package. The immutable anchor
audit revalidated one supporting-only candidate and two headline candidates that are placeholder-
dependent or contract-incompatible, so none can be imported or transported to the exact target.

Empty, universal, identity, singleton, fixed-source, and classical-choice witnesses do not produce
the universally quantified polynomial-time reductions. A universal encoded-verifier language would
still require machine serialization, a polynomial-time universal TM2, and correctness transports,
which are precisely absent. The first failed gate is `M0721-N-SAT-ENCODING`.

Because the positive proof phase is incomplete, no proof receipt and no
`.stage1-worker-selftest.json` are emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to the canonical pinned
artifacts was reused read-only. No dependency update, build, clone, fetch, checkout, or `.lake`
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink Formalizations/Lean/.lake` | 0 | Base `5282ca2773644716295f6f2c45f05b380aaa99a2`, tree `ef4d75f68b707c441252dd5a67d8db151b5b4af3`; the only initial worktree entry was the automation-provided `.lake` symlink resolving to the canonical artifact directory. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check && python3 scripts/stage1_target.py show THM-M-0721` | 0 | Passed 1546 unique targets at ranks 1 through 1546; THM-M-0721 is rank 578, `planned`, L0/rework-required, with legacy artifacts unaccepted and theorem completion false. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | The exact target elaborated in the pinned Lake environment; expression SHA-256 `758b1033903c92b231a24ae3fb5e01e0bbb0d6fdb0bc41f809c062deb7b4b204` matched and all four structural mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1792cc56322b0f0f3d241a5fa10e02345a66a9f007554978cc932b92a`; root remained open M3 with SAT membership and universal hardness M4. |
| From `Formalizations/Lean`, stream lines 1-95 of `Statement.lean` and lines 9-28 of `ObligationTree.lean` to `LEAN_NUM_THREADS=1 timeout 180s lake env lean --trust=0 -t0 --stdin` | 0 | The exact declarations and conditional composition elaborated; `root_of_candidate_packages` reported exactly `[propext, Quot.sound]` and supplied no terminal-package inhabitant. |
| Scan owned Lean files for `sorry`, `admit`, `axiom`, `unsafe`, `proof_wanted`, or `sorryAx` | 1 expected | No prohibited proof device occurs in owned Lean files. |
| Search other repo-local and pinned-mathlib Lean sources for the exact root, terminal packages, NP-completeness, SAT-language, or Cook-Levin endpoints | 1 expected | No eligible endpoint or terminal-package implementation exists outside this dossier. |
| Ask trust-zero Lean in the pinned Lake environment to `#print axioms Turing.TM2ComputableInPolyTime.comp` | 1 expected | Lean reported `Unknown constant`, confirming source-level `proof_wanted` created no checked declaration. |
| `timeout 180s python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 0 | Local pins and hashes plus all three immutable external candidates matched; the audit retained root classification M2 and supplied no eligible exact proof body. |
| Inspect Lean/Lake and pinned dependency identities and cleanliness | 0 | Lean 4.29.0 at `98dc76e3...740`, Lake 5.0.0, mathlib `8a178386...ea95` tree `bdc39a31...c2b`, and flt-regular `56161b6e...1a27` tree `32c9eace...c893`; both dependency worktrees were clean. |
| `sha256sum` the frozen target and environment inputs | 0 | `Statement.lean`, `ObligationTree.lean`, registry, typed graphs, anchor audit, task DAG, validation specs, statement metadata, toolchain, and Lake manifest all matched their recorded hashes. |
| `python3 -m json.tool Stage1_Instances/THM-M-0721/proof-recheck-2026-07-15-head-5282ca27-slot57.json >/dev/null; git diff --check; test ! -e .stage1-worker-selftest.json` | 0 | The structured handoff parsed, diff hygiene passed, and the completion self-test remained deliberately absent. |

## Reopen Condition

First append-only refine exact Lean signatures for the eleven open proof packages, then implement
their placeholder-free SAT and Cook-Levin bodies; alternatively, identify an immutable compatible
Lean 4 proof already available in the pinned closure and exact-type check, transport, and
provenance-audit it without changing the dependency lock.

This is fresh current-base, warm-cache, nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master acceptance.
