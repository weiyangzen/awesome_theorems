# Intake validation

Base revision: `fb0baac89ea0633612be3b47448464b4b8e4bef7`; base tree:
`018557070da18ea1733a82de81a238750c59aa84`.

This validation covers target membership, the planned dossier and open task DAG, catalog and
primary-bibliography provenance, JSON and scoped invariants, a narrow pinned Lean infrastructure
probe, prohibited-construct hygiene, and whitespace. It does not validate a canonical theorem
statement or proof because source admission and the choice of Pólya variant belong to the
downstream statement phase.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

Crossref metadata for DOI `10.1007/BF02546665` identifies G. Pólya's 1937 Acta Mathematica paper,
volume 68, pages 145-254, matching the catalog author and year. The observed response had SHA-256
`71a0e2d7bdc462f43107b2d310a92cd39d1e05252b324fa2b91b8befa98d92bb`. Semantic Scholar and
Unpaywall exposed the same Project Euclid open-copy lead, but direct article requests returned
access-control HTML rather than the paper. No theorem/formula/page, incorporated definitions,
proof, translation, correction/errata record, or independent source review was established. This
supports provisional `H1`, not `H0`.

Pinned mathlib contains Burnside orbit counting and permutation-cycle interfaces, but no exact
Pólya root was selected or located by the bounded intake query. The probe validates reusable
infrastructure only, supporting provisional `M3`; it confers no `M0` proof credit and no credit for
the separately owned Burnside target.

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
| `python3 scripts/stage1_target.py show THM-M-0928` | 0 | rank 1467; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6784,6789 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref metadata `curl` request | 0 | 3855-byte observed response, SHA-256 `71a0e2d7bdc462f43107b2d310a92cd39d1e05252b324fa2b91b8befa98d92bb` |
| Semantic Scholar metadata `curl` request | 0 | 708-byte observed response, SHA-256 `eb4dec46f22789f90a3cb16592fc3f1aecf9479748730bdd4774246cf48172a7`, exposed the Project Euclid open-copy lead |
| Unpaywall metadata `curl` request | 0 | 2799-byte observed response, SHA-256 `f17c9753412c662d5853fd29e912f1886350254d9b538a17cff24fea9bf6df26`, corroborated the Project Euclid published-version lead |
| direct Project Euclid article `curl` request | 0 | returned a small ASCII HTML access page rather than a PDF; no source-text credit |
| pinned exact-topic `git grep` for Pólya, cycle index, inventory polynomial, or enumeration theorem | 1 (expected no match) | no exact-topic declaration name/text in pinned `Mathlib`; bounded query only, not an absence theorem |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0928/IntakeProbe.lean)` | 0 | six adjacent interfaces elaborated; three axiom reports were `[propext, Classical.choice, Quot.sound]`; output SHA-256 `d404282e866bb7b628a3086bd3a8870c599d4bbbd4f8ba9366b25fe468c0fefb` |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `compile` of `Stage1_Instances/THM-M-0928/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0928/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M3/R4 boundary, source and candidate hashes, exact inventory, worker packet, and six open tasks agree |
| prohibited Lean proof-escape scan over the intake probe | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped byte checks plus `git diff --check` | 0 aggregate | final newlines present; no invalid bytes, trailing whitespace, or diff diagnostics |

## Known downstream failures

- The catalog provides no exact formula, action, color inventory, coefficient domain, source
  locator, definitions, hypotheses, conclusion, or proof.
- The primary bibliographic lead was identified but its text, pinpoint statement, proof,
  translation, corrections, errata, and independent review were not admitted.
- Orbit-total, prescribed-inventory, weighted, and cycle-index substitution variants are not the
  same proposition. No canonical choice or checked relationship is frozen.
- Burnside's lemma and cycle APIs are adjacent ingredients only; no coloring action,
  fixed-coloring cycle formula, or Pólya-specific declaration is accepted.
- No exact Lean target, minimal imports, expression/environment fingerprints, checked transports,
  or required removed-hypothesis/domain/binder/boundary mutations exist.
- Exhaustive anchor audit, discovery and obligation freezes, typed graphs, proof integration,
  composition, provenance and trust closure, readable reconstruction, hermetic replay,
  deterministic bundle, independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze scope and open the
downstream DAG. Only the integration lane may accept the provisional worker receipt.
