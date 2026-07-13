# Intake validation

Base revision: `5fe11f4b5e32a06ffb4432460319fc8ae906fe7b`; base tree:
`64c5aacf7cf3eb79008f5a1970151e3e53cb9966`.

This validation covers target membership, the fail-closed dossier and open task DAG, repository and
bibliographic provenance, JSON and scoped invariants, a narrow pinned Lean group-extension boundary
probe, prohibited-construct hygiene, and whitespace. It does not validate a Zassenhaus proposition
or proof because the source identity, classified objects, equivalence, classifying data, binders,
hypotheses, conclusion, and canonical Lean expression are not frozen.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned intake files and root worker packet make the final tree dirty and nonrelease.

## Source boundary

The repository's six-line record was traced to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Crossref and Semantic Scholar metadata exposed the
1937 discrete-groups paper and the 1971 finite-extension-equivalence paper; a 2025 Crossref abstract
identifies the former as the source of Zassenhaus's bounded-derived-length theorem. Publisher
endpoints returned closed-access HTML rather than either primary article. Response hashes are in
`instance.json`. No exact theorem passage, proof, correction, or erratum was inspected, and no
source received H0 credit.

## Environment fingerprint

- Platform: Linux x86_64; kernel `7.0.0-27-generic`; timezone `Asia/Shanghai`.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

Commands ran from the repository root on 2026-07-13 Asia/Shanghai unless a `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0078` | 0 | rank 1528; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 575,580 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -fsSL 'https://api.crossref.org/works/10.1007%2FBF02948950' \| sha256sum` | 0 | SHA-256 `0027bdd25f5a0cbf788ecdaee051e8f8807ad617b9e98644276c96ab58c8b267`; metadata only |
| `curl -fsSL 'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1007/BF02948950?fields=title,authors,year,venue,publicationDate,externalIds,openAccessPdf,citationCount,references.title,references.year,references.externalIds' \| sha256sum` | 0 | SHA-256 `8fc0ca8bbf26903df65119150a865f92b9f66c309d1b34b645c2ccb128e36fc0`; metadata only |
| `curl -fsSL 'https://api.crossref.org/works/10.1007%2FBF01114788' \| sha256sum` | 0 | SHA-256 `307fdd404c843473052546f08c6a10cb3c336fe943bacc417025ecd227706b1e`; metadata only |
| `curl -fsSL 'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1007/BF01114788?fields=title,authors,year,venue,publicationDate,externalIds,openAccessPdf,citationCount' \| sha256sum` | 0 | SHA-256 `dbfe6d3e1825f678c61369a509ac08c9528cd3ba961f0afadc409da8e09e8d55`; metadata only |
| `curl -fsSL 'https://api.crossref.org/works/10.1007%2Fs10013-025-00745-y' \| sha256sum` | 0 | SHA-256 `b29146791fc4608e50acb4c58d5815b7abb2e5df405c4c0aa33f7e95cbb5556a`; secondary diagnostic source only |
| `curl -fsSL --max-time 30 'http://link.springer.com/content/pdf/10.1007/BF02948950.pdf' \| file -` | 0 | HTML, not a PDF; no primary proposition credited |
| `curl -fsSL --max-time 30 'http://link.springer.com/content/pdf/10.1007/BF01114788.pdf' \| file -` | 0 | HTML, not a PDF; no primary proposition credited |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake agree with the fingerprint; no update or build ran |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision/tree above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0078/IntakeProbe.lean)` | 0 | eight APIs and two representative terms elaborated; two boundary axiom sets printed; output 1749 bytes, 21 lines, SHA-256 `007f233dcdd2699cc4aea9a2192745727c716e5d6d94d69dc5a7637d84441d5c` |
| `rg -n -i --glob '*.lean' 'THM[_-]M[_-]0078\|Zassenhaus\|group extension\|extension.*H2\|H2.*extension\|equivalence classes of group extensions' Formalizations/Lean/AwesomeTheorems Stage1_Instances Formalizations/Lean/.lake/packages/mathlib/Mathlib/GroupTheory Formalizations/Lean/.lake/packages/mathlib/Mathlib/RepresentationTheory/Homological/GroupCohomology` | 0 | definitions/basic facts, explicit H2-classification TODOs, and distinct Schur-Zassenhaus matches only; bounded, not a global absence claim |
| `for f in Stage1_Instances/THM-M-0078/*.json .stage1-worker-selftest.json; do python3 -m json.tool "$f" >/dev/null \|\| exit; done` | 0 | all structured artifacts are valid JSON |
| `python3 -c "import ast,pathlib; ast.parse(pathlib.Path('Stage1_Instances/THM-M-0078/check_intake.py').read_text(encoding='utf-8')); print('AST-ok')"` | 0 | scoped validator parses without generated bytecode |
| `python3 -B Stage1_Instances/THM-M-0078/check_intake.py` | 0 | durable public recipe: target, source pins, H5/M4/R4 boundary, null target, artifacts, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0078/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | scheduler handoff additionally agrees with dossier and provisional receipt |
| `if rg -n -i '(^\|[^[:alnum:]_])(sorry\|admit\|sorryAx)([^[:alnum:]_]\|$)\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0078 --glob '*.lean'; then exit 1; fi` | 0 | no prohibited Lean declaration or placeholder |
| `for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-0078/*; do git diff --check --no-index -- /dev/null "$f" >/dev/null; rc=$?; test "$rc" -eq 0 -o "$rc" -eq 1 \|\| exit; done` | 0 | no whitespace diagnostic in any untracked artifact |

## Known downstream failures

- The catalog gives a subject rather than a proposition and supplies no exact source edition,
  theorem/page, definitions, ordered binders, hypotheses, conclusion, proof boundary, corrections,
  errata, or independent reviewer.
- The author/year metadata aligns with a solubility paper while the subject more closely aligns with
  a coauthored 1971 extension paper; no primary source resolves the intended theorem identity.
- Extension objects, endpoint/action data, equivalence, classifier, theorem direction, alternate
  encodings, and all boundary cases remain unresolved.
- Pinned mathlib has vocabulary and a split-extension fact but explicitly leaves the likely
  abelian-kernel `H^2` classification and its cohomology relationship as TODOs.
- Statement mutations, exhaustive anchor/provenance audit, obligation registry, typed graphs, proof,
  composition, readable reconstruction, hermetic replay, independent verification, release, and
  master acceptance remain open.

These failures prevent statement, ordinary theorem-proof execution, audit-completion, and
theorem-completion claims. They do not invalidate a truthful, self-tested `planned` intake whose
purpose is to freeze the ambiguity and open the downstream DAG. Only the integration lane may
accept the provisional worker receipt.
