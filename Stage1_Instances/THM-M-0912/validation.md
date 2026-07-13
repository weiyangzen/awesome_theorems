# Intake validation

Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e`; base tree:
`6434a20532ae7c523ad293e67a6228ab384bfb8a`.

This validation covers target membership, the planned dossier and open task DAG, catalog and modern
source-lead provenance, JSON and scoped invariants, a narrow pinned Lean candidate probe,
prohibited-construct hygiene, and whitespace. It does not validate a canonical theorem statement
or proof because the exact source domain and Lean encoding belong to the downstream statement phase.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

NIST DLMF 1.2.7, Section 26.3(iii), equation 26.3.5 was inspected. It states
`C(m,n) = C(m-1,n) + C(m-1,n-1)` under `m >= n >= 1`. The TeX response had SHA-256
`af43da30b9553896c868f2202e16a0b0a72984111ba0e169bf07814a940663a4`. DLMF points to
Riordan (1958), pages 4-5, and Comtet (1974), page 10, but those sources were not inspected.
Neither the catalog's 1654 attribution nor a complete proof, definition, correction, errata, or
independent review was established. This supports provisional `H1`, not `H0`.

The full section HTML response was also captured for inspection, but dynamic delivery content makes
that response digest unsuitable as a stable source identity. The receipt therefore treats its hash
only as observed-response provenance and relies on the stable 102-byte equation endpoint for the
formula digest. No refetch-equality claim is made for the section page.

Pinned mathlib contains exact recurrence candidates, but its all-natural zero-extended successor
form has a broader displayed domain than DLMF's constrained predecessor form. The probe validates
candidate availability only, supporting `M3` statement/interface discovery. It confers no `M0`
proof credit for an as-yet unselected canonical root.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64.
- Lean: 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0912` | 0 | rank 1454; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6672,6677 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| DLMF equation/section `curl` requests plus `sha256sum` | 0 | formula, constraint, version, release, bibliography, and response digests recorded; no H0 claim |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0912/IntakeProbe.lean)` | 0 | `Nat.choose` and four recurrence candidates elaborated; definitions and candidate axiom reports printed; output SHA-256 `0c75d4158a00f806c3d52a64f2101900f131737e679e12755b9940c6d8208ae8` |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `compile` of `Stage1_Instances/THM-M-0912/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0912/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M3/R4 boundary, source and candidate hashes, exact inventory, worker packet, and six open tasks agree |
| prohibited Lean proof-escape scan over the intake probe | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped byte checks plus `git diff --check` | 0 aggregate | final newlines present; no invalid bytes, trailing whitespace, or diff diagnostics |

## Known downstream failures

- The catalog provides no exact formula, source locator, definition, domain, side conditions, or
  proof. The DLMF modern statement lead does not close the historical, proof, correction, or
  independent-review source gates.
- The constrained predecessor formula and all-natural zero-extended successor formula differ in
  stated domain. Their canonical status and checked relationship are not frozen.
- No exact Lean target, minimal imports, expression/environment fingerprints, checked transports,
  or required removed-hypothesis/domain/binder/boundary mutations exist.
- Exhaustive anchor audit, discovery and obligation freezes, typed graphs, proof integration,
  composition, provenance and trust closure, readable reconstruction, hermetic replay,
  deterministic bundle, independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze scope and open the
downstream DAG. Only the integration lane may accept the provisional worker receipt.
