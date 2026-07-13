# Intake validation

Base revision: `a75b2f3ac5b8b7d34eb73435734edfeecc41bd40`; base tree:
`66a22e1dc2e1c14c27bd01396a99826ab2536bf1`. Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier and all-open downstream DAG,
catalog/source provenance, proposition and neighbor boundaries, JSON and scoped invariants, and a
narrow pinned Lean vocabulary probe. It does not validate a canonical theorem statement or grant
proof credit: the catalog names an operation without selecting one proposition. The initial
worktree contained only the automation-provided untracked `Formalizations/Lean/.lake` symlink. It
was used read-only; no update, build, dependency clone/fetch, or other `.lake` mutation was
performed. This dirty worker evidence is nonrelease evidence.

## Source discovery boundary

Crossref metadata for the matching Kleene-Post 1954 paper was retrieved to temporary storage and
hashed. The version-of-record service returned an automated-access block, so no primary theorem
passage or proof was inspected. The immutable Spring 2024 Stanford Encyclopedia of Philosophy
article was also retrieved to temporary storage, hashed, and inspected at Section 3.5.2,
Proposition 3.7. It confirms the conventional relativized diagonal-halting construction and lists
several separate jump properties. This strengthens the family crosswalk but neither clears H0 nor
selects which proposition the catalog owns.

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

## Commands and results

All repository commands ran at the worker clone root unless a `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0752` | 0 | rank 1338; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 5542,5547 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of `Docs/researches/math_theorems.md:5542-5547`, `Docs/Stage0_Blueprint.md:20542-20567`, target manifest, and neighboring recursion-theory rows | 0 | sparse source wording, open fields, uniform L0 boundary, and neighbor exclusions confirmed |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0' -sS 'https://api.crossref.org/works/10.2307/1969708' -o /tmp/thm-m-0752-crossref.json` | 0 | confirmed Kleene/Post, title, Annals 59(3), May 1954, start page 379, and DOI; 1,613 bytes, SHA-256 `24e7b0e1...26a4b`; metadata only |
| version-of-record and PDF requests for DOI `10.2307/1969708` | 0 transport, blocked content | returned a 2,212-byte automated-access page, not the primary article; no statement or proof was credited |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0' -sS 'https://plato.stanford.edu/archives/spr2024/entries/recursive-functions/' -o /tmp/thm-m-0752-sep.html` | 0 | immutable secondary archive retrieved; 299,572 bytes; SHA-256 `7d856ecd...af1` |
| bounded inspection of SEP Section 3.5.2 and Proposition 3.7 | 0 | confirmed the relativized diagonal-halting construction and separate invariance, noncomputability, strictness, monotonicity, and completeness clauses; secondary discovery only |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}' 'HEAD:Mathlib/Computability/TuringDegree.lean'` | 0 | pinned revision, tree, and source blob `e321ed033ccef4c29c9611e4d27e58116c021544` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short --untracked-files=all` | 0 | empty output; dependency worktree remained clean |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions recorded above |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0752/IntakeProbe.lean)` | 0 | eight oracle-computability, reducibility, equivalence, degree, and order declarations elaborated; no jump or target theorem declared |
| bounded exact-topic `rg` over repo-local Lean outside this target | 1 (expected no match) | no repo-local exact Turing-jump artifact found; intake discovery only |
| bounded exact-topic `rg` over pinned `Mathlib/Computability` | 1 (expected no match) | no computability-theoretic Turing-jump declaration found; not a global absence claim or downstream anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured records valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0752-pycache python3 -m py_compile Stage1_Instances/THM-M-0752/check_intake.py` | 0 | scoped checker compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0752/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, planned lifecycle, null target, H1/M4/R4 boundary, normative recipe shapes, current owned-artifact hashes, candidate and neighbor inventories, receipt packet, exact artifact inventory, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0752/check_intake.py` | 0 | public replay mode passed without the scheduler-only worker packet and replayed the same receipt-bound artifact/hash invariants |
| prohibited-construct `rg` over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null FILE`, then scoped `git diff --check` | 0 | no whitespace diagnostics; no-index exit 1 for a new file was accepted only with empty diagnostic output |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0752-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact primary-source selection and independent
review, target identity, canonical Lean elaboration and mutation tests, anchor audit, discovery and
obligation freezes, typed graphs, proof and composition provenance, trust closure, readable
reconstruction, hermetic replay, deterministic release bundle, independent verification, and
master acceptance remain open. These gates prevent theorem completion but do not invalidate the
planned intake.
