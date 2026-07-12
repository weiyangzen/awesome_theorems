# Intake validation

Base revision: `9898aa12e1dd435f018a54a6266ec411ed09a26a`; base tree:
`c0abfcd8c20a1be4b894a7664746d02086072b9d`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source-family discrimination, JSON and scoped invariants, a narrow pinned Lean substrate
probe, a bounded repo-local and mathlib search, prohibited-construct hygiene, and whitespace. It
does not validate a canonical theorem statement or proof because the catalog supplies no stable
truth-valued proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The author-hosted preliminary edition of Gerald Teschl's *Ordinary Differential Equations and
Dynamical Systems* was inspected as a temporary worker input at Section 6.5, printed pages 199-200.
It uses the catalog's broad idea to introduce the field, separates three local scalar examples, and
gives an implicit-function necessary condition rather than one general theorem. The PDF SHA-256 is
`362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`; a 6,874-byte extract
made with `pdftotext -f 210 -l 211 -layout` has SHA-256
`72cf623f3faffe4eb6df0d1ad7ca173bb3c5157e03bd4cb07840ee2f08911e9f`. The official errata
input has SHA-256 `3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e` and no text match
for the inspected bifurcation passage. No source file was added to the repository, and no immutable
source admission, complete premise/proof/errata mapping, or independent H0 review is claimed.

## Environment fingerprint

- Platform: Linux x86_64.
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
| `python3 scripts/stage1_target.py show THM-M-1358` | 0 | rank 968; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 9901,9906 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git rev-parse bcf3f9fa79ab8c2b6610c9875668c2589b35b74f:Docs/researches/math_theorems.md` | 0 | source-record blob `5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf` |
| `pdftotext -f 210 -l 211 -layout /tmp/teschl-ode.pdf /tmp/thm-m-1358-teschl-extract.txt` | 0 | temporary external worker input; extracted 6,874 bytes with SHA-256 `72cf623f...11e9f` |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1358/IntakeProbe.lean)` | 0 | six adjacent implicit-function, integral-curve, flow, fixed-point, derivative, and smoothness APIs elaborated; complete output SHA-256 `c47c71c8...73a9bd` |
| `rg -n -i --glob '*.lean' 'bifurcat' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | no exact-topic Lean occurrence; intake discovery only, not an exhaustive anchor audit or global absence claim |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-1358/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1358/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H5/M4/R4 boundary, null formal target, exact inventory, worker packet, source hashes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1358/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| `rg -n -i 'sorry\|admit\|sorryax\|axiom\|constant\|opaque\|unsafe\|placeholder\|fake result' Stage1_Instances/THM-M-1358 --glob '*.lean'` | 1 (expected no match) | no prohibited declaration or proof escape in the discovery-only Lean probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1358 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- The title and gloss do not select one stable proposition. No repository-selected source, exact
  theorem, incorporated definitions, assumptions, proof boundary, errata record, or independent
  source review exists.
- The parameter and phase spaces, dynamics model, regularity, invariant object, qualitative-
  equivalence notion, locality, genericity, nondegeneracy, quantifier order, and conclusion remain
  open. The neighboring named bifurcations cannot be substituted.
- No canonical Lean expression, exact imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
