# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9` (tree
`829a47c47ae831cada4f8acc6c2c00ba5883215e`). Validation date: 2026-07-13
(Asia/Shanghai).

Validation is limited to target-set consistency, the planned dossier and open DAG, the inspected
primary-source lead, pinned environment identity, a narrow Lean API feasibility probe, JSON and
scoped invariants, and proof-escape and whitespace hygiene. It does not validate a canonical
three-part Sylow expression or proof because that statement is not frozen.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. The link and package sources were
used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation
was performed. This dirty worker run is nonrelease evidence.

## Environment

- Linux 7.0.0-27-generic x86_64, worker timezone Asia/Shanghai.
- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0062` | 0 | rank 1023, planned, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git blame -L 463,468 -- Docs/researches/math_theorems.md` and source-history inspection | 0 | all six uncited catalog lines originate in commit `bcf3f9fa...b74f`; the record supplies the three-part gloss but no exact definitions or citation |
| inspection of Sylow's 1872 open scan, Zenodo record `2329278`, Theorems I-II at printed pages 586-587 | 0 | maximal-prime-power existence, conjugacy, and `n*p+1` counting located; scan SHA-256 `92a14121...15bf`; historical-domain transport and H0 review remain open |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0062/IntakeProbe.lean)` | 0 | ten pinned Sylow definitions/declarations checked, five candidate axiom sets printed, and six representative existence, conjugacy, congruence, divisibility, normalizer-index, and cardinality uses elaborated; output SHA-256 `e40b6f68...5879` |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0062/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0062/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, null exact target, H1/M3/R4 boundary, source and mathlib pins, exact inventory, provisional packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0062/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0062 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- The catalog does not define a Sylow `p`-subgroup or state the precise counting bundle. The exact
  maximality/order, finite-carrier, conjugacy-action, normalizer, quantifier, and boundary
  conventions remain open.
- The inspected 1872 paper is in finite substitution-group language. Its transport to arbitrary
  finite groups, historical normalizer terminology, full notation and proof mapping, corrections,
  errata, translation, and independent review are not accepted.
- No canonical combined Lean expression, minimal import set, expression/environment fingerprint,
  checked alternate encoding, or statement mutation suite exists.
- The close pinned mathlib candidates have not undergone exact statement normalization,
  wrapper/terminal-body/provenance/dependency/placeholder/axiom/TCB audit, so no M0 is claimed.
- Discovery protocol, obligation registry, typed graphs, proof and composition, readable
  reconstruction, hermetic replay, deterministic bundle, independent verification, release, and
  master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake that freezes the three-part target family and
its unresolved statement boundary. Only the integration lane may accept the provisional receipt.
