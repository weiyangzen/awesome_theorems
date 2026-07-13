# Intake validation

Base revision: `997541734bb32f987fb15f163335a82512992120`; base tree:
`2c866b9d840d48c48ac839740c62d3b9440be0e5`.

This validation covers target membership, the planned dossier, source and scope crosswalks, the
open downstream DAG, JSON integrity, and a narrow pinned Lean API probe. The canonical human claim
is finite Konig matching-cover equality, but the source graph convention, exact Lean expression,
extremal matching invariant, transports, mutations, source acceptance, and proof remain open. The scheduler-provided
canonical `.lake` symlink was used read-only. No dependency update, build, clone, fetch, or `.lake`
mutation was performed. The dirty worker tree is nonrelease evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0812` | exit 0; rank 1371, planned, L0/rework_required, no legacy slot, theorem_complete false |
| `git status --short --untracked-files=all` | exit 0; initially only the automation-provided `Formalizations/Lean/.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree match those above |
| `git blame -L 5970,5975 -- Docs/researches/math_theorems.md` | exit 0; all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; hashes `651c8acc...b1d2` and `321626c8...2d81` |
| source inspection of `https://arxiv.org/pdf/2009.03780v1` and `https://arxiv.org/e-print/2009.03780v1` | exit 0; translation PDF 94,803 bytes, SHA-256 `cecbda9...f671a`; extracted TeX 9,171 bytes, SHA-256 `c64b81e2...53d4`; translated-primary discovery evidence only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0812/IntakeProbe.lean)` | exit 0; nine pinned bipartite, matching, vertex-cover, and Hall interfaces elaborated; no target or proof credit |
| `rg -n -i --glob '*.lean' 'K[oöő]nig\|maximum matching\|minimum vertex cover\|matching.*vertexCover\|vertexCover.*matching\|matching_?(num\|number)\|max_?matching' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics Formalizations/Lean/AwesomeTheorems` | exit 1 (expected no-match); no exact root or matching-number definition found in this bounded intake search |

Final JSON parses, `python3 -B Stage1_Instances/THM-M-0812/check_intake.py
--worker-packet .stage1-worker-selftest.json`, the token-anchored prohibited-construct scan, and
scoped whitespace checks ran with the exact results recorded in `intake-receipt.json`. Because the
new dossier is untracked, `check_intake.py` independently checks inventory, line endings, final
newlines, trailing whitespace, immutable source hashes, dependency pins, and worker-packet shape.

Known downstream failures remain intentional: independent original-source and errata review;
simple-versus-parallel-edge convention; exact Lean extrema and statement elaboration; transports and mutations; immutable anchor audit;
obligation and typed-graph freeze; proof and composition; H0/R0; hermetic replay; independent
verification; and master acceptance. These block theorem completion but not a truthful planned
intake.
