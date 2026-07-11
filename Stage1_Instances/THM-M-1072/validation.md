# Intake validation

Base revision: `23e8c7fd5602b359d75252bd4e37074a071f0c68`.

Validation is limited to repository/manifest consistency, dossier structure, bounded repository
discovery, JSON syntax, scoped intake invariants, and whitespace. No canonical Lean expression
exists at intake, so no elaboration, trust-profile report, or kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1072` | exit 0; rank 514, L0/rework_required, planned, theorem_complete false |
| `rg -n -i 'levy\|khinchin\|characteristicFunction\|infinitelyDivisible' --glob '*.lean' .` | exit 0; nearby Levy/characteristic-function infrastructure found, but no repository-local Levy-Khinchin process declaration located |

The JSON, invariant, owned-path, and whitespace checks are rerun after dossier creation and recorded
in the worker self-test manifest. Known downstream failures are the exact source pinpoint and
review, representation convention, canonical Lean elaboration and mutation tests, formal-candidate
audit, obligation registry, proof, trust/provenance closure, hermetic replay, and independent
verification. They prevent theorem completion but do not invalidate this fail-closed planned intake.
