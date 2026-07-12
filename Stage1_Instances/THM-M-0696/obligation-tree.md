# THM-M-0696 obligation tree

Item: `S56-M-0696-OBLIGATION_TREE`. Registry version: 1. The immutable denominator is recorded in
`obligation-registry.json`; this page is a provisional readable map, not proof evidence.

## Architecture

The selected route is contraposition. From `Gamma` not deriving `phi`, first use a deduction
theorem to show that `Gamma` extended by `not phi` is consistent. Extend that seed to a maximal
consistent theory without assuming that atoms are countable. Interpret an atom as true precisely
when its formula is derivable in the maximal theory, prove a truth lemma by formula induction, and
obtain a valuation satisfying `Gamma` while falsifying `phi`. The checked
`completeness_of_countermodel` declaration converts that exact countermodel package into the frozen
root.

The route deliberately does not use the external Foundation theorem. That endpoint has different
syntax, calculus, atom assumptions, context shape, and toolchain, so it is only a provenance edge.

## M0696-ROOT

**Claim:** The exact arbitrary-`Set` semantic-consequence completeness target. **Role:** canonical
root. **Inputs:** `M0696-T-ASSEMBLE`. **Proof route:** consume the countermodel theorem through the
checked contrapositive composition. **Branch logic:** a derivation exists, or its negation supplies
the countermodel premise. **Formal map:** `PropositionalCompletenessTarget`. **Trust boundary:** no
root proof body exists. **Step ledger:** ROOT-1 uses ASSEMBLE-OUT to return the exact target.
**Boundary:** `[H1, M3, R3]`; no theorem closure is claimed.

## M0696-S-ENCODING

**Claim:** The selected false/implication syntax, Boolean evaluation, arbitrary set contexts, and
K/S/DNE/MP calculus have the frozen meanings. **Role:** fixes every later signature. **Inputs:**
`Statement.lean`. **Proof route:** definitions elaborate directly. **Branch logic:** formula
constructors are atom, falsum, implication. **Formal map:** `Formula`, `Satisfies`,
`SemanticallyEntails`, `Derives`. **Trust boundary:** interface elaboration only. **Step ledger:**
ENC-1 unfolds each named definition at its use. **Boundary:** `[H1, M3, R3]`.

## M0696-S-BOUNDARY

**Claim:** Empty premises, falsum premises, and empty atom types behave as stated. **Role:** prevents
silent scope narrowing. **Inputs:** the frozen encoding. **Proof route:** execute the three checked
boundary theorems. **Branch logic:** empty context does not entail an atom; a falsum context has no
model; a member premise is derivable. **Formal map:** the three `*_boundary` theorems.
**Trust boundary:** local Lean bodies only. **Step ledger:** BND-1 through BND-3 correspond to those
three cases. **Boundary:** `[H1, M3, R3]`; this does not prove completeness.

## M0696-S-FOUNDATION

**Claim:** The eventual declaration's exact axiom set is accepted under a versioned foundation
profile. **Role:** release gate. **Inputs:** all terminal declarations. **Proof route:** machine
`#print axioms` plus dependency audit. **Branch logic:** object-level DNE is part of the calculus;
meta-level choice and extensionality are separate. **Formal map:** planned receipt. **Trust
boundary:** currently open. **Step ledger:** FND-1 inventories, FND-2 compares policy. **Boundary:**
`[H1, M4, R3]`.

## M0696-N-SEED

**Claim:** `not Derives Gamma phi` implies consistency of `insert (Neg phi) Gamma`. **Role:** turns
the root failure into input for maximal extension. **Inputs:** `M0696-L-DEDUCTION`. **Proof route:**
a contradiction from the enlarged set transports by deduction to a derivation of `not not phi`,
then DNE and modus ponens contradict nondrivability. **Branch logic:** no hidden case split.
**Formal map:** `SeedConsistencyTarget`. **Trust boundary:** signature only. **Step ledger:** SEED-1
assume falsum; SEED-2 apply deduction; SEED-3 combine DNE; SEED-4 contradict. **Boundary:**
`[H1, M4, R3]`.

