# Intake validation

Base revision: `be8701e88e791545c16a262edd1909486d5cef4b`; base tree:
`78b0a751473bf6d71f453a6aad18b130268a3428`.

This validation covers target membership, the planned dossier and open task DAG, catalog
provenance, bounded primary-source discovery, JSON and scoped invariants, a narrow pinned Lean API
probe, a bounded repository and mathlib search, prohibited-construct hygiene, and whitespace. It
does not validate a canonical perfect-graph proposition or proof because neither is frozen.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

Crossref metadata identified two direct 1972 Lovasz sources: *Normal hypergraphs and the perfect
graph conjecture*, DOI `10.1016/0012-365X(72)90006-4`, and *A characterization of perfect graphs*,
DOI `10.1016/0095-8956(72)90045-7`. OpenAIRE exposed abstract records for both papers. The first
says a normal-hypergraph min-max theorem implies Berge's complement conjecture. The second states
an induced-subgraph clique-times-stability characterization and says the complement theorem follows
immediately.

Observed metadata-response SHA-256 values were:

- Crossref, normal-hypergraphs paper:
  `bbb49535c70e95adfa3dda60d3abf9b36bbe2d7edb023c91a30df8405ecab0eb`;
- Crossref, characterization paper:
  `6d6fdc00b3e4e32d52b814d34c306114dc5020a1b5039543e396bb5ed568b5cb`;
- OpenAIRE, normal-hypergraphs paper:
  `1fb06a89a686b46bff7617cfce6faf5d02ddb7248a9776f90c7843e498af7221`;
- OpenAIRE, characterization paper:
  `cf756d5aa8bfaea252f56abaab8174bf1787cd47874f6dddb8f95e2cb5cb4bb1`.

Lovasz's author-hosted publication list was inspected and had SHA-256
`399677d8d67733e01ac69f69d8ced789f157ad8a2a623d228645777c3c8ef082`. It lists both 1972
papers and the 1984 reprint, providing identity corroboration but no theorem text. Singh and
Natarajan's Coq formalization paper, arXiv `1912.02211v1`, was inspected with observed PDF SHA-256
`a65c6f372dfe85309585752c76c8b267d7cacaf29dfaa97eff15f39176a68fbb`; it precisely corroborates
the finite-simple-graph, all-induced-subgraphs reading. It was not built or audited as immutable
formal evidence and grants no Lean or M1 credit.

Publisher PDF retrieval was blocked, the unauthenticated publisher API did not provide full text,
and the inspected Unpaywall responses reported no open-access location for either DOI. OpenAIRE
access flags did not yield an admitted full text. No exact numbered theorem, incorporated definition,
proof passage, formula transcription, correction history, errata audit, or independent review could
therefore be admitted. This is `H1` discovery evidence, not `H0`.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- Direct pinned API sources: `Basic.lean`
  `ae6fd7c95ad151f84eb316d32c518485e9877bdda0d9eb6b4aac9e041676ad1e`;
  `Maps.lean` `60bcb9baa33451ed189091e3254004bf77f9b814a87a6ce9709042c4db6d7d2a`;
  `Clique.lean` `18cce0904728a2c5db839682aebe39f1f0ebb9213971ef9b09c93ba1a17e9cf2`;
  `Coloring.lean` `42c4c6ac9c763df08f33a9fc4cf329e19908dacc630be771a547fcb583f7be56`.
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
| `python3 scripts/stage1_target.py show THM-M-0839` | 0 | rank 1396; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6159,6164 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git rev-parse bcf3f9fa79ab8c2b6610c9875668c2589b35b74f:Docs/researches/math_theorems.md` | 0 | source-record blob `5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf` |
| Crossref, OpenAIRE, DBLP, and Unpaywall queries for the two recorded 1972 DOIs | 0 | bibliographic identities and abstract records located; no full primary text or H0 credit |
| `curl`, `sha256sum`, and `pdftotext` on Lovasz's author-hosted publication list | 0 | both 1972 sources and 1984 reprint corroborated; observed PDF SHA-256 recorded above |
| `curl`, `sha256sum`, and `pdftotext` on arXiv `1912.02211` | 0 | finite-simple-graph definition and weak theorem wording corroborated; observed PDF SHA-256 recorded above; secondary Coq lead only |
| final `sha256sum` replay on the six temporary source-discovery captures | 0 | all four metadata-response and two PDF hashes matched the recorded values; temporary inputs remain non-durable and unaccepted |
| publisher PDF and unauthenticated full-text API requests | retrieval blocked | exact definitions, theorem locator, formula, proof, and errata remain open; recorded as a source gate, not fabricated |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0839/IntakeProbe.lean)` | 0 | six complement, induce, chromatic, clique, lower-bound, and complement-clique APIs elaborated; complete output SHA-256 `305109dcab2f4d12882f073a3b7f72027f6ac511b3e86364066f763ec86f815d` |
| `rg -n -i --glob '*.lean' 'weak[ _-]*perfect[ _-]*graph\|perfect[ _-]*graph[ _-]*theorem\|(^\|[^A-Za-z])perfect[ _-]*graph([^A-Za-z]\|$)\|perfectGraph' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | no perfect-graph predicate or weak perfect graph theorem; bounded intake discovery only |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `ast.parse` on `Stage1_Instances/THM-M-0839/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0839/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, null target, exact inventory, worker packet, source hashes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0839/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| `sha256sum` on the root worker packet and every non-receipt owned intake file | 0 | raw nonrelease input hashes recorded under `dirty_input_evidence.untracked_input_hashes`; the self-referential receipt is excluded and must be hashed externally by master acceptance |
| prohibited Lean proof-escape scan over the owned path | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration in the API-only probe |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 after treating each no-index exit 1 as the expected new-file difference | no whitespace diagnostics |
| `git diff --check -- Stage1_Instances/THM-M-0839 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked-file coverage comes from the preceding no-index checks |
| final `git status --porcelain=v1 --untracked-files=all` | 0 | output SHA-256 `f7d4fa03ed896c5c59080ed1911af51a1eba32ec8603ede4c08ea386300b1733`; only the worker packet, owned dossier, and pre-existing `.lake` symlink are untracked |

## Known downstream failures

- No lawfully preserved primary full text, exact numbered result, incorporated perfect-graph
  definition, premise/conclusion/proof-boundary/errata mapping, or independent source review exists.
- Finite graph assumptions, all-induced-subgraphs quantifier, subset/subtype encoding, chromatic and
  clique codomains, coercions, complement transport, ordered binders, and boundary cases remain open.
- No canonical Lean expression, minimal-import certificate, expression/environment fingerprint,
  checked alternate encoding, or statement mutation is frozen.
- No exact formal candidate, exhaustive anchor audit, discovery and obligation freezes, typed
  graphs, proof, composition, readable reconstruction, trust closure, hermetic replay,
  deterministic bundle, independent release verification, or master acceptance exists.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze ambiguity and open
the downstream DAG. Only the integration lane may accept the provisional worker receipt.
