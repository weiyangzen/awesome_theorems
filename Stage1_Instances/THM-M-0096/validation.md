# Intake validation record

## Scope and environment

This record covers only the provisional planned intake node `S56-M-0096-INTAKE` on repository base
`56cce0660d633175f8e66c4a538e5c7dce64652e`, tree
`94920deccabd41cd711821885fe08d62eed67a4e`. The worker environment is Linux x86_64 in an isolated
automation clone. Its pre-existing untracked `Formalizations/Lean/.lake` symlink exposes the
canonical pinned artifacts and was used read-only. This is nonrelease evidence: no clean-room,
cold-cache, offline-replay, second-runner, signature, or master-acceptance claim is made.

The Lean surface is version `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, with Lake `5.0.0-src+98dc76e` and pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. No `lake update`, `lake build`, dependency fetch,
clone, or `.lake` mutation was run.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0096` | 0 | rank 1113, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| `git status --short --untracked-files=all` before edits | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was present |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 705,710 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| inspection of pinned mathlib module docs and `docs/references.bib` | 0 | Serre 1987 Ch. V Sections 4 and 6 and Geck 2017 bibliographic leads recorded; cited works were not independently fetched or inspected, so no H0 credit |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | exact versions recorded above; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision/tree recorded; package worktree clean |
| bounded `rg` search for Chevalley/integral bases and `Z`-forms in repo-local Lean and pinned mathlib | 0 with unrelated hits | explicit Lie-basis TODOs and number-field integral-basis names found; no terminal THM-M-0096 theorem located; scoped discovery only |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0096/IntakeProbe.lean)` | 0 | nine adjacent pinned declarations elaborated; stdout SHA-256 `4765c4f5a9fe359aadf00e1a433b812c2dea6a41f5e663f43e4091b561e38d81`; no canonical target or proof body declared |
| `python3 -m json.tool` on owned JSON files and root packet | 0 | all structured artifacts parsed as JSON after finalization |
| Python `compile` of `check_intake.py` | 0 | validator parsed without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0096/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, pins and hashes, H1/M4/R4 null target, inventory, packet, receipt recipes, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0096/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited declaration scan over `IntakeProbe.lean` | 1, expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check /dev/null` plus scoped `git diff --check` | 0 aggregate | no whitespace diagnostics |

## Known open gates

Exact source identity and statement selection remain open, as do complete definition, assumption,
conclusion and proof-node mapping, correction and historical-attribution review, lawful immutable
source admission, and independent review. The scalar field, characteristic, finite dimensionality,
semisimplicity encoding, Cartan/root/sign choices, meaning of integral basis, bracket relations,
`Z`-form transport, normalization or uniqueness scope, and boundary cases are not frozen.

Pinned mathlib's `LieAlgebra.Basis` is explicitly weaker than a Chevalley basis, whose definition
and general existence remain TODO. The Geck and Serre declarations construct particular algebras
from root or Cartan data and cannot replace the received root without checked equivalence. Canonical
Lean target, minimal imports, expression and environment fingerprints, transports, statement
mutations, exhaustive anchor audit, discovery protocol, obligation registry, typed graphs, proof,
composition, readable reconstruction, trust closure, hermetic replay, independent verification,
master acceptance, audit completion, and theorem completion all remain open.

## Status boundary

This is provisional worker self-test evidence for `S56-M-0096-INTAKE` only. It supports a planned
dossier proposal, not an accepted node receipt. No exact statement, H0 source closure, proof, audit
completion, theorem completion, or master acceptance is claimed.
