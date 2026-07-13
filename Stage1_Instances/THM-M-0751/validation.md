# Intake validation

Base revision: `a75b2f3ac5b8b7d34eb73435734edfeecc41bd40`; base tree:
`66a22e1dc2e1c14c27bd01396a99826ab2536bf1`. Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier and all-open downstream DAG,
catalog/source provenance, the upper-semilattice versus lattice boundary, JSON and scoped
invariants, and a narrow pinned Lean interface probe. It does not validate a canonical theorem
statement or claim proof credit, because neither the catalog nor an accepted source selects the
degree model, join arity, representative construction, and exact least-upper-bound proposition.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink. It was used read-only; no update, build, clone, fetch, or other
dependency mutation was performed. The owned intake artifacts and root worker packet make the final
tree dirty as expected. All evidence here is nonrelease worker evidence.

## Source discovery boundary

Crossref metadata for the 1954 Kleene-Post paper was retrieved to `/tmp` and hashed. OpenAlex
metadata confirmed the same work and reported closed access with no repository full text. The
article itself was therefore not inspected and no theorem passage, incorporated definition,
assumption, proof node, correction, or erratum was credited.

The Encyclopedia of Mathematics API supplied immutable revision `46619`. Its wikitext says that
the set-degree and function-degree approaches form isomorphic upper semilattices, but supplies no
exact join formula or proof. It is secondary discovery evidence only. Together these sources
identify the likely family and expose why the catalog's broader "lattice" wording cannot be used as
an exact statement.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Pinned `TuringDegree.lean` SHA-256:
  `d5fd0caf5c321343ec378e2601913aec152efac58f113ce3b602dca7345b1e5c`.
- The Lean probe stdout SHA-256 is
  `2db08bbaa506acb518138880a5839687278bd0ddb20a2a8327b5aa916140802c`;
  stderr was empty.

## Commands and results

All repository commands ran at the repository root unless `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0751` | 0 | rank 1337; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 5535,5540 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of the catalog, Stage0 projection, target manifest, authoritative blueprint, skill, and execution DAG | 0 | confirmed the sparse source wording, title/gloss mismatch, planned L0 target, and exact intake boundary |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0' -sS 'https://api.crossref.org/works/10.2307/1969708' -o /tmp/thm-m-0751-kleene-post-crossref.json` | 0 | Kleene-Post 1954 bibliographic metadata retrieved; 1,613 bytes; SHA-256 `24e7b0e1...a4b`; metadata only |
| OpenAlex lookup for DOI `10.2307/1969708` with a polite API identifier | 0 | bibliographic match; closed access and no repository full text; 12,211 bytes; SHA-256 `91a9d7df...4668` |
| Encyclopedia of Mathematics API query for revision `46619` | 0 | immutable 2020-06-05 revision retrieved; upper-semilattice family statement inspected; response SHA-256 `547f7674...1224`, wikitext SHA-256 `b2e1a101...0218` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}' 'HEAD:Mathlib/Computability/TuringDegree.lean'` | 0 | pinned revision, tree, and TuringDegree source blob `e321ed033ccef4c29c9611e4d27e58116c021544` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short --untracked-files=all` | 0 | empty output; dependency worktree remained clean |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0751/IntakeProbe.lean)` | 0 | reducibility, equivalence, quotient, and partial-order APIs elaborated; no target, join, wrapper, or proof declared |
| `rg -n --glob '*.lean' 'TuringDegree\|TuringReducible\|TuringEquivalent' Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | no repo-local Turing-degree artifact found in the bounded intake search |
| `rg -n '\b(Sup\|sup\|SemilatticeSup\|Lattice\|sSup\|iSup)\b' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/TuringDegree.lean` | 1 (expected no match) | the pinned 132-line module exposes no join or supremum interface; bounded source fact, not an exhaustive external audit |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 each | all structured records valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0751-pycache python3 -m py_compile Stage1_Instances/THM-M-0751/check_intake.py` | 0 | scoped checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0751/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, pins and source hashes, H1/M4/R4 null target, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0751/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| prohibited Lean construct scan over `Stage1_Instances/THM-M-0751` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null FILE`, then scoped `git diff --check` | 0 | no whitespace diagnostics; no-index exit 1 for a new file was accepted only with empty diagnostic output |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0751-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Primary-source statement inspection and independent
review, exact degree-model and join selection, canonical Lean elaboration and mutations, anchor
audit, discovery and obligation freezes, typed graphs, proof and composition provenance, trust
closure, readable reconstruction, hermetic replay, deterministic release evidence, independent
verification, and master acceptance remain open. These gates prevent theorem completion but do not
invalidate the planned intake.
