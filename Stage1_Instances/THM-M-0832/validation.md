# Intake validation

Base revision: `be8701e88e791545c16a262edd1909486d5cef4b`; base tree:
`78b0a751473bf6d71f453a6aad18b130268a3428`.

This validation covers target membership, the fail-closed planned dossier, scope map, source-
statement crosswalk, six-node open task DAG, repository provenance, inspected expanded primary
source, JSON and scoped invariants, a narrow pinned Lean API probe, prohibited-construct hygiene,
and whitespace. It does not validate an exact theorem statement or proof because source/root and
representation decisions remain open.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned intake files and root worker packet make the final tree dirty and nonrelease.

## Source boundary

The catalog's 1994 attribution maps to the ESA preliminary paper DOI `10.1007/BFb0049404`. The
expanded JACM version DOI `10.1145/263867.263872` was inspected as a seven-page PDF at SHA-256
`c70e66134f25a5eec5317eb6377ef03c1bfb4c568f01bafcc025c38138d76789`.
It fixes an ordinary undirected graph with nonnegative real edge weights, the nontrivial-partition
minimum-cut problem, maximum-adjacency phases and contractions, Theorem 2.1, Lemma 3.1, and a
runtime analysis. Exact root selection, comparison to the preliminary edition, full definition and
assumption mapping, corrections or errata, preservation review, and independent review remain open.
This supports provisional `H1`, not `H0`.

## Environment fingerprint

- Platform: Linux `7.0.0-27-generic`, x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

Commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0832` | 0 | rank 1390; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6110,6115 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 60 https://api.crossref.org/works/10.1007/BFb0049404` | 0 | 1994 ESA title, authors, pages 141-147, and publisher confirmed; response SHA-256 `644294e396c9d2988020fcf56fdec6121107aa8ca7c4f33ddfa28548c0925cd7` |
| `curl -L --fail --silent --show-error --max-time 120 https://www.cs.dartmouth.edu/~ac/Teach/CS105-Winter05/Handouts/stoerwagner-mincut.pdf -o /tmp/thm-m-0832-primary.pdf` | 0 | 207843-byte, seven-page expanded JACM PDF; SHA-256 `c70e66134f25a5eec5317eb6377ef03c1bfb4c568f01bafcc025c38138d76789` |
| `pdftotext -layout /tmp/thm-m-0832-primary.pdf /tmp/thm-m-0832-primary.txt` | 0 | source definitions, algorithm, Theorem 2.1, Lemma 3.1, and runtime inspected; text SHA-256 `67c648775ce40efafd73d2d5a767010ce0e1f7a768a13f1e87ee2115b9b62759` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | tool versions agree with the fingerprint; no update or build ran |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0832/IntakeProbe.lean` | 0 | nine adjacent finite-graph APIs elaborated; stdout SHA-256 `6d9de3d924737eeb3046bbcf4c522021415b2ff06678d8cd65d5974c19529f44`; no target theorem |
| `rg -n -i --glob '*.lean' 'stoer.?wagner\|minimum.?cut\|global.?min.*cut\|maximum.?adjacency\|cut.?weight\|cut.?capacity\|contract.*vert' Formalizations/Lean/AwesomeTheorems.lean Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 (expected no match) | no exact-topic named or documented declaration found in the bounded roots; not an exhaustive anchor audit |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all final structured artifacts are valid JSON |
| Python `ast.parse` on `check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0832/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H1/M4/R4 boundary, null target, source/tool hashes, inventory, packet, receipt, and six open tasks agree |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0832` | 1 (expected no match) | no prohibited declaration or proof escape in the API probe |
| per-new-file no-index whitespace checks plus `git diff --check` | 0 aggregate | no whitespace diagnostics |

## Known downstream failures

- The catalog does not select phase correctness, contraction recurrence, end-to-end correctness,
  termination, witness/value output, runtime, or an exact conjunction.
- Graph, weight, cut, maximum-adjacency search, tie, contraction, original-vertex provenance,
  output, complexity, ordered-binder, and boundary semantics remain open.
- Primary source identity and proof route are inspected, but exact root admission, 1994/1997
  edition comparison, complete definition/assumption/proof mapping, correction or errata audit, and
  independent review remain open.
- No exact Lean target, minimal imports, expression/environment fingerprint, checked alternate
  encoding, statement mutation tests, usable formal candidate, or proof body exists.
- Discovery protocol, obligation registry, typed graphs, proof, composition, trust closure,
  readable reconstruction, hermetic replay, deterministic bundle, independent verification, audit
  completion, theorem completion, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake. Only the integration lane may accept the
provisional worker receipt.
