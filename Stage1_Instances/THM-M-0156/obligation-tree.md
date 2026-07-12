# THM-M-0156 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 16 canonical obligations from the exact rectangular statement and the
immutable anchor inventory. The candidate route was selected before this phase credited any proof
closure. The source, provenance, trust, documentation, and workflow nodes are typed support
boundaries and cannot be counted as mathematical proof premises.

## Typed proof route

```text
M0156-ROOT exact DivergenceTheoremTarget [open M3]
`-- M0156-T-ASSEMBLE checked conditional composition
    `-- M0156-T-ADAPTER specialize the exception set to empty
        |-- M0156-B-CANDIDATE pinned off-countable mathlib theorem [candidate only]
        `-- M0156-L-EMPTY empty set is countable [checked M0-L]
```

The refinement graph separately records the exact binder/hypothesis package, coordinate trace,
signed face flux, and degenerate cases. The proof graph contains reciprocal `proof_requires` and
`composes` edges. No provenance, source, trust, evidence, documentation, or workflow edge can close
the root.

## Node ledgers

### m0156-root

**Claim:** the exact `DivergenceTheoremTarget`. **Role:** canonical root. **Inputs:** only the
assembly child. **Proof route:** consume the exact adapter result. **Branch logic:** no domain case
is removed. **Formal map:** `Statement.lean`. **Trust boundary:** pending. **Step ledger:** ROOT-1,
assembly output to identical target. **Boundary:** open. **Status vector:** `[H1, M3, R4]`.

### m0156-b-candidate

**Claim:** the pinned off-countable divergence theorem supplies the stronger package. **Role:** sole
remaining machine cut. **Inputs:** mathlib hypotheses and a countable exceptional set. **Proof
route:** later proof phase must bind the audited declaration to the package. **Branch logic:** none.
**Formal map:** `MeasureTheory.integral_divergence_of_hasFDerivAt_off_countable` at mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. **Trust boundary:** terminal provenance and transitive
trust remain unaccepted. **Step ledger:** CAND-1, exact theorem to package. **Boundary:** candidate,
not accepted proof credit. **Status vector:** `[H1, M0-W-candidate, R4]`.

### m0156-l-empty

**Claim:** the empty exception is countable. **Role:** discharges the adapter boundary case.
**Inputs:** none. **Proof route:** `Set.countable_empty`. **Branch logic:** empty membership is
impossible. **Formal map:** `ObligationTree.empty_exception_is_countable`. **Trust boundary:** kernel
checked. **Step ledger:** EMPTY-1, apply the library set fact. **Boundary:** proves no divergence
identity. **Status vector:** `[H1, M0-L, R4]`.

### m0156-t-adapter

**Claim:** the off-countable package implies the no-exception target. **Role:** exact transport.
**Inputs:** candidate package and the empty-set leaf. **Proof route:** instantiate the exception set
with `empty`; project the interior conjunct. **Branch logic:** all dimensions and degenerate boxes
remain universally quantified. **Formal map:** `ObligationTree.root_of_offCountablePackage`.
**Trust boundary:** kernel checked conditionally. **Step ledger:** ADAPT-1 select empty; ADAPT-2 pass
countability; ADAPT-3 transport derivative premise; ADAPT-4 return equality. **Boundary:** does not
supply the candidate premise. **Status vector:** `[H1, M0-L, R4]`.

### m0156-t-assemble

**Claim:** the adapter output is definitionally the exact root. **Role:** root composition.
**Inputs:** adapter. **Proof route:** direct checked output. **Branch logic:** none. **Formal map:**
`ObligationTree.root_of_offCountablePackage`. **Trust boundary:** conditional only. **Step ledger:**
ASSEMBLE-1, return adapter output. **Boundary:** root stays open until the candidate and later gates
are accepted. **Status vector:** `[H1, M0-L, R4]`.

## Status

The minimal open root cut is `M0156-B-CANDIDATE`. Primary-source acceptance, terminal-body and
transitive trust closure, readable review, proof-phase acceptance, hermetic replay, independent
verification, and release remain open. Audit completion and theorem completion are both false.
