# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier, source and duplicate-scope
crosswalk, open task DAG, JSON and scoped invariants, a narrow pinned Lean API probe, and bounded
repo/mathlib discovery. It does not validate a canonical Liouville proposition or proof because
neither has been frozen. The automation-provided canonical `.lake` symlink was pre-existing and
used read-only. No `lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation was
performed. The worker tree is nonrelease evidence.

## Source discovery boundary

The author-hosted David Tong *Classical Dynamics* PDF was inspected outside the repository. Section
4.2, printed pages 88-90, states phase-space-region volume invariance under Hamiltonian evolution
and sketches the canonical-coordinate infinitesimal Jacobian proof. The PDF was 1,093,743 bytes with
SHA-256 `b65ba2b0399df6b02ca3850e5c69ee0255c3011a35664e80766349f521e43e80`.
Extracting the inspected text with `pdftotext -layout` and selecting source-text lines 4600-4682
produced a 4,056-byte passage with SHA-256
`7b18b0386bde96a0babcc5add0883ae94c5dd40be9fe3a646a1143141d61819d`.
The mutable PDF was not added to the repository and is not an immutable H0 packet.

## Environment

- Linux `7.0.0-27-generic`, `x86_64`; timezone `Asia/Shanghai`.
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

All repository commands ran at the repository root unless another working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1375` | 0 | rank 985; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 10020,10025 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| inspect `Docs/researches/math_theorems.md:11101-11106` and `Docs/researches/physics_theorems.md:6839-6845` | 0 | located the same-gloss `THM-M-1520` duplicate and the Hamiltonian-flow `THM-P-0800` corroborating record; no cross-target credit |
| retrieve author-hosted Tong PDF outside the repo; `pdftotext -layout`; inspect Section 4.2 | 0 | source-family discriminator and hashes recorded above; no source acceptance |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean/Lake versions recorded above; no update or build |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | pinned hashes recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1375/IntakeProbe.lean)` | 0 | ten adjacent APIs elaborated; complete combined output SHA-256 `c65fa987d8d9df7133e44eddec3b2bb1d38efb83432b7f27839420bce05c8069`; no target theorem declared |
| bounded exact-topic `rg` over pinned mathlib and repo-local Lean | 0 | pinned mathlib contributed only unrelated number-theory volume; repo-local results were the separately owned legacy `S1_M_189.lean` boundary, which explicitly denies terminal completion |
| `python3 -m json.tool` on the three owned JSON files and root worker packet | 0 | all structured artifacts valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1375-pycache python3 -m py_compile Stage1_Instances/THM-M-1375/check_intake.py` | 0 | scoped validator compiled without generated owned files |
| `python3 -B Stage1_Instances/THM-M-1375/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, H1/M4/R4 boundary, null target, source pins, duplicate boundary, artifact hashes, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1375/check_intake.py` | 0 | public replay mode passed without scheduler-only packet |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-1375` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the discovery probe |
| per-new-file `git diff --no-index --check /dev/null` plus scoped `git diff --check` | 0 aggregate | no whitespace diagnostics; no-index exit 1 per new file meant only content differed from `/dev/null` |

## Status boundary

This is provisional self-test evidence for `S56-M-1375-INTAKE` only. Canonical-root selection,
accepted immutable source and complete premise/proof/errata mapping, `THM-M-1520` duplicate
reconciliation, independent review, exact Lean expression and statement mutations, exhaustive
anchor audit, obligation registry, typed graphs, proof, composition, trust closure, readable
reconstruction, hermetic replay, deterministic release bundle, and independent verification remain
open. These failures prevent statement, audit-completion, and theorem-completion claims, but do not
invalidate the planned intake.
