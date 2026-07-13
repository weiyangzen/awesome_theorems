# Intake validation

Base revision: `be8701e88e791545c16a262edd1909486d5cef4b`; base tree:
`78b0a751473bf6d71f453a6aad18b130268a3428`.

This validation covers target membership, the planned dossier and open task DAG, catalog and
primary-source provenance, the distinct CS-record boundary, JSON and scoped invariants, a narrow
pinned Lean substrate probe, prohibited-construct hygiene, and whitespace. It does not validate a
canonical theorem statement or proof because the catalog does not select correctness, termination,
generic operation complexity, FIFO running-time complexity, or an exact composite.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source boundary

The inspected source is Goldberg and Tarjan, *A New Approach to the Maximum-Flow Problem*, JACM
35(4) (1988), 921-940, DOI `10.1145/48014.61051`. The observed 20-page Princeton-hosted PDF has
SHA-256 `e0c93940c1f450c801443af639fff047ac49c9bc43f9f55c9f2ac5d5889fb808`.
Printed pages 923-931 provide the network and algorithm definitions, conditional correctness,
termination and generic operation bound, and FIFO `O(n^3)` result. Exact catalog-root selection,
complete mapping, correction status, durable source admission, and independent review prevent H0
or statement-freeze credit.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0830` | 0 | rank 1388; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6096,6101 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| source download to `/tmp/p921s.pdf` | 0 | 20 pages, 1628825 bytes; primary PDF SHA-256 recorded above |
| `pdftotext -layout /tmp/p921s.pdf /tmp/p921s.txt` and inspection | 0 | printed pages 923-931 crosswalked; extracted-text SHA-256 `916a88fceac832d4732c6d52e46cb88e16c95f73d08309275ff070c180ae78d4` |
| bounded `rg` searches over repo and pinned mathlib Lean | 1 (expected no match) | no push-relabel, preflow, maximum-flow, flow-network, or residual-network formal artifact located |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0830/IntakeProbe.lean)` | 0 | six generic substrate APIs elaborated; complete output SHA-256 `7f8302396e027e3c9077952def8d61138e3ff7bb1aadec85485a62e8662b71a9` |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0830/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0830/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M4/R4 boundary, null target, source hashes, packet, receipt, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0830/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0830 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- The catalog does not select correctness, termination, generic `O(n^2 m)` basic operations, FIFO
  `O(n^3)` time, another scheduling rule, or an exact composite. `THM-C-0099` cannot redefine it.
- Exact network, capacity, algorithm, scheduling, output, cost, asymptotic, and boundary conventions
  remain open.
- The primary passages are inspected and hashed, but exact root mapping, corrections, durable source
  admission, and independent review are open.
- No canonical Lean expression, minimal imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen; no usable exact formal artifact was found.
- Anchor/provenance audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake. Only the integration lane may accept the
provisional worker receipt.
