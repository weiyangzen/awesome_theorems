# THM-M-0414 obligation tree

The version-1 registry freezes four required obligations. The mathematical root is the exact
conjunction already frozen by `Statement.lean`; its two conjuncts are separate bridge obligations.
The trust obligation is root-critical for completion but is not a mathematical proof premise.

## Root

**Claim:** Every commutative Dedekind domain has unique factorization of integral ideals in the UFM
and explicit height-one finite-product senses. **Role:** canonical root. **Inputs:** `UFM` and
`FINPROD`. **Proof route:** obtain both uniformly in the same ring context and form the conjunction.
**Branch logic:** conjunction decomposition is exhaustive. **Formal map:**
`IdealUniqueFactorizationTarget`; conditional certificate `ObligationTree.components_compose`.
**Trust boundary:** only conditional composition is checked here. **Step ledger:** `ROOT.1` obtain
UFM; `ROOT.2` obtain FINPROD; `ROOT.3` pair them. **Boundary:** neither child body receives proof
credit in this phase. **Status vector:** `[H1, M2, R4]`.

## UFM component

**Claim:** `UniqueFactorizationMonoid (Ideal R)` for every bound `R`. **Role:** first conjunct.
**Inputs:** `CommRing R`, `IsDedekindDomain R`. **Proof route:** later integrate the pinned terminal
body `Ideal.uniqueFactorizationMonoid`. **Branch logic:** none. **Formal map:** mathlib module
`Mathlib.RingTheory.DedekindDomain.Ideal.Basic` at the pinned revision. **Trust boundary:** the anchor
audit is not transitive provenance acceptance. **Step ledger:** `UFM.1` bind context; `UFM.2` obtain
the structure body; `UFM.3` return it. **Boundary:** source pinpoint review, integration, and release
trust remain open. **Status vector:** `[H1, M2, R4]`.

## Finite-product component

**Claim:** for `I != 0`, the `finprod` of `v.maxPowDividing I` equals `I`. **Role:** second conjunct.
**Inputs:** the same ring context and a nonzero ideal. **Proof route:** later integrate
`Ideal.finprod_heightOneSpectrum_factorization`. **Branch logic:** zero is excluded; the unit ideal
is included and was separately exercised at the statement gate. **Formal map:** pinned mathlib
`DedekindDomain.Factorization`. **Trust boundary:** no computation or oracle is credited. **Step
ledger:** `FP.1` bind inputs; `FP.2` invoke the exact terminal theorem; `FP.3` preserve scope;
`FP.4` return equality. **Boundary:** no fractional-ideal strengthening or properness restriction is
introduced. **Status vector:** `[H1, M2, R4]`.

## Trust boundary

**Claim:** release requires the accepted transitive declaration, axiom, import, executable, and TCB
closure. **Role:** root-critical validation gate, separate from proof dependency. **Inputs:** both
terminal body identities and the eventual wrapper. **Proof route:** enumerate, hash, policy-check,
and independently replay. **Branch logic:** failure of any terminal closure denies release. **Formal
map:** validation and release phases. **Trust boundary:** this node is itself the disclosed boundary.
**Step ledger:** `TRUST.1` declarations; `TRUST.2` axioms; `TRUST.3` closure hashes; `TRUST.4` policy;
`TRUST.5` independent replay. **Boundary:** currently open. **Status vector:** `[H1, M2, R4]`.

All ledgers are below the 100-step split threshold. They specify the next proof surfaces; they do
not assert that the terminal bridge bodies or release gate are accepted.
