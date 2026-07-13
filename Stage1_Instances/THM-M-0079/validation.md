# Historical intake validation

This file preserves the earlier intake run and is not current statement evidence. The intake
checker pins its pre-statement base, generated authority hashes, and nine-file inventory, so it is
expected to reject the expanded statement dossier. Current evidence is in `statement-validation.md`.

## Scope and environment

- Item: `S56-M-0079-INTAKE`
- Intent: `intake`
- Base revision: `0d2c3bdcd192266bc255ac3d5186da604517145a`
- Base tree: `eafbcb48efd51d9cda34f0fc1afe780434abad64`
- Worktree boundary: nonrelease worker checkout. Before this dossier was created, `git status
  --short --untracked-files=all` reported only the automation-provided
  `Formalizations/Lean/.lake` symbolic link. It points to the canonical pinned dependency artifacts
  and was inspected read-only; no update, build, fetch, clone, or `.lake` mutation was run.
- Toolchain: Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`,
  `x86_64-unknown-linux-gnu`; Lake `5.0.0-src+98dc76e`.
- Pinned mathlib: revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`.
- Validation class: narrow, warm, nonhermetic worker self-test. This is not a clean-room, cold-cache,
  offline replay, deterministic evidence bundle, or independent-runner result.

## Source and statement result

The repository's unrestricted claim is frozen as "every subgroup of a free group is free."
Crossref metadata provides a 1927 Schreier primary-paper lead, but no primary theorem text was
available for inspection, and the repository's 1921 joint attribution remains historically
unresolved. Thus the source is `H1`, not `H0`.

The candidate Lean shape
`{G : Type u} -> [Group G] -> [IsFreeGroup G] -> (H : Subgroup G) -> IsFreeGroup H`
and the pinned `subgroupIsFreeOfIsFree` application elaborate. They remain candidate-only: the
canonical expression, transports, expression and environment fingerprints, mutations, wrapper,
terminal-body provenance, transitive trust closure, and accepted axiom policy are downstream.

## Commands and observed results

All paths below are repository-relative. Commands without a stated `cwd` ran at the repository
root.

| Command | Exit | Observed result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok` with 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok` with 1546 unique targets, ranks 1..1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0079` | 0 | rank 1105, planned, L0/rework required, no legacy slot, legacy artifacts unaccepted, theorem complete false |
| `git status --short --untracked-files=all` | 0 | initial status contained only the pre-existing automation `.lake` link; final status adds only this assigned dossier and the authorized root worker packet |
| `git blame -L 582,587 -- Docs/researches/math_theorems.md` | 0 | all catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 30 -H 'User-Agent: awesome-theorems-stage1-intake/1.0 (mailto:noreply@example.invalid)' https://api.crossref.org/works/10.1007/BF02952517 -o /tmp/thm-m-0079-crossref.json` | 0 | metadata identified Schreier's 1927 paper, volume 5(1), pages 161-183; response SHA-256 `84b9c8...b3f7` |
| `curl -L --fail --silent --show-error --max-time 30 https://eudml.org/doc/159170 -o /tmp/thm-m-0079-eudml.html` | 22 | HTTP 403; no article text was inspected or credited |
| `lake env lean --version` (`cwd=Formalizations/Lean`) | 0 | Lean 4.29.0 at commit `98dc76e3...` for x86_64 Linux |
| `lake --version` (`cwd=Formalizations/Lean`) | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned revision and tree matched the intake record |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain=v1 --untracked-files=all` | 0 | empty output; pinned mathlib dependency worktree was clean |
| `lake env lean ../../Stage1_Instances/THM-M-0079/IntakeProbe.lean` (`cwd=Formalizations/Lean`) | 0 | candidate declaration and both generic/literal-carrier applications elaborated; axioms reported `propext`, `Classical.choice`, `Quot.sound` |
| `python3 -m json.tool` for the three owned JSON files | 0 | all JSON parsed after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0079-pycache python3 -m py_compile Stage1_Instances/THM-M-0079/check_intake.py` | 0 | scoped validator compiled without writing inside the owned dossier |
| `python3 Stage1_Instances/THM-M-0079/check_intake.py` | 0 | manifest/DAG identity, lifecycle, hashes, scope boundary, empty accepted state, artifact inventory, and open task chain agreed |
| `python3 Stage1_Instances/THM-M-0079/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | final packet identity, changed paths, base, failures, and provisional state agreed |
| `rg -n --glob '*.lean' '\\b(sorry\|admit)\\b\|\\bsorryAx\\b\|^\\s*axiom\\b' Stage1_Instances/THM-M-0079` | 1 | no proof holes or bodyless axiom declarations found in the intake probe; exit 1 means no matches |
| `git diff --check -- Stage1_Instances/THM-M-0079 .stage1-worker-selftest.json` | 0 | no whitespace errors after finalization |

## Structured recipes

The provisional receipt records four narrow recipes as argv arrays: the standard validator, target
manifest validator, scoped intake validator, and `lake env lean` probe. All deny network and cover
intake structure or discovery-only declarations, not any accepted theorem obligation.

## Gate result

The intake self-test passes as a provisional `planned` dossier. `audit_complete=false` and
`theorem_complete=false`. The first theorem gate remains the dependent statement phase: freeze and
mutation-test the exact Lean expression and source boundary. Primary-source review, immutable
anchor and provenance audit, obligation registry, proof integration, trust closure, hermetic replay,
independent verification, release, and master acceptance are all open.
