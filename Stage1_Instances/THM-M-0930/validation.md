# Intake validation

Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7` (tree
`018557070da18ea1733a82de81a238750c59aa84`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the fail-closed planned dossier and open task DAG,
catalog and primary-source root discrimination, structured invariants, and a narrow pinned Lean
candidate probe. It does not validate a canonical Combinatorial Nullstellensatz proposition or
proof because Theorem 1.1 versus Theorem 1.2 versus package selection remains open.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned intake files and root worker packet make the final snapshot dirty and nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`; Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0930` | 0 | rank 1469; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight output was only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6798,6803 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| pre-dedup Stage0 inspection at `c61be3c80710c07c5f7626e3404e51f40ecb39a6^` | 0 | this name/gloss was `THM-M-0957`; old `THM-M-0930` was Bose-Shrikhande-Parker, so provenance is bound to ID plus name/gloss |
| `curl -L -k --fail --silent --show-error https://www.cs.tau.ac.il/~nogaa/PDFS/null2.pdf -o /tmp/thm-m-0930-null2.pdf` | 0 | author-hosted 26-page primary PDF retrieved outside the repository; 305123 bytes; SHA-256 `5933068242b0ecc6bba6944bf6d396492bb31c630d4cd7616e477b0a3e1646b7` |
| `pdfinfo` and `pdftotext -layout` on the temporary PDF, followed by scoped inspection | 0 | Theorems 1.1 and 1.2, Section 2 proofs, and the statement that both may be called Combinatorial Nullstellensatz were inspected; extracted-text SHA-256 `1ee86c030001e584bb0316aa463ed24fa6fa9773ad2ececadb329140518d0cec` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0930/IntakeProbe.lean)` | 0 | seven exact-topic types and three candidate axiom diagnostics elaborated; complete combined output SHA-256 recorded in `intake-receipt.json`; no target declaration was added |
| bounded `rg` search for Combinatorial Nullstellensatz declarations in repo-local Lean and pinned mathlib | 0 | dedicated pinned module and its three recorded interfaces found; no pre-existing repo-local THM-M-0930 wrapper found; intake discovery only |
| `python3 -m json.tool` on all structured owned files and `.stage1-worker-selftest.json` | 0 each | valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0930-pycache python3 -m py_compile Stage1_Instances/THM-M-0930/check_intake.py` | 0 | scoped checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0930/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency hashes, null target, H1/M3/R4 boundary, exact artifact inventory, provisional receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0930/check_intake.py` | 0 | public replay mode passed without the scheduler-only root packet |
| token-anchored prohibited Lean declaration scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration token in the API-only probe; diagnostic `#print axioms` is intentionally permitted |
| `git diff --check` plus per-new-file `git diff --no-index --check /dev/null FILE` | 0 aggregate | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |

## Known open gates

Exact source-root selection, lawful immutable preservation, complete field/domain, variable,
finite-set, degree, coefficient, subring, conclusion, binder, and boundary mapping, correction and
errata audit, and independent source review remain open. So do canonical Lean elaboration, minimal
imports, expression and environment fingerprints, checked transports, all four mutation classes,
exhaustive anchor and terminal-body provenance audit, discovery protocol, obligation registry,
typed graphs, proof and composition, trust closure, readable reconstruction, hermetic replay,
deterministic bundle, independent verification, and release.

These gates block the statement and theorem, but do not invalidate a truthful self-tested `planned`
intake. The receipt is provisional and unsigned; only the integration lane may accept it.

## Status boundary

This is worker self-test evidence for `S56-M-0930-INTAKE` only. It supports a planned dossier and
concrete statement blocker, not an accepted node. No canonical statement, H0 source closure, M0
proof credit, audit completion, theorem completion, or master acceptance is claimed.
