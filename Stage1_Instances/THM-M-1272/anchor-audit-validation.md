# THM-M-1272 anchor-audit validation

Item: `S56-M-1272-ANCHOR_AUDIT`  
Audit date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `3a3bd9b5ae3837526b6a41daf06c7587654c209d`

## Decision

The exact frozen Fountain proposition elaborates, but no proof-bearing exact anchor was found.
Pinned mathlib supplies genuine Frechet-calculus, local-minimum criticality, Hilbert-basis,
orthogonal-splitting, and sequence infrastructure. It has no Fountain, Palais-Smale, genus,
deformation, or applicable variational minimax theorem. These declarations are nonterminal anchors.

The repository's historical `S1_M_165.lean` is also nonterminal. Its `StatementShape` is conditional
on a `FountainHypotheses` value whose hard Palais-Smale and minimax claims are proposition-valued
fields accompanied by proofs. It is not definitionally or propositionally a proof of the frozen
root and earns no inherited proof credit.

Every locally installed Lake dependency was checked at the exact manifest revision, and all source
trees were searched. The only semantic dependency hit was an unrelated prose mention of a
statistical minimax theorem. Five GitHub repository searches were attempted, but the shared
unauthenticated quota returned HTTP 403; grep.app returned HTTP 503. No failed endpoint result was
counted as evidence, and the audit makes no exhaustive-web claim. No external candidate with a
declaration, proof body, toolchain, license, and immutable revision was found to integrate.

The root therefore remains `M3 / not_repo_local_closed`. This completes the bounded candidate
inventory for master review only. It does not prove, validate, release, or complete the theorem.

## Commands and exact results

Commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` using the existing
pinned `.lake` artifacts.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks passed |
| `python3 scripts/stage1_target.py show THM-M-1272` | 0 | rank 165, planned, theorem incomplete |
| manifest-to-HEAD check for every installed Lake dependency | 0 | all 11 installed source trees equal their immutable manifest revisions |
| pinned dependency `rg` alias/semantic search | 0 | one unrelated statistical-minimax prose hit; no Fountain/Palais-Smale/genus/deformation candidate |
| five GitHub repository API queries | 0 (curl) / HTTP 403 | shared unauthenticated search quota exhausted; no result credited |
| three grep.app queries | 0 (curl) / HTTP 503 | non-JSON service-unavailable responses; no result credited |
| `lake env lean ../../Stage1_Instances/THM-M-1272/Statement.lean` | 0 | exact target and checked consequence elaborated |
| `lake env lean AwesomeTheorems/Stage1/S1_M_165.lean` | 0 | legacy conditional scaffold and explicit non-completion boundary elaborated |
| `lake env lean ../../Stage1_Instances/THM-M-1272/AnchorAudit.lean` | 0 | four typed wrappers and twelve pinned mathlib API probes elaborated |
| `python3 ../../Stage1_Instances/THM-M-1272/check_anchor_audit.py` | 0 | statement/source hashes, 11 pins/HEADs, witnesses, candidate ledger, and open-root boundary passed |
| `python3 -m json.tool Stage1_Instances/THM-M-1272/anchor-audit.json` | 0 | valid JSON |
| forbidden-token scan of new executable artifacts | 1 | no forbidden proof placeholder or axiom declaration; exit 1 is the expected no-match result |
| `git diff --check -- Stage1_Instances/THM-M-1272 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The clone's pre-existing untracked `Formalizations/Lean/.lake` link reuses canonical pinned
artifacts. No Lake update/build, dependency clone/fetch, or `.lake` mutation occurred.
