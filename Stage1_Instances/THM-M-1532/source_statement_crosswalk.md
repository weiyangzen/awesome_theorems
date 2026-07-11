# Source-statement crosswalk

| Claim component | Source discovery anchor | Lean target | Intake assessment |
|---|---|---|---|
| Repository claim: "the Standard Model of particle physics" | `Docs/Stage0_Blueprint.md`, THM-M-1532; no proposition, premises, or conclusion supplied | none | The label is not elaborable as `Prop`; source-statement gate fails |
| Electroweak gauge theory | S. Weinberg, *A Model of Leptons*, Physical Review Letters 19 (1967), 1264-1266, DOI 10.1103/PhysRevLett.19.1264 | none selected | Primary historical component, not a theorem asserting the complete modern Standard Model |
| Unified weak/electromagnetic interaction | A. Salam, *Weak and Electromagnetic Interactions*, in *Elementary Particle Theory* (1968), pp. 367-377 | none selected | Historical component; edition, pages, conventions, and premise mapping require audit |
| Quark gauge structure and asymptotic freedom | D. J. Gross and F. Wilczek, *Ultraviolet Behavior of Non-Abelian Gauge Theories*, Physical Review Letters 30 (1973), 1343-1346, DOI 10.1103/PhysRevLett.30.1343; H. D. Politzer, *Reliable Perturbative Results for Strong Interactions?*, ibid. 1346-1349, DOI 10.1103/PhysRevLett.30.1346 | none selected | QCD anchors do not turn the aggregate theory into one proved proposition |
| Modern field/representation/Lagrangian specification | No authoritative convention-bearing source was supplied by repository metadata | candidate definitions only | Must freeze gauge group quotient convention, generations, representations, neutrino sector, parameters, spacetime, and classical/quantum semantics |
| Empirical success | Repository says `已验证` ("verified") without an artifact | not eligible as kernel closure | Experimental confirmation and parameter fitting must not be relabeled as theorem proof |

No `H0` claim is made. A later source audit must pin immutable editions, inspect errata, and choose a
precise proposition whose assumptions and conclusion can be mapped premise by premise. Until then,
creating a Lean wrapper would broaden, narrow, or substitute the received claim.
