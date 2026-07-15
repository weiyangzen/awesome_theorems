# THM-M-1105 proof recheck at a23d86cd (slot62)

Item: `S56-M-1105-PROOF`

Intent: `prove`

Recorded: `2026-07-15T09:12:45+08:00`

Base revision: `a23d86cd84f03c26102b43c6b1b3b6d0a7a31e61`

Base tree: `9268aa9f5379837642b6f748f01255e8744c4e78`

## Verdict

`blocked`. No placeholder-free body for the exact canonical target
`Stage1.THM_M_1105.WignerSemicircleLaw` exists in the owned sources, the scoped
repository-local Lean sources, or the pinned mathlib closure. This recheck adds no Lean proof body,
closes no obligation, and leaves the root at `[H2, M3, R4]`. It does not satisfy the proof item or
claim audit completion, theorem completion, validation, release, receipt acceptance, or master
acceptance.

All 20 machine-required obligations in the frozen registry still have
`terminal_proof_body_id: null`. The only checked local theorem,
`Stage1.THM_M_1105.ObligationTree.root_of_sample_weak_convergence`, consumes
`terminal : forall-almost-everywhere omega, SampleWeakConvergence A hA_hermitian omega`. That
premise is the missing analytic conclusion; the theorem is conditional composition, not a proof of
`M1105-T-WEAK`, `M1105-T-COMPOSE`, or the root.

The graph-derived root cut remains `M1105-L-NONPAIR`, `M1105-L-PAIRING`,
`M1105-L-CONCENTRATION`, `M1105-L-TIGHTNESS`, and `M1105-L-BC-APPROX`. Completing the route also
requires trace expansion, parity and walk classification, independence cancellation, Catalan
enumeration, expected and almost-sure moment convergence, semicircle moments, polynomial
extension, and final weak convergence. Supplying any of these as an assumption, axiom, bodyless
declaration, or `sorry` would be a prohibited placeholder.

## Candidate And Freshness Recheck

Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` still provides only supporting
Hermitian-spectrum, trace, independence, integration, and weak-convergence APIs. Its sole topical
source match is the unrelated geometric semicircle comment in Thales' theorem. A repository-local
exact-interface scan outside this dossier returned no matches, and reachable Lean history contains
only this target's statement, anchor audit, and conditional obligation tree.

The prerequisite immutable audits remain decisive. `semicircle-catalan@95d99de4` supplies finite
Catalan/genus-zero combinatorics only, HighDimProb supplies infrastructure only, and
`FredRaj3/SemicircleLaw@724f9ad6` has 25 `sorry` tokens, no almost-sure weak empirical-spectral
terminal, and a different ensemble and convergence mode. None is an eligible body in the pinned
dependency closure.

No proof-relevant target input changed after the original proof execution at `270e3fb3`: current
hashes of `Statement.lean`, `ObligationTree.lean`, the frozen registry, typed graphs, and anchor
inventory are unchanged. The current scheduler projection nevertheless records `attempts: 0` and
`children: []`, while the owned path contains repeated unresolved proof blocker runs. Rev-5.6
section 10.2 requires splitting the item after five unresolved ticks. This worker may not edit
the scheduler DAG or broaden its assignment, so that workflow inconsistency is reported for master
reconciliation rather than silently changed.

## Smallest Real Validation

All Lean checks reused the automation-provided canonical `.lake` symlink read-only. No
`lake update`, `lake build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed. The untracked symlink makes this warm, nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1105` | 0 | Rank 545; planned; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1105/check_obligation_tree.py` | 0 | 22 obligations and 108 typed edges passed; denominator `409c3f4a...26f0e`; root explicitly open at M3. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-1105/Statement.lean` | 0 | The exact canonical proposition elaborated; Lean emitted only the expected unused-hypothesis linter warnings. |
| Same trust-zero command for `ObligationTree.lean` | 0 | The conditional terminal-to-root composition elaborated; its printed type includes the explicit terminal premise. |
| Stdin trust-zero `#print axioms` probe of the composition | 0 | The report was exactly `propext`, `Classical.choice`, and `Quot.sound`; no repository artifact was written. |
| Token-anchored prohibited-construct scan over owned `*.lean` files | 1 | Expected no-match exit; no `sorry`, `admit`, `sorryAx`, bodyless axiom-like declaration, unsafe/oracle path, or equivalent prohibited construct was found. |
| Pinned-mathlib topical source scan | 0 | The only match was Thales' unrelated geometric semicircle comment; no random-matrix terminal exists. |
| Repository-local exact-interface scan outside this owned path | 1 | Expected no-match exit; no reusable body for the target or terminal interface was found. |

Lean is version `4.29.0` at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`;
Lake is `5.0.0-src+98dc76e`; mathlib is `8a178386...ea95`, tree
`bdc39a31...1c2b`. Proof-relevant SHA-256 values and the complete command ledger are in the paired
JSON artifact.

## Retry Condition

Resume after placeholder-free implementations of the frozen trace-moment, walk-classification,
non-pairing, pairing, concentration, almost-sure moment, semicircle-moment, tightness,
polynomial-approximation, bounded-continuous approximation, and weak-convergence packages. The
only alternative is an immutable exact-scope Lean 4 terminal theorem that can be dependency-legally
pinned, exact-type transported, and provenance/trust validated without changing the target.

This current-base artifact is a nonrelease blocker handoff, not a proof receipt. Because the
assigned proof phase is not genuinely self-tested as complete, `.stage1-worker-selftest.json` is
deliberately absent.
