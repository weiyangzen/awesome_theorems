# THM-M-0312 validation-phase evidence

Item: `S56-M-0312-VALIDATION`  
Base revision: `230f719da7724afb27c761dcb8c62a327557fe63`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The narrow worker gate passed. In a fresh temporary target directory, pinned Lean elaborated the
frozen statement, conditional composition, both proof interfaces, the composed exact root, the
pinned public wrapper, and a separately implemented exact-root reconstruction. `Validation.lean`
imports neither `Proof` nor `ObligationTree`. Every proof-bearing declaration reported exactly
`propext`, `Classical.choice`, and `Quot.sound`. Source hygiene, content hashes, registry identity,
the clean mathlib revision, and terminal source hashes also passed.

This is nonrelease evidence. It reused the canonical shared warm `.lake` symlink; there was no cold
empty-cache offline restoration, complete transitive TCB/SBOM archive, distinct runner, second
attestation, or independently implemented release verifier. The frozen graph retains pre-proof
candidate state and open foundation/provenance/source nodes pending master reconciliation. H0 and
independently reviewed R0 are open. No accepted M0, E0/E1, audit completion, theorem completion,
release, or master acceptance is claimed.

## Commands and exact outcomes

All commands ran from the repository root. No `lake update`, `lake build`, dependency fetch/clone,
network access, or `.lake` mutation was performed.

| Command | Exit | Outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546, passed. |
| `python3 scripts/stage1_target.py show THM-M-0312` | 0 | Rank 814, planned, L0/rework-required, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0312/check_validation.py` | 0 | Kernel replay, exact axiom sets, hashes, registry, dependency pin/source identity, and differential reconstruction passed; release gates failed closed. |
| `python3 Stage1_Instances/THM-M-0312/check_statement.py` | 0 | Exact expression, mutations, boundary, environment, and pins passed. |
| `python3 Stage1_Instances/THM-M-0312/check_obligation_tree.py` | 0 | 15 obligations, 28 typed edges, and frozen denominator passed; pre-proof open boundary retained. |
| `python3 -m json.tool` on `validation-spec.json` and `validation-receipt.json` | 0 | Both validation records are valid JSON. |
| Placeholder scan over four Lean modules | 1 | Expected no-match result for `sorry`, `admit`, `sorryAx`, added `axiom`, or `unsafe`. |
| `git diff --check -- Stage1_Instances/THM-M-0312 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, interface proofs, composition, local exact root, pinned root, and differential exact root elaborate. |
| Placeholder and unsafe scan | pass | Checked source has no prohibited proof shortcut or unsafe declaration. |
| Axiom observation | provisional pass | All proof-bearing declarations report only the three disclosed axioms; full TCB acceptance is not inferred. |
| Local provenance | pass | Inputs, frozen denominator, mathlib pin/cleanliness, and terminal source hashes agree. |
| Same-worker differential reconstruction | pass with boundary | A separately implemented root imports only `Statement`; this is not a distinct runner. |
| Authoritative structured state | fail closed | Candidate nodes and the foundation/provenance/source cut set await master reconciliation. |
| Human source/readability | fail closed | Primary-source H0 and independently accepted R0 are absent. |
| Hermetic release replay | fail closed | Shared warm cache; no immutable cold offline replay or complete supply-chain bundle. |
| Independent verification | fail closed | No distinct provisioned runner, second signature, or independently implemented release verifier. |

## Status boundary

The validation node is self-tested pending master acceptance. The first failed node gate is
`structured.authoritative_state_reconciliation`; the first release-grade failure is
`hermetic.cold_empty_cache`. The later release phase must decide every remaining completion gate.