## M0696-L-DEDUCTION

**Claim:** Derivation from an inserted premise is equivalent to derivation of an implication.
**Role:** central syntactic engine for the seed. **Inputs:** induction over `Derives`. **Proof
route:** forward direction handles assumption, K, S, DNE, and MP constructors; reverse direction is
assumption plus MP. **Branch logic:** all five derivation constructors must be covered. **Formal
map:** `DeductionTheoremTarget`. **Trust boundary:** no body yet. **Step ledger:** DED-1 reverse;
DED-2 assumption split; DED-3 axioms; DED-4 MP via S; DED-5 recompose. **Boundary:**
`[H1, M4, R3]`.

## M0696-C-MAXIMAL

**Claim:** Every consistent theory extends to a deductively closed, syntactically complete,
consistent theory for arbitrary atom types. **Role:** constructs the canonical-model carrier.
**Inputs:** `M0696-L-CHAIN`. **Proof route:** a maximality construction such as Zorn, followed by
closure and decision lemmas. **Branch logic:** for each formula, failure of both alternatives must
contradict maximality. **Formal map:** `LindenbaumTarget`. **Trust boundary:** choice use must be
reported; enumeration requiring `Encodable Atom` is forbidden. **Step ledger:** MAX-1 order
extensions; MAX-2 chain bound; MAX-3 maximal element; MAX-4 closure; MAX-5 completeness.
**Boundary:** `[H1, M4, R3]`.

## M0696-L-CHAIN

**Claim:** A chain union of consistent theories remains consistent. **Role:** discharges the
maximal-extension limit condition. **Inputs:** finitary structure of `Derives`. **Proof route:** a
falsum derivation uses finitely many assumptions; a chain member contains all of them, contradicting
its consistency. **Branch logic:** induction over the finite derivation tree. **Formal map:** planned
exact signature. **Trust boundary:** no hidden compactness theorem may be invoked. **Step ledger:**
CHAIN-1 extract finite support; CHAIN-2 choose a chain upper member; CHAIN-3 replay; CHAIN-4
contradict. **Boundary:** `[H1, M4, R3]`.

## M0696-C-VALUATION

**Claim:** A maximal theory determines a Boolean valuation on atoms. **Role:** supplies the model
used by the truth lemma. **Inputs:** `Derives Delta (.atom a)`. **Proof route:** classical
decidability selects true exactly in that case. **Branch logic:** derivable versus not derivable.
**Formal map:** `canonicalValuation`. **Trust boundary:** the definition elaborates with classical
choice; it proves no truth property. **Step ledger:** VAL-1 decide derivability; VAL-2 return the
Boolean. **Boundary:** `[H1, M3, R3]`.

## M0696-B-TRUTH

**Claim:** Evaluation by the canonical valuation is true exactly for members of a maximal theory.
**Role:** connects syntax to semantics. **Inputs:** `M0696-C-VALUATION`, `M0696-L-IMP`, and the
encoding. **Proof route:** induction on formulas. **Branch logic:** atom follows by definition;
falsum follows by consistency; implication uses the membership lemma. **Formal map:**
`TruthLemmaTarget`. **Trust boundary:** no body yet. **Step ledger:** TRUTH-1 atom; TRUTH-2 falsum;
TRUTH-3 implication; TRUTH-4 induction recomposition. **Boundary:** `[H1, M4, R3]`.

## M0696-L-IMP

**Claim:** Membership of `phi -> psi` in a maximal theory agrees with Boolean implication of the
membership facts for `phi` and `psi`. **Role:** hard induction case of the truth lemma. **Inputs:**
deductive closure, syntactic completeness, K/S/DNE/MP. **Proof route:** derive the forward direction
by MP and the reverse by completeness and contradiction. **Branch logic:** `phi` absent or present;
when present, `psi` absent or present. **Formal map:** planned exact signature. **Trust boundary:**
no body yet. **Step ledger:** IMP-1 split `phi`; IMP-2 false antecedent; IMP-3 split `psi`; IMP-4
MP contradiction; IMP-5 recompose. **Boundary:** `[H1, M4, R3]`.

