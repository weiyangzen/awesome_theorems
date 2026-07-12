# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

Validation is limited to target-set consistency, the planned dossier and open downstream DAG,
repository-source and duplicate-target provenance, pinned environment identity, a narrow Lean API
probe, bounded local discovery, proof-escape hygiene, JSON and scoped invariants, and whitespace.
It does not validate a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is dirty, nonrelease worker evidence.

## Environment fingerprint

- Platform: Linux x86_64, kernel `7.0.0-27-generic`, timezone Asia/Shanghai.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All commands ran on 2026-07-13 Asia/Shanghai. Repository-root commands are shown without a `cwd`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0303` | 0 | rank 1049; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame` on catalog lines 2174-2179, 2393-2398, and 9038-9043 | 0 | all three uncited records originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; the first two records are byte-identical while the mixed-title record is retained separately |
| `sed -n '260,365p' Docs/tools/generate_stage0_blueprint.py` plus manifest/source comparison | 0 | inspected `assign_ids` and exact-signature `dedupe_items`; the generated artifacts retain the first Real Analysis record as `THM-M-0303` and the mixed-title PDE record as distinct `THM-M-1237`; no generator was run and no output was rewritten |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3...16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and status | 0 | pinned revision/tree above; no package changes |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes match the environment fingerprint |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0303/IntakeProbe.lean)` | 0 | four pinned GNS norm estimates and two Holder interfaces elaborated; output SHA-256 `3f5989a6...f7f6ec`; none is the exact target |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_175.lean)` | 0 | the separate `THM-M-1237` legacy boundary elaborated and explicitly reported its terminal parent proof/status gate open; no credit transferred to this target |
| bounded exact-topic search over pinned mathlib and repo-local Lean sources | 0 findings classified | no target-specific `THM-M-0303` declaration; only mathlib GNS support, the separate `THM-M-1237` boundary, and unrelated compact-embedding discovery references were found; not an exhaustive anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| Python `ast.parse` on `Stage1_Instances/THM-M-0303/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0303/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, H5/M4/R4 boundary, null target, duplicate and neighbor boundaries, hashes, exact artifact inventory, receipt/packet agreement, and six open tasks agree |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0303 .stage1-worker-selftest.json` plus scoped new-file checks | 0 | no whitespace diagnostics in changed files |

## Known downstream failures

- The catalog gloss does not select one Sobolev embedding proposition, and the separately retained
  `THM-M-1237` duplicate has not been reconciled by the integration lane.
- No exact primary or authoritative theorem/page/formula, complete definition and assumption map,
  errata check, or independent source review is accepted.
- No canonical Lean expression, minimal imports, expression/environment fingerprint, checked
  transport, or statement mutation exists.
- Discovery protocol, exhaustive anchor audit, obligation registry and typed graphs, proof,
  composition and trust closure, readable reconstruction, hermetic replay, deterministic evidence
  bundle, and independent release verification remain open.

These failures prevent statement, audit, and theorem-completion claims. They do not invalidate a
truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and ownership
boundary. Only the integration lane may accept the provisional worker receipt.
