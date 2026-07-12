# Intake validation

Base revision: `85da7777da7cc5104d4bc4eaa1d947b8137ca5f5`; base tree:
`ae4ad4de219b61476e1ed10c008e8139247b9d77`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, JSON and scoped invariants, a narrow pinned Lean candidate probe, prohibited-construct
hygiene, and whitespace. It does not validate a canonical theorem statement, a source-statement
identity bridge, or a proof. The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink; it was used read-only and not modified. No dependency update,
build, clone, fetch, or `.lake` mutation was run, so this is nonrelease worker evidence.

## Source discovery boundary

Crossref metadata for DOI `10.2307/1967124` was retrieved to `/tmp`, inspected, and hashed. It
corroborates a T. H. Gronwall paper published in July 1919 in *The Annals of Mathematics*, but it
does not expose theorem text. The JSTOR PDF endpoint returned HTTP 420, and no article was added to
the repository. The bibliography is discovery evidence only; exact primary-source wording,
premises, relation to the later integral form, errata, and independent review remain open.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 (Asia/Shanghai) unless a `cwd` is
shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1337` | 0 | rank 948; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD` / `git rev-parse HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 9754,9759 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref DOI API query for `10.2307/1967124`, then `wc -c` and `sha256sum` on the `/tmp` response | 0 | 1,532-byte metadata response; SHA-256 `e3d0c9b0ed14b8d67fd642968d2646fc6ffc576fa155024687f9a357eb285ecc`; T. H. Gronwall, article title, Annals of Mathematics 20(4), July 1919, starting page 292 |
| JSTOR PDF retrieval for stable item `1967124` | 22 | HTTP 420; no primary article obtained or credited |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| pinned-mathlib `rg` search for integral/Gronwall combinations | 1 | no matching integral-form Gronwall declaration; bounded negative text search only |

The final Lean probe, JSON checks, scoped intake checker, prohibited-construct scan, and whitespace
checks are recorded in `intake-receipt.json` after finalization.

## Status boundary

This is provisional worker self-test evidence for `S56-M-1337-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Source theorem selection and independent review,
canonical statement elaboration and mutations, checked integral/differential transports, anchor and
provenance audit, discovery and obligation freezes, typed graphs, proof and composition, readable
reconstruction, trust closure, hermetic replay, deterministic release evidence, independent
verification, and master acceptance remain open. They prevent audit and theorem completion but do
not invalidate the planned intake.