## M0696-T-COUNTERMODEL

**Claim:** Nonderivability yields a valuation satisfying every member of `Gamma` and falsifying
`phi`. **Role:** first open root cut set. **Inputs:** seed consistency, maximal extension, truth
lemma. **Proof route:** extend `insert (Neg phi) Gamma`, use its canonical valuation, apply truth to
the included premises and to `Neg phi`. **Branch logic:** none beyond the supplied construction.
**Formal map:** `CountermodelTarget`. **Trust boundary:** signature only. **Step ledger:** CM-1 seed;
CM-2 extend; CM-3 define valuation; CM-4 satisfy Gamma; CM-5 falsify phi. **Boundary:**
`[H1, M4, R3]`.

## M0696-T-ASSEMBLE

**Claim:** The exact countermodel package implies the exact root. **Role:** checked terminal
composition. **Inputs:** `CountermodelTarget`. **Proof route:** assume semantic entailment and
nonderivability, obtain a satisfying falsifying valuation, and contradict entailment. **Branch
logic:** classical `by_contra`. **Formal map:** `completeness_of_countermodel`. **Trust boundary:**
Lean reports `propext`, `Classical.choice`, and `Quot.sound`; this is interface evidence, not a root
receipt. **Step ledger:** ASM-1 introduce; ASM-2 contradict; ASM-3 obtain model; ASM-4 apply semantic
hypothesis; ASM-5 close. **Boundary:** `[H1, M3, R3]`; the child premise is open.

## M0696-X-SOURCE

**Claim:** Primary sources eventually map every material route node. **Role:** human-source gate.
**Inputs:** Post plus a modern source for arbitrary-context completeness. **Proof route:** source
audit, not a proof premise. **Branch logic:** historical tautology form versus modern consequence
form. **Formal map:** not applicable. **Trust boundary:** pinpoint review is open. **Step ledger:**
SRC-1 pin; SRC-2 map assumptions; SRC-3 map nodes; SRC-4 audit errata. **Boundary:**
`[H1, M4, R3]`.

## M0696-X-EXTERNAL

**Claim:** Foundation's theorem is a nearby empty-context endpoint only. **Role:** provenance
boundary. **Inputs:** anchor audit `M0696-C02`. **Proof route:** no proof edge. **Branch logic:** all
recorded mismatches remain blockers. **Formal map:** external `provable_of_tautology`. **Trust
boundary:** absent toolchain and dependency closure. **Step ledger:** EXT-1 identify; EXT-2 compare;
EXT-3 exclude credit. **Boundary:** `[H1, M3, R3]`.

## M0696-X-PROVENANCE

**Claim:** Every credited body and dependency is classified. **Role:** evidence and documentation
overlay. **Inputs:** eventual Lean declarations and receipts. **Proof route:** dependency, axiom,
placeholder, and origin audit. **Branch logic:** local, pinned library, or external body.
**Formal map:** planned receipt bundle. **Trust boundary:** open. **Step ledger:** PROV-1 locate body;
PROV-2 close dependencies; PROV-3 scan trust; PROV-4 bind receipt. **Boundary:**
`[H1, M4, R3]`.

## M0696-X-COMPUTATION

**Claim:** The selected architecture needs no solver, reflection, oracle, or finite computation.
**Role:** explicit mandatory-layer assessment. **Inputs:** current graph. **Proof route:** independent
review of absence. **Branch logic:** any later computational dependency creates a new registry
version. **Formal map:** not applicable pending review. **Trust boundary:** exclusion is provisional.
**Step ledger:** COMP-1 inspect graph; COMP-2 record absence. **Boundary:** `[H1, M4, R3]`.

## Closure boundary

All 17 obligations belong to the frozen inventory. The first open proof cut set is
`M0696-T-COUNTERMODEL`. The composition above is checked, but its premise is not supplied. No node
is credited `M0`, no readable node is independently accepted `R0`, the root remains
`[H1, M3, R3]`, and `theorem_complete` is false.
