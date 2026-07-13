# Intake validation

Base revision: `0c019b7194c9c43fa5f683fa82d637a0b275410d` (tree
`43cf6ac322b1dba09be739b52ab3d02e9f9d8f3e`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, source-family and scope discrimination, open task DAG,
JSON and scoped invariants, and a narrow pinned Lean API probe. It does not validate a canonical LPS
statement or proof because neither is frozen. The automation-provided canonical `.lake` symlink was
pre-existing and used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other
`.lake` mutation was performed. This dirty worker evidence is nonrelease evidence.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source discovery boundary

Crossref metadata and the publisher abstract for DOI `10.1007/BF02126799` identified the matching
1988 article and its spectral and girth result family. The publisher article body was restricted;
the PDF route returned an HTML access page. The mutable metadata/abstract responses were not
admitted as immutable theorem text. The versioned 2017 Lubotzky survey was inspected and its PDF
hashed, but it is a secondary family discriminator. Exact 1988 theorem text, definitions, parameter
conditions, construction branches, proof boundary, corrections, catalog-root selection, lawful
capture, and independent review remain open, so no `H0` claim is made.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0883` | exit 0; rank 1435, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all` | exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` symlink existed before this intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base revision and tree shown above |
| `git blame -L 6467,6472 -- Docs/researches/math_theorems.md` | exit 0; all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref API query for DOI `10.1007/BF02126799` | exit 0; LPS authors, title, *Combinatorica* 8(3), September 1988, pages 261-277 confirmed; mutable metadata only |
| publisher abstract query for DOI `10.1007/BF02126799` | exit 0; explicit `k`-regular Cayley family, spectral bound, and asymptotic girth clauses observed; subscription preview only |
| arXiv API and versioned PDF query for `1711.06558v1` | exit 0; immutable author survey inspected; PDF SHA-256 `cfcdc1d023eb9ab8bb7397fefa98b216cce74770fcbb9177b84ee2534f65a32e`; secondary evidence only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | exit 0; pinned revision/tree recorded above; clean output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0883/IntakeProbe.lean)` | exit 0; eleven adjacent pinned graph, spectrum, PSL/PGL, Legendre-symbol, and square-root APIs elaborated; output SHA-256 `a7ec652010c73111f342fdc66e3a5ada6352476e7e425638114febfbb8445379`; no target declaration or proof body |
| exact-topic `rg` search for LPS/Ramanujan-graph names in repo-local and pinned-mathlib `.lean` files | exit 1, expected; no exact-topic occurrence; bounded intake discovery rather than a complete anchor audit |
| `python3 -m json.tool` on structured owned artifacts and `.stage1-worker-selftest.json` | exit 0 for each after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0883/check_intake.py` | exit 0; validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0883/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; target and DAG authority, source/dependency hashes, null target, H1/M4/R4 boundary, exact inventory and receipt/packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0883/check_intake.py` | exit 0; packet-independent replay also passes |
| prohibited Lean proof-escape scan over the owned path | exit 1, expected no match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API probe |
| per-new-file whitespace checks plus `git diff --check` | exit 0 aggregate; no whitespace errors |

## Known open gates

An admitted primary theorem and definition bundle; independent review; exact prime, congruence,
residue, group, generator, graph, family, explicitness, degree, cardinality, bipartite, spectrum, and
girth choices; the canonical Lean expression and fingerprints; checked transports and mutations;
the formal anchor audit; discovery and obligation freezes; typed graphs; proof and composition;
trust and provenance closure; readable reconstruction; hermetic replay; deterministic release
bundle; independent verification; master acceptance; audit completion; and theorem completion all
remain open. These failures do not invalidate a truthful, self-tested `planned` intake.
