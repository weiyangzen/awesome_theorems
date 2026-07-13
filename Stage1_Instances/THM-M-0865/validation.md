# Intake validation record

## Environment and scope

- Item: `S56-M-0865-INTAKE`; intent: `intake`; proposed worker state: `[_]`.
- Base commit: `748243faadc15828fb087059337fd05b7be9fdeb`; base tree:
  `e46d642646f80980838b6f016f5d69b817bd464d`.
- Toolchain: Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`;
  Lake `5.0.0-src+98dc76e`.
- Pinned mathlib: commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; dependency source was clean.
- Initial dirty boundary: the automation-provided untracked `Formalizations/Lean/.lake` symlink only.
  It and its canonical pinned target were used read-only. No update, build, clone, fetch, or `.lake`
  mutation was run.
- This is nonrelease worker evidence. It validates the planned dossier and discovery-only API probe,
  not an exact Kuratowski statement or proof.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0865` | 0 | rank 1419, planned lifecycle, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight showed only the pre-existing canonical `.lake` symlink; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | recorded base commit and tree above |
| `git blame -L 6341,6346 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 30 'https://api.crossref.org/works/10.4064/fm-15-1-271-283'` | 0 | title, author, journal volume, 1930 date, and pages 271-283 identified; metadata only, no H0 credit |
| `curl -L --fail --silent --show-error --max-time 60 -o /tmp/diestel-ch4.pdf 'https://www.math.uni-hamburg.de/home/diestel/books/graph.theory/preview/Ch4.pdf'` followed by `sha256sum`, `pdftotext -layout`, and `rg -n -C 20 'Theorem 4\\.4\\.6\|Kuratowski\|topological minor\|subdivision'` | 0 | Section 4.4 and Theorem 4.4.6 inspected; 2,085,914-byte PDF SHA-256 `bfdfbcb1e7c0df0d6fc1322ae02b11a8c7ef5c6c85f509e96ad20ad7665b15a9`; no dependency added |
| `curl -L --fail --silent --show-error --max-time 60 -o /tmp/diestel-ch1.pdf 'https://www.math.uni-hamburg.de/home/diestel/books/graph.theory/preview/Ch1.pdf'` followed by `sha256sum`, `pdftotext -layout`, and `rg -n -C 16 'finite\|simple graph\|topological minor\|subdivision'` | 0 | Sections 1.1 and 1.7 inspected; PDF SHA-256 `ebd9084653a1a534b964cbe327eeb8ab6b46a5e98deeee94280b05ebb6f37b56`; no dependency added |
| `rg -ni 'kuratowski\|planarity\|isplanar\|topological[ _-]?minor\|subdivision\|graph[ _-]?minor' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics/SimpleGraph --glob '*.lean'` | 1 (expected no match) | empty output, SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; not an exhaustive anchor audit |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib commit and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short --untracked-files=all` | 0 | empty output; dependency source stayed clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0865/IntakeProbe.lean)` preliminary | 1 | correctly exposed namespace, universe, and parser errors in the first API probe; probe was corrected without adding a target theorem |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0865/IntakeProbe.lean)` final | 0 | seven pinned graph interfaces and the universe-polymorphic predicate-parameterized shape elaborated; 1083 output bytes, SHA-256 `a2aa28f936a224e63c48b05efc5de0eef1b59aa0c8c081173689f2c3fc144e23`; no target or proof |
| `python3 -m json.tool` on all structured owned files and `.stage1-worker-selftest.json` | 0 each | valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0865-pycache python3 -m py_compile Stage1_Instances/THM-M-0865/check_intake.py` | 0 | scoped validator compiled outside the owned path |
| `python3 -B Stage1_Instances/THM-M-0865/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | authority identity, pins, H1/M4/R3 planned boundary, null target, artifact inventory, packet, receipt, Lean output, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0865/check_intake.py` | 0 | public replay mode passed without the scheduler-only root packet |
| prohibited-construct `rg` over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| changed-file final-newline, invalid-byte, and trailing-whitespace check | 0 | all ten changed files passed |
| per-new-file `git diff --no-index --check /dev/null FILE` and scoped `git diff --check` | 0 aggregate | no whitespace diagnostics; no-index difference exits were treated as expected differences |

## Source and formal boundary

Diestel's modern theorem and definition locators identify the conventional family strongly enough
for provisional H1, but the catalog does not cite that edition and the historical article text,
definition chain, corrections, exact Kuratowski-versus-Wagner ownership, premise-to-proof-node map,
and independent review remain open. No H0 is claimed.

The Lean probe authenticates `SimpleGraph`, isomorphism, plain subgraph-copy containment, and the
two obstruction graphs. The probe's `Planar` and `IsTopologicalMinor` arguments are deliberately
uninterpreted: they demonstrate only that the intended high-level binder shape parses. They do not
define the missing mathematics, elaborate a canonical target, or provide M3/M0 credit. The machine
classification remains M4.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0865-INTAKE` only. Master acceptance,
exact source and statement freeze, canonical Lean elaboration and mutations, exhaustive anchor and
provenance audit, obligation registry, typed graphs, proof, composition, trust/readability closure,
hermetic replay, deterministic release bundle, and independent verification remain open. No audit
or theorem completion is claimed.
