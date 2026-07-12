# Anchor audit

Item: `S56-M-0996-ANCHOR_AUDIT`  
Base revision: `b15861ce0ba012fa04e8c728e6bacbc35a359aea`  
Pinned toolchain: `leanprover/lean4:v4.29.0`  
Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`

## Result

No exact or stronger Lean 4 theorem matching
`Stage1Instances.THM_M_0996.GaussianIsoperimetricTarget` was found. The pinned
mathlib tree supplies the standard Gaussian measure and coordinate transports,
one-dimensional Gaussian infrastructure, and metric-thickening facts. These are
dependency anchors only. In particular, none compares the Gaussian measure of
the thickenings of an arbitrary measurable set and an equal-measure half-space.

The retained candidates and machine-readable roles are in `anchor-audit.json`.
`AnchorAudit.lean` checks that every named declaration resolves under the pinned
toolchain. The important source locations are:

| Candidate surface | Pinned source location | Audit disposition |
|---|---|---|
| standard Gaussian and transports | `Mathlib/Probability/Distributions/Gaussian/Multivariate.lean`, declarations at lines 66-153 | useful foundation; not a root theorem |
| real Gaussian and atomlessness | `Mathlib/Probability/Distributions/Gaussian/Real.lean`, declarations at lines 199-212 | possible half-space-measure support; not a root theorem |
| open thickening geometry | `Mathlib/Topology/MetricSpace/Thickening.lean`, declarations at lines 82, 90, and 326 | statement/topology support; no Gaussian comparison |

The terminal bodies are ordinary committed mathlib declarations at the exact
revision above. No external proof body, axiom, unsafe declaration, oracle, or
placeholder is imported or credited by this audit.

## Search boundary

Repository-local searches covered the complete pinned mathlib `Mathlib` source
tree and every Lean file in the other manifest-pinned package trees for
case-insensitive combinations of Gaussian/isoperimetric and the historical names
Borell, Sudakov, and Tsirelson. There was no relevant hit; the two matches were
lexical false positives in unrelated algebra modules. Direct inspection of the
multivariate and real Gaussian declaration inventories confirmed that their
strongest nearby results concern characteristic functions, covariance, maps,
density, and atomlessness rather than isoperimetry.

For external discovery, GitHub REST repository searches for the quoted phrase
"Gaussian isoperimetric" with Lean and for `Gaussian isoperimetric language:Lean`
both returned `total_count: 0` on 2026-07-12. Since search results are mutable,
this is recorded only as negative discovery evidence. There is consequently no
external candidate whose revision, type, toolchain, dependencies, or proof body
could truthfully be audited. No dependency was fetched or mutated.

## Validation

| Command | Result |
|---|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0996/AnchorAudit.lean` | exit 0; all 12 retained declarations resolved with no diagnostics |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0996/Statement.lean` | exit 0; exact selected target still elaborates |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique ordered targets |
| `python3 -m json.tool Stage1_Instances/THM-M-0996/anchor-audit.json` | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0996` | exit 0; no output |

## Status boundary

The anchor-audit phase is self-tested and may be submitted for master
acceptance. Its result is negative with respect to root closure: the vector
remains `[H2, M3, R4]`. Primary-source fidelity, proof architecture, the exact
kernel proof, trust/provenance closure, hermetic replay, and independent review
remain open. This is neither audit completion nor theorem completion.
