# Anchor audit record

Item: `S56-M-0441-ANCHOR_AUDIT`  
Base revision: `8932ac8a67df919ccd98afecae003a1de4988008`

## Frozen target

This audit is against `Stage1Instances.THM_M_0441.PilaWilkie`, expression SHA-256
`103f282fc63e0dfa6ac9de4f13736044bf5131a41883196fdca531df00a5a475`. It does not
audit a weakened predicate package or the legacy `StatementShape`.

## Pinned mathlib

The manifest pins mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` and Lean at
`v4.29.0`. `AnchorAudit.lean` checks the usable leaves: first-order parameter-definability,
ring-language definability over `Real`, connected/nontrivial sets, finite-set cardinality, and real
exponentiation. A source search of the pinned mathlib, `flt-regular`, and this repository found no
Pila-Wilkie declaration, o-minimal geometry library, or subpolynomial rational-point counting proof.
These are statement ingredients only, not a terminal anchor.

## External Lean 4 candidates

Repository discovery used the GitHub repository API on 2026-07-12. Exact-name searches
`PilaWilkie language:Lean` and `Pila-Wilkie language:Lean` returned zero repositories. Broader
o-minimal searches returned the three candidates below; their immutable trees, manifests, and
central o-minimality sources were inspected at the listed commits.

| Candidate and immutable revision | Toolchain / mathlib | Finding | Integration decision |
|---|---|---|---|
| `theominimalist/monotonicity@6e3ee129f0d9cc0d9d6a58cac4fc03bc7b121b30` | no toolchain or manifest in tree | custom o-minimal structure and monotonicity material; no Pila-Wilkie/counting module | infeasible: no pinned package boundary or exact closure |
| `tonysf/lean-OMIN@fd8b4f3423265d9beb290a08992ad866eb5230e0` | Lean `v4.30.0-rc1`; mathlib `f8770bc8...` | substantial custom `OMinStructure`; milestone results are fields such as `cellDecomposition_axiom`; no rational-height/algebraic-part/Pila-Wilkie theorem | infeasible: incompatible pins and no terminal proof body |
| `KittySaya/Lean-ominimal@4429c2cc75e49a83043175f7a85c4c1bf284c2eb` | Lean `v4.19.0-rc3`; mathlib `44efe040...` | pure dense-order example and basic definability; no real-field rational-point counting | infeasible: incompatible older pins and wrong theorem surface |

No candidate is imported or credited. In particular, a structure field carrying a theorem-shaped
assumption is an interface boundary, not terminal proof provenance. No candidate supplies a checked
transport to the canonical declaration.

## Validation

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0441/AnchorAudit.lean` from `Formalizations/Lean` | 0 | all pinned mathlib anchor types elaborated and requested declarations printed |
| `lake env lean ../../Stage1_Instances/THM-M-0441/Statement.lean` from `Formalizations/Lean` | 0 | frozen canonical statement still elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0441/anchor-audit.json` | 0 | structured audit parsed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target coverage passed |
| `python3 scripts/stage1_target.py check` | 0 | ordered uniform-L0 manifest passed |
| `python3 scripts/stage1_target.py show THM-M-0441` | 0 | rank 87, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0441` | 0 | no whitespace errors |

The repo-local inventory command was
`rg -n -i --glob '*.lean' 'Pila.?Wilkie|o.?minimal|ominimal|rational points|algebraicPart|subpolynomial' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/.lake/packages/flt-regular Formalizations/Lean/AwesomeTheorems`
(exit 0: matches occurred only in generic rational-point material and the legacy local boundary;
there was no dependency closure). External discovery used `curl --get
https://api.github.com/search/repositories --data-urlencode 'q=<query>' --data per_page=10`, then
`curl https://api.github.com/repos/<repository>/commits/HEAD` to freeze the returned heads and
`curl 'https://api.github.com/repos/<repository>/git/trees/<commit>?recursive=1'` for each immutable
tree (all exit 0). Raw manifests and central sources were read from
`https://raw.githubusercontent.com/<repository>/<commit>/<path>` (all exit 0). The six query counts,
in the order recorded in `anchor-audit.json`, were `0, 0, 2, 1, 0, 0`.

Phase verdict: the immutable candidate inventory and integration-feasibility audit are complete and
self-tested, pending master acceptance. Machine status remains `M3`; no exact closure was found.
The theorem, human-proof audit, obligation tree, trust closure, replay, and release gates remain open.
