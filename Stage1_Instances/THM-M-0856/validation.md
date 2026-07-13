# Intake validation

Base revision: `1c0c5fc6f43e6ae5ecc3b50589b45c3628e0ead4`

Base tree: `61214aa2a03c032134ddc4958b1df63df3430a85`

## Validated boundary

Validation covers only the `planned` intake dossier, source and scope discrimination, the six-node
open downstream task DAG, a bounded direct-candidate search, and a discovery-only pinned Lean probe.
It does not establish a canonical statement fingerprint, source fidelity, proof-body provenance,
machine closure, audit completion, or theorem completion.

The worker input was nonrelease-dirty before these artifacts were created because
`Formalizations/Lean/.lake` is an automation-provided untracked link to the canonical pinned Lake
artifacts. It was reused read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was run.

## Environment

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- mathlib `Tutte.lean`: SHA-256
  `47072b914aa564222ef8013092c38fa62227fea8230e308cc3eb5f11afcdffc3`
- candidate origin: mathlib commit `358193a686dedec6d9d4d69374d1bdd6ecad9b25`, verified ancestor
  of the pin

## Commands and results

All commands ran in this worker clone unless a working directory is stated otherwise.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0856` | 0 | rank 1410; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` before editing | 0 | only the pre-existing `Formalizations/Lean/.lake` link; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 6278,6283 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref work lookup for DOI `10.1112/jlms/s1-22.2.107` | 0 | confirmed Tutte, article title, April 1947, journal, volume/issue, and pages 107-111; response SHA-256 `5d0dbb...22a5` |
| OpenAlex work lookup for the same DOI | 0 | confirmed bibliographic identity and reported no open full text; response SHA-256 `d3c5f6...2532` |
| bounded `rg` search for `Tutte`, `IsTutteViolator`, `theorem tutte`, and `perfect matching` in repo-local Lean and pinned mathlib SimpleGraph sources | 0 | found direct pinned `SimpleGraph.tutte` and supporting matching/odd-component APIs; no repo-local THM-M-0856 module |
| `git -C Formalizations/Lean/.lake/packages/mathlib merge-base --is-ancestor 358193a686dedec6d9d4d69374d1bdd6ecad9b25 HEAD` | 0 | candidate-introduction commit is an ancestor of the pinned mathlib revision |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0856/IntakeProbe.lean` | 0 | candidate definition, perfect-matching predicate, and theorem type elaborated; axioms printed as `propext`, `Classical.choice`, `Quot.sound`; output SHA-256 `919587...8351` |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all four JSON documents parsed after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0856-pycache python3 -m py_compile Stage1_Instances/THM-M-0856/check_intake.py` | 0 | scoped validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0856/check_intake.py` | 0 | authority, planned H1/M3/R4 boundary, pins, candidate, exact inventory, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0856/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | the same checks plus receipt/worker-packet agreement passed |
| prohibited Lean construct scan over `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped per-new-file whitespace checks and `git diff --check -- Stage1_Instances/THM-M-0856 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Known open gates

An admitted primary text, exact theorem locator and incorporated definitions, complete
assumption/conclusion/proof-boundary/correction crosswalk, and independent source review remain
open. So do canonical Lean target selection, minimal imports, expression and environment
fingerprints, checked alternate transports, all four mutation classes, exhaustive formal anchor and
terminal-body audit, discovery and obligation freezes, typed graphs, proof/composition acceptance,
readable reconstruction, trust closure, hermetic replay, deterministic evidence, independent
release verification, and master acceptance. These open gates prevent theorem completion but do not
invalidate the self-tested planned intake.
