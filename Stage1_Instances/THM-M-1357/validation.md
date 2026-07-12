# Intake validation

Base revision: `531673f2e97293dd22e5727b12fc7e13eca7d6e5` (tree
`4acbd91f6e676b2b89949bb52992c0be522de40f`). Validation ran on 2026-07-13 in the isolated worker
clone.

Validation is limited to target-set consistency, dossier structure and scope invariants,
repository-source provenance, neighboring-target boundaries, pinned environment identity, a
narrow Lean API probe, bounded local discovery, proof-escape hygiene, JSON integrity, and
whitespace. The catalog does not select one proposition, so no canonical target, expression hash,
statement mutation, source acceptance, or proof is claimed.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
This is nonrelease worker evidence.

Environment fingerprint:

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

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1357` | 0 | rank 967, planned, L0/rework_required, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git blame -L 9894,9899 -- Docs/researches/math_theorems.md` | 0 | all six uncited target-record lines originate at commit `bcf3f9fa...b74f` |
| Crossref DOI metadata lookup for `10.1002/j.1538-7305.1932.tb02344.x` | 0 | plausible paper lead: H. Nyquist, *Regeneration Theory*, BSTJ 11(1), 1932, pp. 126-147; metadata only, not an accepted theorem source |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1357/IntakeProbe.lean)` | 0 | six adjacent meromorphic-divisor, order, logarithmic-derivative, and circle APIs elaborated |
| bounded `rg` over repo-local and pinned Lean sources for Nyquist, feedback/transfer systems, encirclement, winding, and argument-principle terms | 1 | expected no-match exit; no obvious terminal target declaration under the searched terms; discovery only, not an exhaustive anchor audit |
| `python3 -m json.tool` on all structured owned artifacts and the root worker packet | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1357-pycache python3 -m py_compile Stage1_Instances/THM-M-1357/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-1357/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | manifest/DAG identity, planned H5/M4/R4 boundary, null target, exact inventory, source hashes, provisional packet, and six open tasks agree |
| prohibited Lean proof-escape scan over the owned path | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-1357 .stage1-worker-selftest.json` plus scoped new-file checks | 0 | no whitespace diagnostics in changed files |

## Known downstream failures

- The title and gloss do not select one stable proposition. No repository-cited primary source,
  exact theorem, edition, page, assumptions, proof boundary, correction record, or independent
  source review exists.
- The feedback topology and sign, time domain, SISO/MIMO model, transfer-function class, stability
  predicate, contour, orientation, pole/zero/encirclement convention, boundary singularities,
  cancellation/minimality conditions, and degenerate cases remain open.
- No canonical Lean expression, expression/environment hash, exact imports, checked alternate
  encoding, or statement mutation is frozen.
- The pinned declarations are only adjacent complex-analysis substrate. No source transport,
  winding-number or argument-principle closure, control-system model, or exhaustive anchor audit
  exists.
- Discovery and obligation freezes, typed graphs, proof, composition, readable reconstruction,
  hermetic replay, deterministic bundle, independent verification, release, and master acceptance
  remain open.

The worker self-test therefore proposes only the intake node as `[_]`. Both `audit_complete` and
`theorem_complete` remain false.
