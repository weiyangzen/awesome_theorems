# Intake validation

- Item: `S56-M-1565-INTAKE`
- Base revision: `b5768b55f94197ed20d70d350ea6d4def3c3a667`
- Validation date: 2026-07-12 (Asia/Shanghai)

Validation is limited to membership and manifest consistency, source discovery, the truthful
`planned` dossier, JSON syntax, scoped intake invariants, the pinned environment, and whitespace.
The source names a theory rather than one theorem and the exact root remains a statement-phase
decision, so there is no canonical Lean expression to elaborate and no kernel-proof claim.

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The
worker clone's untracked `Formalizations/Lean/.lake` link to canonical pinned artifacts pre-existed
this work and was read only for toolchain/version and scoped mathlib discovery.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1565` | 0 | Rank 576, planned, legacy artifacts unaccepted, theorem incomplete |
| `git rev-parse HEAD` | 0 | `b5768b55f94197ed20d70d350ea6d4def3c3a667` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | SHA-256 `651c8acc...b1d2` and `321626c8...8b81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `curl -L --max-time 30` on the Springer DOI page | 0 | Publisher metadata confirmed title, author, journal, 2014 publication, volume 198, pages 269-504, and DOI |
| `curl -L --max-time 30 https://www.hairer.org/papers/Structure.pdf` | 0 | PDF, 1,270,070 bytes, author revision dated 2015-06-08, SHA-256 `95f8c90...33da` |
| `pdftotext -layout` plus scoped theorem/definition searches | 0 | Definition 2.1 and candidate Theorems 3.10, 8.24, and 10.7 inspected with their hypotheses/conclusions |
| repository and pinned-mathlib `rg` for Hairer regularity structures, reconstruction, modelled distributions, and singular SPDEs | 0 | No matching implementation; only metadata, unrelated bibliography, and separate-target audit/interface material found |
| `python3 -m json.tool` on owned JSON files | 0 | Valid JSON |
| scoped Python intake assertions | 0 | Planned lifecycle, empty accepted state, null formal target, `[H1,M4,R4]`, and six ordered open downstream tasks confirmed |
| `git diff --check -- Stage1_Instances/THM-M-1565 .stage1-worker-selftest.json` | 0 | No whitespace errors |

## Known downstream failures

- No exact source root has independent scope approval; theorem/page premise mapping, source-edition
  archival, errata disposition, and independent review remain open.
- Therefore no exact Lean target, minimal imports, expression/environment fingerprints, checked
  transports, or mutation tests exist.
- Anchor audit, frozen obligation registry, proof, composition and trust checks, readable
  reconstruction, hermetic replay, and independent release verification remain open.

These failures prevent any proof or theorem-completion claim. They do not invalidate a self-tested
planned intake whose purpose is to freeze the honest ambiguity boundary and dependent task DAG.
