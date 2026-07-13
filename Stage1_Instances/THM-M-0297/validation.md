# Intake validation

Base revision: `940588d30669014430d5a1beb187f2bca118e816`; base tree:
`42d80725ccbabcdd826ed2bc8b3622ac31ac7695`. Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, source-family discrimination, JSON and scoped invariants, a narrow pinned Lean substrate
probe, bounded repository/mathlib search, prohibited-construct hygiene, and whitespace. It does not
validate a canonical Marcinkiewicz statement or proof because the repository record supplies no
binder-complete proposition.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Environment

- Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target
  `x86_64-unknown-linux-gnu`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package source status was clean after the probe.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Source discovery boundary

The repository source is six uncited catalog fields and gives no formula. A later-paper reference
record identifies Marcinkiewicz's *Sur l'interpolation d'operations*, C. R. Acad. Sci. Paris 208
(1939), 1272-1273, while Crossref also returns earlier 1936 papers titled *Sur l'interpolation (I)*
and *(II)*. These locators explain the theorem family and reveal a provenance distinction, but no
complete source text, translation, theorem boundary, premise map, correction audit, immutable
repository packet, or independent H0 review was admitted.

The bounded formal search found generic interpolation mentions but no named Marcinkiewicz or
weak-type interpolation declaration. Pinned `Lp` and Chebyshev-Markov APIs elaborated and confirm
that basic measure/distribution infrastructure exists. They do not select or prove the target.

## Commands and results

All repository commands ran at the repository root unless a different `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0297` | 0 | rank 1301; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 2132,2137 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref metadata inspection for the Zygmund chapter and Marcinkiewicz interpolation works | 0 | corroborated the 1939 volume/page locator and found the separate 1936 papers; metadata only, no source accepted |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision and tree shown above |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0 and pinned toolchain identity |
| bounded case-insensitive Lean search for Marcinkiewicz and weak-type interpolation | 1 expected | no exact-topic declaration; discovery only, not an exhaustive anchor audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0297/IntakeProbe.lean)` | 0 | six adjacent pinned APIs elaborated; complete output SHA-256 `034c2dc33d13fb77d236e90236dedc00913b939a507622f35f6482e852f04258`; no target declaration or proof body |
| `python3 -B Stage1_Instances/THM-M-0297/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, input pins, null canonical target, `[H1,M4,R4]`, exact inventory, packet agreement, and six open tasks passed |
| `python3 -B Stage1_Instances/THM-M-0297/check_intake.py` | 0 | public replay mode passed without the scheduler-only packet |
| `python3 -m json.tool` on the three owned JSON files and worker packet | 0 | all parsed as JSON |
| prohibited declaration scan over owned Lean files | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null FILE` | expected differences only | no whitespace diagnostics for any new artifact |
| `git diff --check -- Stage1_Instances/THM-M-0297 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; no-index checks cover untracked files |

## Result boundary

The intake self-test passes and proposes only worker state `[_]`. Exact source admission and
statement freeze, elaboration and mutation tests, exhaustive formal-candidate audit, obligation
registry, typed graphs, proof, composition, trust closure, readable reconstruction, hermetic replay,
independent validation, deterministic release bundle, and master acceptance all remain open. This
record is not audit completion or theorem completion.
