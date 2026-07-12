# THM-M-1131 frozen obligation architecture

Item: `S56-M-1131-OBLIGATION_TREE`  
Registry: `THM-M-1131-OBLIGATIONS-v1`

The registry was frozen from the exact elaborated statement and the bounded anchor audit, before
crediting the checked conditional compositions in `ObligationTree.lean`. Every leaf has a semantic
step budget at most 100. The JSON bundle separately records proof, refinement, provenance,
evidence, trust, documentation, and workflow graphs; only proof and logical-refinement edges can
affect machine closure.

## M1131-ROOT

**Claim:** The exact homogeneous isotropic conditional Fourier heat-conduction statement. **Role:**
canonical root. **Inputs:** `M1131-T-ASSEMBLE`. **Proof route:** instantiate the flux-divergence
package, then substitute its result into local energy balance. **Branch logic:** inherited from the
flux package. **Formal map:** `Stage1Instances.THM_M_1131.Statement`. **Trust boundary:** open root;
no terminal proof body. **Step ledger:** `ROOT-1`, consume the exact assembly output. **Boundary:**
the conditional composition does not prove its flux package premise. **Status vector:** `[H1,M3,R3]`.

## Material Nodes

| Anchor | Claim and role | Formal target | Budget | Status and boundary |
|---|---|---|---:|---|
| <a id="m1131-s-defs"></a>`M1131-S-DEFS` | Freeze all differential operators; definition layer for every child | `Space`, `gradient`, `divergence`, `laplacian`, `timeDerivative` | 30 | `[H1,M0-L,R3]`; elaboration is not proof |
| <a id="m1131-s-domain"></a>`M1131-S-DOMAIN` | Preserve every binder and physical regime | `Statement` | 25 | `[H1,M0-L,R3]`; source acceptance open |
| <a id="m1131-s-foundation"></a>`M1131-S-FOUNDATION` | Audit axioms and transitive TCB | planned trust report | 40 | `[H1,M4,R3]`; release gate open |
| <a id="m1131-n-flux"></a>`M1131-N-FLUX` | Rewrite flux by the constitutive hypothesis | planned exact rewrite | 35 | `[H1,M4,R3]`; no body |
| <a id="m1131-l-coord"></a>`M1131-L-COORD` | Move negation and constant scalar multiplication through each coordinate derivative | planned `fderiv` bridge | 70 | `[H1,M4,R3]`; mathlib anchors are support only |
| <a id="m1131-l-finsum"></a>`M1131-L-FINSUM` | Normalize the finite coordinate sum | planned finite-sum lemma | 35 | `[H1,M4,R3]`; no body |
| <a id="m1131-b-zero"></a>`M1131-B-ZERO` | Cover zero conductivity without cancellation | planned exact branch | 25 | `[H1,M4,R3]`; branch open |
| <a id="m1131-b-nonzero"></a>`M1131-B-NONZERO` | Cover nonzero conductivity with justified derivative identities | planned exact branch | 50 | `[H1,M4,R3]`; branch open |
| <a id="m1131-t-fluxdiv"></a>`M1131-T-FLUXDIV` | Assemble the universal flux-divergence identity | `FluxDivergencePackage` | 30 | `[H1,M4,R3]`; minimal open root cut set |
| <a id="m1131-l-balance"></a>`M1131-L-BALANCE` | Substitute flux divergence into pointwise balance | `heatEquation_of_balance_of_fluxDivergence` | 10 | `[H1,M0-L,R3]`; conditional algebra only |
| <a id="m1131-t-assemble"></a>`M1131-T-ASSEMBLE` | Compose the package into the exact public root | `statement_of_fluxDivergencePackage` | 15 | `[H1,M0-L,R3]`; package remains an explicit premise |
| <a id="m1131-x-source"></a>`M1131-X-SOURCE` | Pinpoint all material claims in primary sources | human crosswalk | 60 | `[H1,M4,R3]`; no machine proof role |
| <a id="m1131-x-provenance"></a>`M1131-X-PROVENANCE` | Inventory terminal bodies, imports, and origins | planned provenance closure | 50 | `[H1,M4,R3]`; informational overlay |

## Composition Boundary

Lean checks both the fixed-point algebra and the exact root wrapper. The sole minimal open root cut
set is `M1131-T-FLUXDIV`; its planned body must discharge all constitutive rewrite, coordinate
derivative, finite-sum, and conductivity-branch obligations. Primary-source H0, readable R0,
foundation/provenance closure, hermetic replay, independent review, and theorem completion remain
open.
