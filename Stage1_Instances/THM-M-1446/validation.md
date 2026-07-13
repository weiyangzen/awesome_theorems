# THM-M-1446 intake validation

Base revision: `b4e1220a37cc10a96534cfd411e3b29523d7fd81` (tree
`a67dd08a83c396119f4762e0ff109cd0df43ee60`). Validation date: 2026-07-13
(`Asia/Shanghai`).

This validation covers the planned dossier, source and duplicate boundaries, obstruction to one
false unrestricted reading, open downstream DAG, structured intake invariants, and a narrow pinned
Lean probe. It does not validate a corrected LU/LDU/PLU/LUP target or proof. The automation-provided
canonical `.lake` symlink was pre-existing and used read-only; no dependency update, build, clone,
fetch, or other `.lake` mutation was performed. The dirty worker run is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1446` | exit 0; rank 1123, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before intake |
| `git blame -L 10560,10565 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref DOI API inspection for `10.1093/qjmam/1.1.287` | exit 0; Turing, title, journal, volume/issue, year, and pages confirmed as a bibliographic lead; response SHA-256 `76d532496701e9c3fc51180694b4a1e4d221225c715e16ca78acf8cb73f26412` |
| King's College, Cambridge Turing Digital Archive `AMT/B/18` inspection | exit 0; 25-page PDF, SHA-256 `4762fc6d01628be3282d336e6fc080be6b34cc0d75d6e70542afa98b23e272d3`; Section 3 pages 289-290 qualified LDU statement and proof visually inspected; H1 only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded exact-topic `rg` search for LU/LDU/PLU/LUP in pinned mathlib and repo-local Lean | exit 0; only specialized Schur-complement block LDU identities matched; no general exact target declaration found |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1446/IntakeProbe.lean)` | exit 0; rational swap-matrix obstruction kernel-checked and six adjacent APIs elaborated; reported axioms `propext`, `Classical.choice`, `Quot.sound`; stdout SHA-256 `00a1a9138aa5e19f4550b11351becaa187b0b50b346983faf9dcbb08262d1817` |
| `python3 -m json.tool` on the three structured dossier JSON files and root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1446-pycache python3 -m py_compile Stage1_Instances/THM-M-1446/check_intake.py` | exit 0; validator compiled without writing generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1446/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; identity, pins, null target, H1/M4/R4 boundary, source/duplicate boundaries, artifacts, receipt/packet, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

The catalog must be corrected, redirected, merged, or rejected under source and duplicate-identity
review. Exact matrix/scalar/index domains, principal-minor meaning, pivot and permutation convention,
hypotheses, diagonal representation, normalization, uniqueness, reverse clause, and boundary cases
remain open. So do the canonical Lean expression and environment fingerprints, transports,
statement mutations, exhaustive anchor audit, discovery protocol, obligation registry, typed graphs,
exact-root proof and composition, readable reconstruction, trust/provenance closure, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These open gates do not invalidate a truthful self-tested `planned` intake.
