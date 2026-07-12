# Validation-phase evidence

Item: `S56-M-0648-VALIDATION`

Base revision: `734cdf53ab1cc41c766d2a40058a1929f6e1311a`.

The worker reran the frozen statement and proof with the pinned Lean toolchain. A separate
`Validation.lean` module reconstructs both theorem directions directly from the two pinned mathlib
terminal declarations without importing `Proof.lean`. The Python verifier independently checks
input hashes, the full frozen machine denominator, reciprocal graph edges, local placeholder and
trust boundaries, terminal source hashes and revision, elaboration, and kernel axiom reports.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets pass |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0648` | exit 0; rank 694, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0648/Statement.lean` | exit 0; exact paired proposition printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0648/Proof.lean` | exit 0; axioms `propext`, `Classical.choice`, `Quot.sound` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0648/Validation.lean` | exit 0; independent paired proof has the same three-axiom profile |
| `python3 Stage1_Instances/THM-M-0648/check_validation.py` | exit 0; exact root, probe, pins, graph, provenance, trust, and open release boundary agree |

No dependency update, build, clone, fetch, or network access occurred. The pre-existing `.lake`
symlink points to the canonical pinned artifacts and was not modified.

This is warm worker evidence, not release-grade validation. Section 10.6 fails first because no
new checkout, empty-cache cold build, or offline archive replay is available under the worker
contract. Section 10.7 also remains open: the separate proof is not a distinct signed verifier on
an independently provisioned runner. H0/R0 reviews, supply-chain evidence, protected CI, mutation
tests, signed attestations, and a deterministic release bundle are also missing. Therefore
`audit_complete=false` and `theorem_complete=false`; only provisional worker validation is claimed.
