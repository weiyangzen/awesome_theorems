# Intake validation

Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d` (tree
`0d6c1fdf06d1573c256af331c6b198e5a787af43`). Validation date: 2026-07-13
(`Asia/Shanghai`).

This validation covers target membership, the fail-closed planned dossier, repository and source
provenance, the scope and non-substitution boundary, the six-task open DAG, a narrow pinned Lean
discovery probe, scoped intake invariants, JSON and Python integrity, proof-escape hygiene, and
whitespace. It does not validate a canonical Viviani proposition or proof because neither is
frozen.

The automation-provided `Formalizations/Lean/.lake` symlink existed before this work and points to
the canonical pinned artifacts. It was used read-only. No `lake update`, `lake build`, dependency
clone or fetch, or other `.lake` mutation was performed. This dirty inherited worker environment
is nonrelease evidence.

The MPIWG transcription, DML index, two arXiv PDFs, and MathWorld page were downloaded to `/tmp`
only for inspection and hashing. They were not added as dependencies. The exact primary theorem
and proof excerpt, identifiers, source hash, rights metadata, and a clearly provisional working
translation are preserved in `primary-source-excerpt.md`; the full temporary downloads are not
claimed as a durable source archive. Recorded replay recipes use only repository and already pinned
inputs and deny network access.

## Environment

- Linux `7.0.0-27-generic`, x86_64; worker timezone `Asia/Shanghai`.
- Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree status was empty.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All commands ran at the repository root unless the table says otherwise.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0208` | 0 | rank 1539; planned; `L0/rework_required`; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before editing | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 1499,1504 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sed -n '1499,1504p' Docs/researches/math_theorems.md \| sha256sum` | 0 | exact catalog block SHA-256 `2379a8af833df110b61de371bb6c7dbbd22769f9f53837ec225399c9541029f0` |
| `sed -n '5779,5804p' Docs/Stage0_Blueprint.md \| sha256sum` | 0 | exact Stage0 block SHA-256 `17bdc8f8b42ea02fc448c6fd686c7f607e501aaeb3d213ffccf4cb19e940e4a6` |
| retrieve MPIWG `ECHO:QN4GHYBF.xml` with `curl -L --fail --max-time 60 -sS` to `/tmp` | 0 | 1,729,692-byte CC-BY-SA 3.0 transcription SHA-256 `57a438ef902213671bf06b0cac8088bfc50b10f4127f7eb0b18b0ebe16a8535e`; Appendix Lemma II Proposition II statement and proof inspected at printed pages 146-147 / scans 332-333 |
| retrieve DML author index with `curl -L --fail --max-time 30 -sS` to `/tmp` | 0 | 31,882-byte response SHA-256 `4b7d986c2f46d390c5ca0fa13238e65b8408d27754b0a6fcac039474de343af6`; cross-links the 1659 book and `QN4GHYBF` holding |
| retrieve arXiv PDFs `0903.0753v3` and `1008.1236v2` with bounded `curl` to `/tmp`; run `pdftotext` | 0 | 164,109-byte SHA-256 `e00b9b38c5d7c925f1a2cf9b9e7d4aae9e3cbad0637dd01cc9deead09a5cdeab`; 219,471-byte SHA-256 `ee772a99068720d50e2e5703baccabca9ff22d67ac9b21e3a64555d0b30fbc22`; modern corroboration and altitude alternate form inspected |
| retrieve MathWorld Viviani page with bounded `curl` to `/tmp` | 0 | mutable 53,037-byte response SHA-256 `0ba20b51d1da1d75431b0db4e45ee4e307c71afb092ccef0e6742174ec9ef80e`; secondary discovery only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package `status --short` | 0 each | pinned mathlib revision/tree recorded above; status output empty |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0208/IntakeProbe.lean)` | 0 | thirteen pinned triangle, equilateral, interior, signed-distance, and altitude APIs elaborated; two reduction interfaces reported only `propext`, `Classical.choice`, and `Quot.sound`; stdout+stderr 3,804 bytes, SHA-256 `8e09f674f02561bfd5bf7071ff8656a48b3beb376788f3b10fda3a461e35b9b9`; no target theorem declared |
| bounded case-insensitive `rg` over pinned mathlib and repo-local Lean for Viviani and sum/side-distance terms | 0 | only internal uses of `signedInfDist_affineCombination` in the unrelated incenter file matched the broad sum pattern; no Viviani-named or packaged three-side-distance theorem found; discovery only |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured records valid after final serialization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0208-pycache python3 -m py_compile Stage1_Instances/THM-M-0208/check_intake.py` | 0 | scoped validator compiled without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0208/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, H1/M3/R4 null-root boundary, source and pin hashes, exact artifact inventory, provisional receipt/packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0208/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-construct `rg` over the owned Lean probe | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0208 .stage1-worker-selftest.json` plus `git diff --no-index --check /dev/null <file>` for every new file | 0 aggregate | no whitespace diagnostics; no-index exit 1 was accepted only when output contained the expected new-file diff and no whitespace warning |

## Known open gates

- The primary edition and exact proof are located, but the Latin translation, definition and
  assumption map, critical-edition/correction/errata audit, lawful durable archive, exact
  regular-polygon-to-equilateral-triangle specialization, and independent review remain open.
- Strict versus closed interior, side line versus finite segment, signed versus unsigned distance,
  ambient dimension, binder order, point-independence versus derived altitude equality, and every
  degenerate case remain unfrozen.
- No canonical Lean target, minimal imports, elaborated expression or environment fingerprint,
  checked alternate-form transport, or semantic mutation suite exists.
- Complete anchor and terminal-body provenance audits, discovery precommit, obligation registry,
  typed graphs, proof, composition and trust checks, readable reconstruction, hermetic replay,
  deterministic evidence bundle, and independent release verification remain open.
- Integration-lane acceptance is pending.

These open gates prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake that freezes the source and scope boundary and leaves all
dependent work open.
