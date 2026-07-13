# THM-M-0821 anchor-audit validation

Item: `S56-M-0821-ANCHOR_AUDIT`

Base revision: `39704171d88ffcdc33a47365ae9791f855fa3a44`

Base tree: `050ab5c6392560337051d2eadd1b82277dbe1c4f`

Validation date: 2026-07-13 (`Asia/Shanghai`)

## Result

The pinned mathlib revision contains all ingredients for the exact frozen maximum-value target.
`IsAntichain.sperner` proves the universal upper bound. A lower-middle `powersetCard` is an
antichain by `Set.sized_powersetCard.isAntichain`, and `Finset.card_powersetCard` proves that it has
the required binomial cardinality. `AnchorAudit.lean` composes these declarations into
`Stage1Instances.THM_M_0821.spernerMaximum_mathlib_candidate` and independently serializes the
literal target. The checker requires that serialization to have the same SHA-256 as the canonical
statement-phase expression.

The local candidate elaborates in Lean 4.29.0 against mathlib commit `8a178386...a95`. Its
machine-produced axiom set is exactly `propext`, `Classical.choice`, and `Quot.sound`. The relevant
local and pinned sources contain no `sorry`, `admit`, `sorryAx`, bodyless axiom/constant, `opaque`,
or `unsafe` construct after comments are removed. This is a provisional `M0-W` / `E2` candidate,
not accepted root state: the accepted vector remains `[H1, M3, R4]` until dependency-ordered master
acceptance and downstream obligation, proof-composition, trust, validation, and release gates.

## External candidates

The bounded inventory classifies five candidates. Atlas revision `34ffed396...fb50` has two useful
upper-bound routes, but neither contains attainability. `SetSystems.sperner_theorem` is a `Fin n`
wrapper over the same pinned mathlib LYM theorem. `boolean_sperner` uses an abstract
`maxRankCount` interface and lacks a checked transport to the chosen binomial coefficient. Atlas is
not locally pinned and uses a restrictive CC BY-NC/no-training license. It adds no root coverage.

Cam-combi revision `1c8502fd...872d` has a separate LYM inequality proof, not the maximum-value
root, and uses Lean 4.31.0 with a different mathlib revision. Solpin-manai/sperner-lean revision
`3ee6a421...17e` formalizes the different topological Sperner lemma and contains explicit proof
gaps. Formal-conjectures has a related Dedekind-number statement file but no maximum-antichain
theorem and later declarations contain `sorry`.

The general Sourcegraph query reached its 200-match shard limit. GitHub code search returned HTTP
403 and grep.app returned HTTP 429. These failures are recorded rather than counted as negative
evidence. The inventory is fully classified for its frozen version, but discovery saturation is not
claimed.

## Commands and exact outcomes

Commands ran from the repository root unless a different working directory is shown.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0821` | 0 | rank 1379, planned, L0/rework-required, theorem incomplete |
| initial `git status --short --untracked-files=all` | 0 | only the automation-provided untracked `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0821/AnchorAudit.lean)` | 0 | exact candidate, terminal body, and axiom reports elaborated; output SHA-256 `9b7df95ece298a00a837416bfcc3e9c492c90af5f5d256254f7a7d95c83bac23` |
| `python3 -B Stage1_Instances/THM-M-0821/check_anchor_audit.py --worker-packet .stage1-worker-selftest.json` | 0 | five candidates classified; exact pinned mathlib candidate M0-W/E2; accepted root M3; audit/theorem false |
| `python3 -B Stage1_Instances/THM-M-0821/check_anchor_audit.py` | 0 | packet-independent replay passed |
| `python3 -m json.tool` over all new JSON artifacts | 0 | all structured artifacts parsed |
| Python `ast.parse` on `check_anchor_audit.py` | 0 | checker parses without writing bytecode |
| comment-aware prohibited-construct check over `AnchorAudit.lean` and three pinned source files | 0 | no prohibited construct found |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree matched and dependency worktree was clean |
| repo-local and pinned-mathlib `rg` queries recorded in the audit | 0/1 as appropriate | no other local exact wrapper; the only Sperner-named pinned terminal is `IsAntichain.sperner` |
| Sourcegraph, GitHub REST, immutable commit/tree/raw-source, and other-prover queries recorded in the audit | 0 at transport layer | bounded results, immutable revisions, response hashes, and access failures recorded |
| `git diff --check -- Stage1_Instances/THM-M-0821 .stage1-worker-selftest.json` plus no-index checks for new files | 0 aggregate | no whitespace errors |

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.

## Known failures

- The statement prerequisite and this node still require dependency-ordered master acceptance.
- Discovery is bounded rather than exhaustive because public search surfaces imposed limits.
- The obligation registry, typed graphs, and proof-phase composition receipt are not frozen.
- Full transitive declaration/provenance/trust and TCB closure is not accepted.
- Human-source H0, readable R0, hermetic replay, independent verification, deterministic release
  evidence, `AUDIT-Z`, and theorem completion remain open.

This completes only the assigned anchor-inventory and candidate-check work pending master
acceptance. It does not claim accepted M0, the downstream proof phase, audit completion, or theorem
completion.
