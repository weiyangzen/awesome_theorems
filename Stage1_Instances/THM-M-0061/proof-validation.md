# THM-M-0061 proof-phase validation

Item: `S56-M-0061-PROOF`

Base revision: `771d5d4800fbd95eaaa343e9bc55ebfdde20b364`

Base tree: `a98ba0c37e56a7c04256f7d7df305c88e5cbe76e`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Implemented proof

`Proof.lean` realizes the frozen fiber decomposition, fiber-to-coset transport, left-coset
equivalence, constant-sigma/product equivalence, cardinal product and congruence engines. It feeds
those implementations through every checked composer in `ObligationTree.lean`, obtains arbitrary
group divisibility, specializes to the explicit finite-group scope, and closes the exact frozen
root as `lagrangeDivisibility`.

The separate `lagrangeDivisibility_mathlib` declaration closes the same exact target through the
audited pinned `Subgroup.card_subgroup_dvd_card`. This distinguishes the expanded local M0-L
candidate from the independently checked M0-W pinned-wrapper candidate. `Statement.lean` is
re-elaborated in the same isolated recipe to cover the exact interface, boundary fixtures, and
Fintype transport; these are rechecked inputs rather than new proof bodies in `Proof.lean`.

Lean reports all fourteen proof declarations sorry-free. Every axiom set is contained in
`propext`, `Classical.choice`, and `Quot.sound`. This worker receipt proposes proof closure pending
master acceptance and validation. It does not claim theorem completion, H0, R0, hermetic replay,
independent verification, or release. `M0061-S-FOUNDATION` and the non-proof assurance overlays
remain open.

## Commands and results

Commands ran in this worker clone. The automation-provided canonical `.lake` symlink was reused
read-only; no update, build, clone, fetch, or other dependency mutation command ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure, 15 assurance groups, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546, passed |
| `python3 scripts/stage1_target.py show THM-M-0061` | 0 | rank 1093; planned; L0/rework-required; theorem incomplete |
| `bash Stage1_Instances/THM-M-0061/check_proof.sh` | 0 | isolated Statement, ObligationTree, and Proof elaboration passed; 14 declarations were sorry-free with only the allowed axioms |
| `python3 -B Stage1_Instances/THM-M-0061/check_proof.py` | 0 | item identity, target hash, denominator, source markers, pins, receipt hashes, packet agreement, and status boundary passed |
| `python3 -m json.tool Stage1_Instances/THM-M-0061/proof-receipt.json` and root packet | 0 | both structured artifacts parsed |
| prohibited-construct scan over `Proof.lean` | 1 (expected no match) | no proof gap, new axiom, unsafe/opaque body, native oracle, external implementation, or placeholder |
| `git diff --check -- Stage1_Instances/THM-M-0061 .stage1-worker-selftest.json` plus per-new-file checks | 0 | no whitespace diagnostics |

## Status boundary

The exact root has a self-tested local composition and pinned wrapper, but the accepted instance
remains `H1/M3/R4`. Only the integration lane may accept this proof receipt. Validation, source,
readability, transitive trust/provenance, hermetic/independent replay, `AUDIT-Z`, `THEOREM-Z`, and
release remain separate open gates.
