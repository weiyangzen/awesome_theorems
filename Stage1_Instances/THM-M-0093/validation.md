# Intake validation

Base revision: `cea7a197878ce23e819b006b2780b0bb1702fbbe` (tree
`079dc70c0b48278054700d1b4d45efee14a3bd04`). Validation date: 2026-07-13
(Asia/Shanghai).

This validation covers the planned dossier, highest-weight scope and non-substitution boundaries,
six-node open task DAG, structured intake invariants, and a narrow pinned Lean API probe. It does
not validate a canonical classification proposition or proof because neither has been frozen. The
automation-provided canonical `.lake` symlink was pre-existing and used read-only; no dependency
update, build, clone, fetch, or other `.lake` mutation was performed. This dirty worker run is
nonrelease evidence.

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

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0093` | 0 | rank 1110, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` | 0 | preflight contained only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 684,689 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded inspection of Etingof's author-issued MIT 18.745 full lecture notes | 0 | Section 25 setup plus Definition 25.4, Propositions 25.5 and 25.12-25.14, Corollary 25.13, Lemmas 25.15-25.16, and Theorem 25.17 on printed pages 132-137 inspected; PDF digest `908b49bd938da6b28f2bceb01311028c8f453c721af6830ce0e32a1e52b6b929`; H1 lead only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above; package status clean |
| bounded `rg` search for highest-weight, dominant-integral-weight, and Verma classification in repo-local Lean and pinned mathlib | 0 with unrelated hits, plus narrower no-match checks | only semistandard-tableau terminology and abstract affine predicates in another legacy target were found; no terminal classification was located; intake discovery only, not an exhaustive external audit |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0093/IntakeProbe.lean)` | 0 | eleven adjacent pinned Lie-module, Cartan, weight-space, root-system, and enveloping-algebra APIs elaborated; no target declaration or proof body |
| `python3 -m json.tool` on the three owned JSON files and root worker packet | 0 | structured artifacts are valid JSON after finalization |
| `python3 -c` with `ast.parse` on `check_intake.py` | 0 | validator parsed without writing generated files into the owned path |
| `python3 -B Stage1_Instances/THM-M-0093/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, pins and hashes, H1/M4/R4 null target, inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0093/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| Lean declaration scan for prohibited proof escapes in `IntakeProbe.lean` | 1, expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null` plus scoped `git diff --check` | 0 aggregate | no whitespace diagnostics |

## Known open gates

Exact source selection remains open, as do a complete definition/assumption/conclusion/proof-node
map, correction and historical-attribution audit, lawful immutable source admission, and independent
review. The scalar field, characteristic, finite-dimensionality, splitting, semisimplicity,
Cartan/Borel/positive-root data, weight lattice, dominant-integral predicate, representation and
irreducibility encoding, isomorphism classes, classification direction, and boundary cases are not
frozen.

Pinned mathlib's root-system construction assumes a nondegenerate Killing form, while the catalog
says semisimple; the reverse bridge is not present in the pinned library. This adjacent API cannot
be used to narrow the theorem silently. Canonical Lean target, minimal imports, expression and
environment fingerprints, checked transports, statement mutations, exhaustive anchor audit,
discovery protocol, obligation registry, typed graphs, proof and composition, trust and provenance
closure, readable reconstruction, hermetic replay, deterministic bundle, independent verification,
master acceptance, audit completion, and theorem completion all remain open.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0093-INTAKE` only. It supports a planned
dossier, not an accepted node receipt. No canonical statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
