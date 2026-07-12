# Intake validation

Base revision: `2612b21a0cd5f3f13bd2223af801c73511f950c0` (tree
`62baf871bcb662ecc80ad61fc2909e065d211ab5`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, scope and source crosswalk, open task DAG, structured
invariants, and pinned Lean candidate probe. It does not validate a canonical Arzela-Ascoli
proposition or proof because source variant selection and statement freeze remain open. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only. No update,
build, clone, fetch, or other dependency mutation was performed. Dirty worker evidence is
nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean after the probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source boundary

The Encyclopedia of Mathematics permanent revision 53769 was inspected as a secondary source
discriminator. The observed 14,761-byte response had SHA-256
`cc74b5b2a829ec1710907a773606c86e2b0129f146739fb37a941b5ff3bcc840` and cited Ascoli 1883 and
Arzela 1893 while describing a family of limit-continuity results. It neither selects the catalog's
1889 compactness-criterion root nor supplies a complete primary proof crosswalk. It receives no H0
credit and was not added to the repository.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0267` | exit 0; rank 1046, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git rev-parse HEAD 'HEAD^{tree}'`; `git blame -L 1922,1927 -- Docs/researches/math_theorems.md` | exit 0; base revision/tree recorded above; all six source-record lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded `curl` retrieval and inspection of Encyclopedia of Mathematics revision 53769 | exit 0; response size and digest recorded above; secondary discovery only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | exit 0; pinned revision/tree recorded above; empty status output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0267/IntakeProbe.lean)` | exit 0; six direct named interfaces elaborated; three representative declarations reported `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `3d1f15292cd5965e6f59b3a924c93b087d06a9e492ac40049b224c17fccfbc7b` |
| bounded `rg` search in pinned mathlib and repo-local Lean | exit 0; non-equivalent exact-topic interfaces and a foreign-target use were located; no source-identical root or proof credit was inferred |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | exit 0 after finalization; all structured artifacts parse |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0267-pycache python3 -m py_compile Stage1_Instances/THM-M-0267/check_intake.py` | exit 0; checker compiled without writing generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0267/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0 after finalization; target/DAG identity, source and dependency hashes, H1/M3/R4 boundary, null target, exact inventory, receipt/packet agreement, pinned Lean probe, and six open tasks agree |
| token-anchored prohibited Lean declaration scan over the owned path | exit 1 as expected; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token; diagnostic `#print axioms` remains permitted |
| scoped per-file new-file whitespace checks and `git diff --check` | exit 0; no whitespace diagnostics |

## Known open gates

An exact immutable primary result, its incorporated definitions, ordered statement, assumption and
proof map, historical attribution, translation, corrections or errata, and independent review
remain open. So do canonical Lean expression and environment fingerprints, checked transports,
statement mutations, exhaustive anchor and provenance audit, discovery and obligation freezes,
typed graphs, proof and composition, accepted trust closure, readable reconstruction, hermetic
replay, deterministic bundle, independent verification, master acceptance, audit completion, and
theorem completion. These open gates do not invalidate a truthful self-tested `planned` intake.
