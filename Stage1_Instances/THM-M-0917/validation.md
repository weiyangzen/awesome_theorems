# Intake validation

Base revision: `46a0f2a3ea74765a0467c489264b838ffbb70675`; base tree:
`7b1b5269d7da840fd086da731d6f92903c209c35`. Validation date: 2026-07-13
(Asia/Shanghai). This is scoped worker evidence, not release evidence.

Validation is limited to target-set consistency, the planned dossier and open task DAG, literal
repository provenance, the source-statement ambiguity boundary, pinned environment identity, a
narrow Lean API probe, bounded local discovery, JSON/inventory hygiene, and whitespace. The catalog
does not state a truth-valued proposition, so elaborating a purported canonical theorem would
prematurely choose a definition, identity, recurrence, asymptotic, or other property. The probe
therefore supplies only M3 interface evidence and no root statement or proof credit.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned artifacts and worker packet make the final tree dirty and nonrelease.

## Environment

- Linux `7.0.0-27-generic` x86_64; timezone `Asia/Shanghai`.
- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source and search boundary

All six catalog fields originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Stage0 repeats them and leaves the exact mathematics
and evidence open. The Euler Archive page for *Introductio in analysin infinitorum*, volume 1, was
inspected as a bibliographic lead (observed HTML SHA-256
`aea040ff1d05c629927511cdc33e5aa9a88cfe6b4366c81a359940454d389a3c`), not admitted as a pinpoint
theorem source. Its linked PDF could not be completely retrieved within two bounded timeouts, so no
PDF hash, page-level statement, proof, or H credit is recorded.

A bounded repo-local and pinned-mathlib search located partition definitions, finite-cardinality
interfaces, generic generating-function infrastructure, and Glaisher's restricted identities. It
found no selected repo-local THM-M-0917 declaration. This is intake discovery, not the exhaustive
anchor audit or a claim of global external absence.

## Commands and results

All commands ran at the repository root unless another `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0917` | 0 | rank 1459; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 6707,6712 -- Docs/researches/math_theorems.md` | 0 | every uncited catalog field originates at the repository source-record commit |
| `sha256sum` on authority files, source records, toolchain, dependency lock, and pinned partition modules | 0 | hashes recorded in `instance.json` and the provisional receipt |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | pinned Lean and Lake versions above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | pinned revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0917/IntakeProbe.lean)` | 0 | eight partition/cardinality/generic-generating-function interfaces elaborated; complete stdout SHA-256 `8c70d48c...dd282a`; no target declaration or proof body |
| bounded `rg` searches for partition-function candidates in repo-local Lean and pinned mathlib | 0 or expected no match | interfaces and neighboring dossiers located; no canonical THM-M-0917 target selected |
| two bounded `curl` attempts to the Euler Archive PDF | 28 | expected external-source retrieval blocker; partial temporary downloads only, no source admitted or repository file written |
| `python3 -m json.tool` on the three owned JSON files and root worker packet | 0 | every final structured artifact is valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0917-pycache python3 -m py_compile Stage1_Instances/THM-M-0917/check_intake.py` | 0 | validator compiles without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0917/check_intake.py` | 0 | public replay verifies authority/source/pin hashes, H5/M3/R4 null-target boundary, artifact inventory, and six open tasks |
| `python3 -B Stage1_Instances/THM-M-0917/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | scoped worker packet agrees with the provisional receipt |
| prohibited-construct scan over `IntakeProbe.lean` | expected no match | no `sorry`, `admit`, `sorryAx`, axiom, constant, opaque, or unsafe declaration |
| per-file `git diff --no-index --check /dev/null FILE` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each raw exit 1 was only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0917 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; no-index checks cover untracked files |

## Open gates

An accountable truth-valued target correction or pinpoint source-statement selection, immutable
edition/page/formula inspection, definition/premise/proof/errata crosswalk, independent source
review, exact partition representation and boundary conventions, canonical Lean target, minimal
imports, expression/environment fingerprints, checked transports, and statement mutations remain
open. So do the full anchor audit, discovery protocol, obligation registry, typed graphs, proof and
composition, source/provenance/trust closure, readable reconstruction, hermetic replay,
deterministic bundle, independent release verification, and master acceptance.

These gates block ordinary statement and theorem execution but do not invalidate a truthful
self-tested `planned` intake. The H5 classification applies only to the unstable catalog gloss, and
the M3 classification gives no proof credit.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0917-INTAKE` only. It supports a planned
dossier and concrete statement blocker, not an accepted node receipt. No canonical statement, H0,
M0, R0, proof, audit completion, theorem completion, or master acceptance is claimed.
