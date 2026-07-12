# Anchor-audit validation record

Item: `S56-M-1119-ANCHOR_AUDIT`  
Audit date: `2026-07-12`  
Base revision: `110eef5926707beba105078ad2163c88ae8bf0e8`

## Decision

The exact local artifact is the elaborated proposition
`Stage1Instances.THM_M_1119.KestenTarget`, not a proof declaration. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` provides the Bernoulli product-measure, graph
reachability, and infimum substrate checked in `AnchorAudit.lean`; a recursive search found no
percolation, infinite-cluster, critical-probability, square-lattice, or Kesten theorem declaration.

Bounded public searches found no exact Lean 4 candidate. An exact-phrase Sourcegraph query returned
zero matches. A broader query returned only a number-theoretic result attributed to Kesten and the
finite Van den Berg-Kesten-Reimer inequality. The latter was inspected at immutable cam-combi commit
`1c8502fd40113ba0141652c23d542e04c1aa872d`: it is mathematically non-equivalent to the target and
its terminal `Finset.card_certificator_le` body is `sorry`. It also uses Lean 4.31.0 and mathlib
`fabf563...`, outside this pinned closure. It is rejected, not treated as an anchor or proof.

The exact root therefore remains `M4`: no proof candidate exists to integrate. This is a complete
bounded anchor audit, not theorem completion and not a claim that no formalization exists anywhere.

## Commands and results

Commands ran in this worker clone. Lean used only the existing pinned Lake environment. No update,
build, clone, fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `rg -n -i 'percolat\|infinite.?cluster\|critical probability\|square lattice\|kesten' Formalizations/Lean/.lake/packages/mathlib/{Mathlib,Archive} -g '*.lean'` | 1 | no match in pinned mathlib source; exit 1 is the expected no-match result |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest pin `8a178386...ea95` |
| Sourcegraph exact-phrase public search | 0 | exhaustive `matchCount=0`; response SHA-256 `6906ea4e...eb7` |
| Sourcegraph broad `Kesten OR percolation` search | 0 | 10 exhaustive but unrelated matches; response SHA-256 `72422e69...002` |
| GitHub repository searches `percolation lean4` and `Kesten Lean` | 0 | both complete with `total_count=0`; response SHA-256 `08c082fd...b2` |
| immutable raw inspection of `YaelDillies/cam-combi@1c8502f...` | 0 | non-equivalent BK-Reimer lemma; `sorry` at source line 105; Lean 4.31.0, mathlib `fabf563...`, Apache-2.0 |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1119/AnchorAudit.lean` | 0 | eight pinned substrate declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1119/Statement.lean` | 0 | exact target and checked transport re-elaborated |
| `python3 Stage1_Instances/THM-M-1119/check_anchor_audit.py` | 0 | structured audit, pin, probes, rejection, and M4 boundary agree |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1,546 uniform-L0 targets pass |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546 |
| `python3 scripts/stage1_target.py show THM-M-1119` | 0 | rank 559; planned; L0/rework-required; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1119 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Reopen gate

Reopen integration only for an exact candidate with an immutable revision, compatible toolchain,
dependency and license record, exact-type comparison, terminal proof-body provenance, and explicit
placeholder, axiom, and unsafe/oracle checks. Until it is pinned or vendored and a local exact
wrapper checks, no `M0-P`, `M0-W`, `M1`, or theorem-completion credit is valid.
