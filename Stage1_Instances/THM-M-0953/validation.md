# Intake validation

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`; base tree:
`fdfff18dea4c6798c5b322b6088dfe556109c134`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, primary-source and numbered-result discrimination, the logarithm and singleton-defect
boundary, JSON and scoped invariants, a narrow pinned Lean substrate/candidate-shape probe, a
bounded repo-local and mathlib search, prohibited-construct hygiene, and whitespace. It does not
validate a canonical theorem statement or proof because the catalog does not select one exact
Solymosi proposition and the likely source has unresolved statement details.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The immutable `arXiv:0806.1040v3` PDF and source archive were downloaded to temporary worker
storage and inspected. The PDF is 1,016,066 bytes with SHA-256
`a48837d2d5e3bcb2af02593aa6315699347c5440a69d3f495c2c0fe2f0b853f2`; the versioned source
archive has SHA-256 `22a2c5ea2245e98805afae114793b75ff95962f1620cd60333e949a854a05338`.
Theorem 2.1 and Corollary 2.2 occur on PDF page 2. Crossref confirms the journal title, sole author,
2009 publication, volume 222, issue 2, pages 402-408, and DOI
`10.1016/j.aim.2009.04.006`.

The source supports family discrimination and provisional H1 only. The catalog neither cites nor
selects it, and there is no independent H0 review. The source text does not explicitly declare the
logarithm base, although its proof partitions by powers of two. The displayed denominator is zero
at singleton cardinality under usual log conventions, and clearing the denominator makes the
singleton instance false. An accountable reviewer must decide whether to admit a corrected
cardinality guard or classify the literal source statement as defective. No temporary external file
was added to the repository or treated as content-addressed acceptance evidence.

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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0953` | 0 | rank 1488; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6959,6964 -- Docs/researches/math_theorems.md` | 0 | all six mathematical catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| temporary download and text inspection of arXiv `0806.1040v3` PDF/source and Crossref DOI metadata | 0 | hashes and source boundary recorded above; no external file retained in the repository |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0953/IntakeProbe.lean)` | 0 | eight sumset, product-set, energy, and `Nat.clog` interfaces plus one explicitly uncredited guarded candidate `Prop` elaborated; complete output SHA-256 `62ba16ac6e208a21dad742e210fe85f8d925bd734f9dd8e17cdb96e3a3b230ec` |
| bounded exact-topic search over pinned mathlib and repo-local Lean | 0 | found generic multiplicative-energy APIs but no Solymosi or source-identical sum-product theorem; discovery only, not a complete anchor audit |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0953/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0953/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M3/R4 boundary, null target, source/result/boundary map, inventory, packet, hashes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0953/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| `rg -n -i --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0953` | 1 (expected no match) | no prohibited proof escape or bodyless/unsafe declaration in the intake probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0953 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |

## Known downstream failures

- The catalog does not choose Theorem 2.1, Corollary 2.2, the asymmetric two-set extension, or
  Theorem 3.1 from the matching paper.
- The inspected primary candidate is not catalog-cited or independently admitted to H0.
- The log base is not explicit, and the printed statement has a substantive singleton defect.
- Domain, positivity, set representation, binder order, exact inequality, constants, ceiling,
  coercions, powers, maximum, and all degenerate cases remain open.
- The guarded base-two candidate is an uncredited feasibility shape, not a canonical target; no
  exact imports, expression/environment fingerprint, checked alternate encoding, or statement
  mutation is frozen.
- Formal anchor audit, discovery and obligation freezes, typed graphs, proof, composition, trust
  closure, readable reconstruction, hermetic replay, deterministic bundle, independent release
  verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
