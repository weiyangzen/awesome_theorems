# THM-M-0047 intake validation

Base revision: `7e54c0fcaf9c0e53fa7afbbeb0a36218152f932c` (tree
`80ece87e35401b07ba76abc36ea83440b5fa7f31`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, literal-claim counterexample, source-statement and
non-substitution boundaries, open task DAG, structured intake invariants, and a narrow pinned Lean
probe. It does not validate a corrected LU/PLU proposition or proof because no corrected root has
been source-selected. The automation-provided canonical `.lake` symlink was pre-existing and used
read-only; no dependency update, build, clone, fetch, or other `.lake` mutation was performed. This
dirty worker run is nonrelease evidence.

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
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0047` | exit 0; rank 1087, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git blame -L 356,361 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref DOI API inspection for `10.1093/qjmam/1.1.287` | exit 0; Turing, title, journal, volume/issue, year, and pages confirmed as a bibliographic lead only |
| publisher PDF request | exit 0 transport; returned a 5,542-byte HTML access page, not a PDF |
| King's College, Cambridge Turing Digital Archive `AMT/B/18` inspection | exit 0; 25-page PDF, SHA-256 `4762fc6d01628be3282d336e6fc080be6b34cc0d75d6e70542afa98b23e272d3`; Section 3 pages 289-290 LDU theorem and proof inspected; H1 only |
| bounded inspection of ALAFF Sections 5.2.3 and 5.3.3 | exit 0; precise unpivoted leading-submatrix and partial-pivoting variants located; current Section 5.2.3 HTML digest `15fc81a54356635a5311a50c0373d1c3e9ad5b384b7d2770906aba2f52bff9b3`; H0 not claimed |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| bounded exact-topic `rg` search for LU/PLU/LUP in pinned mathlib and repo-local Lean | completed; no terminal declaration located; triangular and pivot/transvection substrate only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0047/IntakeProbe.lean)` | exit 0; rational swap-matrix counterexample kernel-checked and six adjacent APIs elaborated; stdout SHA-256 `85212b1124123df2a24a58ed1631096335d68cdcc74c15bf792f47d31678807c` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0047-pycache python3 -m py_compile Stage1_Instances/THM-M-0047/check_intake.py` | exit 0; scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0047/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest/DAG identity, null corrected target, H1/M4/R4 boundary, source/dependency pins, artifact hashes, receipt/packet, checked counterexample, and six open tasks agree |
| prohibited Lean construct scan over `IntakeProbe.lean` | exit 1 as expected; no match for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` |
| scoped new-file whitespace checks plus `git diff --check` | exit 0; no whitespace errors |

## Known open gates

The catalog must be corrected, redirected, or rejected against the inspected source under
independent review. Exact matrix/scalar/index domains, meaning of principal minors, pivot or
permutation convention, hypotheses,
normalization, uniqueness, equation orientation, and boundary cases remain open. So do the
canonical Lean expression and environment fingerprints, transports, statement mutations,
exhaustive formal anchor audit, discovery protocol, obligation registry, typed graphs, corrected
root proof and composition, trust/provenance closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, master acceptance, audit completion, and theorem
completion. These gates do not invalidate a truthful self-tested `planned` intake.
