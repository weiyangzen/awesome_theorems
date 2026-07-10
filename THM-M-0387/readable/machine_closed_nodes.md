# Machine-closed nodes: readable reconstruction

## Scope and ten-part format

This file reconstructs the public machine-closed families in the rev-5.6 tree.
It does not turn internal proof prose into new theorems. A canonical ID is
machine-closed only when its exact declaration or exact package target is
kernel checked; internal source hooks are mapped as evidence for an upstream
proof body and must not be mistaken for repo-local theorem bodies.

Every entry has the required ten parts: exact target; hypotheses/interfaces;
proof idea; formal map; trust boundary; axiom report; `H/M/R` vector;
independent ledger of at most 100 logical steps; composition rule; remaining
debt/boundary. The shared audited axiom output for the public FLT wrappers and
upstream endpoints is `[propext, Classical.choice, Quot.sound]`, except the
generic semiring monotonicity declaration, whose report is `[propext]`.
`sorryAx` and custom axioms were not found in the local, pinned mathlib, or
pinned `flt-regular` proof sources covered here.

Pins used by every entry:

- Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`;
- mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`;
- `leanprover-community/flt-regular`
  `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`;
- local modules live below
  `Formalizations/Lean/AwesomeTheorems/NumberTheory/THM_M_0387/`.

## Statement and foundation APIs

### M0387-S-S01 and M0387-S-S02: exact fixed-exponent definitions

1. **Exact target.** `M0387-S-S01` is
   `FermatLastTheoremWith R n := ∀ a b c : R, a ≠ 0 -> b ≠ 0 -> c ≠ 0 ->
   a^n+b^n ≠ c^n` for a semiring `R`; `M0387-S-S02` is
   `FermatLastTheoremFor n := FermatLastTheoremWith ℕ n`.
2. **Hypotheses/interfaces.** `[Semiring R]`, natural exponent `n`; no theorem
   hypothesis is hidden in either definition.
3. **Proof idea.** These are statement objects, not proof bodies.
4. **Formal map.** Pinned mathlib
   `Mathlib.NumberTheory.FLT.Basic`, declarations `FermatLastTheoremWith` and
   `FermatLastTheoremFor`.
5. **Trust boundary.** Pinned mathlib supplies the exact definitions, but this
   dossier has no repo-local same-name wrapper/theorem evidence for either
   definition; both nodes are source-interface overlays, not machine-closure
   claims.
6. **Axiom report.** Definitions introduce no proof axiom; downstream checked
   endpoints report only the accepted baseline.
7. **H/M/R vector.** Each is `[H1, M3, R0]`; `H1` records incomplete
   primary-source genealogy for the selected formal presentation, while `M3`
   records the located statement interfaces without a node-scoped local
   wrapper and exact axiom probe.
8. **Independent ledgers.** S01 (3 steps): quantify over three elements; assume
   each nonzero; assert inequality. S02 (2 steps): select `R=ℕ`; unfold S01.
9. **Composition rule.** S01 specialized at `ℕ` is S02; S02 is the codomain
   of all fixed-exponent wrappers below.
10. **Remaining debt/boundary.** A definition being kernel accepted does not
    prove any exponent and does not prove the full root.

### M0387-S-S03: root alias and exact quantifier boundary

1. **Exact target.** The local theorem
   `fermatLastTheoremRootStatement_iff :
   fermatLastTheoremRootStatement ↔ FermatLastTheorem`, where mathlib defines
   `FermatLastTheorem := ∀ n ≥ 3, FermatLastTheoremFor n`.
2. **Hypotheses/interfaces.** None.
3. **Proof idea.** The local alias unfolds definitionally to the selected
   mathlib proposition, so the equivalence is reflexivity.
4. **Formal map.** Local `StatementAndReductionPath.lean`; proof is `Iff.rfl`.
5. **Trust boundary.** Repo-local proof body, `M0-L`, checked by Lean's kernel.
6. **Axiom report.** No additional axioms for this definitional equality.
7. **H/M/R vector.** `[H1, M0-L, R0]` for the alias theorem only.
8. **Independent ledger (3 steps).** (1) unfold the local alias; (2) observe
   both sides are the same proposition; (3) apply reflexivity.
9. **Composition rule.** Fixes the exact target used by `R05` and the root gate.
10. **Remaining debt/boundary.** This proves statement identity, not an
    inhabitant of either proposition. `M0387-ROOT` remains `M2`.

### M0387-S-S04.1 and M0387-S-S04.2: integer and rational transports

1. **Exact target.** Local theorems, for every `n`:
   `fermatLastTheoremFor_iff_integer : FermatLastTheoremFor n ↔
   FermatLastTheoremWith ℤ n` and `fermatLastTheoremFor_iff_rational :
   FermatLastTheoremFor n ↔ FermatLastTheoremWith ℚ n`.
2. **Hypotheses/interfaces.** Natural exponent `n`; mathlib's simultaneous
   `ℕ/ℤ/ℚ` equivalence.
3. **Proof idea.** Integer signs are normalized using parity/oddness cases;
   rational solutions are denominator-cleared; conversely naturals embed into
   either domain.
4. **Formal map.** Local wrappers around
   `fermatLastTheoremFor_iff_int`, `fermatLastTheoremFor_iff_rat`, and upstream
   `fermatLastTheoremWith_nat_int_rat_tfae` in `Basic.lean`.
5. **Trust boundary.** Local exact wrappers have small repo-local terms
   (`M0-L`); mathematical proof bodies live in pinned mathlib.
6. **Axiom report.** Accepted baseline only:
   `[propext, Classical.choice, Quot.sound]`.
7. **H/M/R vector.** Each `[H1, M0-L, R0]`.
8. **Independent ledgers.** Integer (5 steps): map a putative integer solution
   to absolute values/sign cases; use parity of `n`; reduce to naturals; embed
   naturals for the converse; assemble `↔`. Rational (5 steps): extract
   numerators/positive denominators; multiply by the common denominator power;
   obtain an integer solution; use the integer/natural equivalence; embed
   naturals for the converse.
9. **Composition rule.** Either equivalence transports a fixed-exponent result
   in both directions; `flt4IntPath` uses the integer forward direction.
10. **Remaining debt/boundary.** These equivalences preserve a proof already
    supplied; they do not generate the missing all-prime family.

### M0387-S-S05: primitive/coprime equivalence

1. **Exact target.** `fermatLastTheoremFor_iff_coprime :
   FermatLastTheoremFor n ↔ FermatLastTheoremForCoprime n`, where the latter
   restricts to triples with finite-set gcd `1`.
2. **Hypotheses/interfaces.** Natural exponent `n`, normalized gcd in `ℕ`.
3. **Proof idea.** The forward direction forgets the gcd hypothesis. For the
   reverse direction, divide a putative triple by its common gcd and cancel its
   `n`-th power.
4. **Formal map.** Local proof in `StatementAndReductionPath.lean`; reverse
   direction invokes pinned mathlib
   `fermatLastTheoremWith_of_fermatLastTheoremWith_coprime`.
5. **Trust boundary.** Exact equivalence is a repo-local checked theorem
   (`M0-L`); gcd reduction proof body is pinned mathlib.
6. **Axiom report.** Accepted baseline only.
7. **H/M/R vector.** `[H1, M0-L, R0]`.
8. **Independent ledger (6 steps).** (1) assume unrestricted FLT and a
   primitive triple; (2) apply it directly; (3) assume primitive FLT; (4) take
   an unrestricted triple; (5) divide by the finite-set gcd and cancel its
   power; (6) apply the primitive hypothesis.
9. **Composition rule.** Provides the exact statement bridge used in
   normalization work such as `W01.1`.
10. **Remaining debt/boundary.** The theorem is an equivalence, not a proof of
    either side for arbitrary `n`.

### M0387-S-S06: axiom-policy certificate

1. **Exact target.** Public validation certificate that every claimed `M0-*`
   endpoint has a reported allowed axiom set and no disallowed placeholder in
   the covered source closure.
2. **Hypotheses/interfaces.** Pinned revisions, terminal `#print axioms`, and
   placeholder/custom-axiom scans.
3. **Proof idea.** Enumerate endpoints, query their transitive axiom reports,
   and scan the local/pinned proof sources rather than inferring trust from
   filenames.
4. **Formal map.** Stable evidence is recorded in `machine_checked_audit.md`
   and `build_validation.md`; the policy is not a theorem that proves FLT.
5. **Trust boundary.** Lean kernel, compiler/toolchain, source pins, and the
   audit script are explicit trust nodes.
6. **Axiom report.** Allowed: `propext`, `Classical.choice`, `Quot.sound` as
   actually reported. Disallowed: `sorryAx`, `admit`, and custom proposition-
   producing axioms.
7. **H/M/R vector.** `[H1, M3, R0]` for this governance evidence overlay. It
   aggregates machine evidence but is not itself a Lean proposition with a
   repo-local proof body.
8. **Independent ledger (5 steps).** (1) freeze revisions; (2) enumerate exact
   endpoints; (3) print types and axioms; (4) scan proof sources for
   placeholders/custom axioms; (5) reject any endpoint outside policy.
9. **Composition rule.** Required evidence overlay for every `M0-*` row.
10. **Remaining debt/boundary.** An audit certificate validates only the
    declarations queried; it is not a proof of the exact FLT root.

## Reduction and boundary APIs

### M0387-R-R01: exponents one and two are outside the root

1. **Exact target.** Local theorems `notFltExponentOnePath :
   ¬ FermatLastTheoremFor 1` and `notFltExponentTwoPath :
   ¬ FermatLastTheoremFor 2`.
2. **Hypotheses/interfaces.** None; explicit natural counterexamples.
3. **Proof idea.** `1+1=2` refutes exponent one and `3²+4²=5²` refutes
   exponent two.
4. **Formal map.** Local wrappers around mathlib
   `not_fermatLastTheoremFor_one` and `not_fermatLastTheoremFor_two`.
5. **Trust boundary.** Repo-local exact terms, upstream computation proof in
   pinned mathlib.
6. **Axiom report.** Accepted baseline only; these computations do not require
   a disallowed axiom.
7. **H/M/R vector.** `[H1, M0-L, R0]` for each boundary result. The elementary
   counterexamples are explicit, but the manifest conservatively retains
   human-source reconstruction debt until its E4 crosswalk gate is audited.
8. **Independent ledgers.** Exponent one (3 steps): instantiate `(1,1,2)`;
   check nonzero; calculate equality. Exponent two (3 steps): instantiate
   `(3,4,5)`; check nonzero; calculate equality.
9. **Composition rule.** Explains why the root begins at `n ≥ 3`; no result is
   needed to prove a root case.
10. **Remaining debt/boundary.** These are negations of nearby statements, not
    FLT branches.

### M0387-R-R02: exponent-divisibility monotonicity

1. **Exact target.** `fltOfDivisorPath {m n} : m ∣ n ->
   FermatLastTheoremFor m -> FermatLastTheoremFor n`.
2. **Hypotheses/interfaces.** A divisor witness `n=m*k` and fixed-exponent FLT
   at `m`.
3. **Proof idea.** Rewrite `a^n` as `(a^k)^m`; a solution at exponent `n`
   would be a solution at exponent `m`.
4. **Formal map.** Local theorem in `StatementAndReductionPath.lean`, invoking
   `FermatLastTheoremFor.mono`; generic proof in mathlib `Basic.lean`.
5. **Trust boundary.** Exact local wrapper is `M0-L`; upstream generic body is
   pinned mathlib.
6. **Axiom report.** Generic semiring declaration reports `[propext]`; local
   endpoint stays within the accepted baseline.
7. **H/M/R vector.** `[H1, M0-L, R0]`; the machine proof is exact, while the
   independent primary human-source crosswalk remains unaudited.
8. **Independent ledger (5 steps).** (1) write `n=m*k`; (2) assume nonzero
   `a,b,c`; (3) rewrite all `n`-th powers as `m`-th powers of `k`-th powers;
   (4) prove the powered bases remain nonzero; (5) apply FLT at `m`.
9. **Composition rule.** Drives `R05`, `flt8ViaFlt4Path`, and the composite
   cases in `fltSmallExponentsPath`.
10. **Remaining debt/boundary.** Monotonicity cannot prove an exponent unless
    a divisor exponent is already closed.

### M0387-R-R05: exact conditional root assembly

1. **Exact target.** `fermatLastTheoremRootOfOddPrimesPath :
   OddPrimeExponentClosure -> fermatLastTheoremRootStatement`.
2. **Hypotheses/interfaces.** Exact premise
   `∀ p, Nat.Prime p -> Odd p -> FermatLastTheoremFor p`; checked exponent
   four is internal to mathlib's assembly theorem.
3. **Proof idea.** For `n ≥ 3`, either `4 ∣ n` or some odd prime `p ∣ n`;
   apply exponent four or the premise, then monotonicity.
4. **Formal map.** Local theorem in `StatementAndReductionPath.lean` calling
   pinned `FermatLastTheorem.of_odd_primes` from
   `Mathlib.NumberTheory.FLT.Four`.
5. **Trust boundary.** Exact conditional wrapper is repo-local (`M0-L`);
   assembly proof body is pinned mathlib.
6. **Axiom report.** `[propext, Classical.choice, Quot.sound]`.
7. **H/M/R vector.** `[H1, M0-L, R0]` for the implication, not the root; the
   independent primary human-source crosswalk remains open.
8. **Independent ledger (5 steps).** (1) assume the odd-prime family; (2) fix
   `n ≥ 3`; (3) obtain `4|n` or odd prime `p|n`; (4) apply exponent four or
   the premise; (5) transport along divisibility.
9. **Composition rule.** `R04 + B4 -> ROOT` is checked as an implication.
10. **Remaining debt/boundary.** `R04` is not inhabited. Therefore this exact
    theorem cannot authorize `M0-*` for `M0387-ROOT`.

## Exponent-three branch

### M0387-B3 and M0387-B3-B3.5

1. **Exact target.** Mathlib `fermatLastTheoremThree :
   FermatLastTheoremFor 3` and local `flt3Path` of the same exact type.
2. **Hypotheses/interfaces.** None beyond the fixed natural-domain statement.
3. **Proof idea.** Mathlib reduces to a generalized cubic equation, packages
   a normalized solution in Eisenstein integers, chooses a solution of minimal
   `λ`-multiplicity, constructs one with strictly lower multiplicity, and
   contradicts minimality.
4. **Formal map.** Proof body:
   `Mathlib.NumberTheory.FLT.Three` at the pinned mathlib revision, terminal
   declaration at source line 750; local wrapper in `FLT3Path.lean`.
5. **Trust boundary.** `M0-W`: the exact theorem is checked locally through
   pinned mathlib; its body is not repo-local.
6. **Axiom report.** `[propext, Classical.choice, Quot.sound]`; no `sorryAx`.
7. **H/M/R vector.** `[H1, M0-W, R0]` for `M0387-B3` and
   `M0387-B3-B3.5`. The internal B3 source-map nodes below are
   `[H1, M3, R0]` because the terminal wrapper is not evidence for their
   different exact targets.
8. **Independent ledger (8 steps).** (1) reduce to a primitive integer triple;
   (2) close the mod-9 Case-I boundary; (3) reduce the remaining case to
   `FermatLastTheoremForThreeGen`; (4) build `Solution'`; (5) normalize it to
   `Solution`; (6) select a minimal multiplicity solution; (7) construct a
   strictly smaller solution; (8) contradict minimality.
9. **Composition rule.** Supplies the `p=3` input of the planned `W08` and the
   exponent-three cases of `SMALL.5`.
10. **Remaining debt/boundary.** It proves only exponent `3`. Internal source
    hooks below explain the imported body; they do not become repo-local bodies.

#### Exponent-three internal source map

1. **Exact target.** Map B3 IDs to actual pinned hooks: `B3.1.1`
   `cube_of_not_dvd`; `B3.1.2` `fermatLastTheoremThree_case_1`; `B3.2`
   `FermatLastTheoremForThreeGen` and its reduction; `B3.3.1` `Solution'`;
   `B3.3.2` `exists_Solution_of_Solution'`; `B3.4.1` multiplicity/finiteness;
   `B3.4.2` `Solution.exists_minimal`; `B3.4.3` `Solution'_descent`;
   `B3.4.4` `exists_Solution_multiplicity_lt`.
2. **Hypotheses/interfaces.** Eisenstein-integer primitive root and the fields
   carried by `Solution'`/`Solution`.
3. **Proof idea.** Congruence controls the entry case; multiplicity supplies a
   well-founded descent measure.
4. **Formal map.** All hooks are in pinned
   `Mathlib.NumberTheory.FLT.Three`; `eligibles/` prose provides the longer
   reader ledger.
5. **Trust boundary.** Upstream mathlib body; no source hook is claimed as a
   newly proved local theorem.
6. **Axiom report.** Covered by the terminal endpoint's accepted report.
7. **H/M/R vector.** Source-map entries inherit readable `R0`; exact machine
   labels are `[H1, M3, R0]` in the manifest: each has a located source
   interface, but no exact repo-local wrapper/type/axiom packet. The terminal
   `flt3Path` must not substitute for these narrower targets.
8. **Independent ledger references.** B3.1 (mod-9 residues and Case I), B3.2
   (generalized equation), B3.3 (solution normalization), and B3.4 (finite
   multiplicity, minimal choice, explicit descent, strict decrease) each have
   separate ledgers in `machine_checked_audit.md` and `full_study.md`; no
   individual ledger exceeds 100 steps.
9. **Composition rule.** B3.1--B3.4 are the actual imported dependency route
   into `fermatLastTheoremThree`, then `flt3Path`.
10. **Remaining debt/boundary.** These hooks do not prove arbitrary odd-prime
    exponents and do not relocate the mathlib body into this repository.

## Exponent-four branch and derivatives

### M0387-B4: exponent-four terminal

1. **Exact target.** Mathlib `fermatLastTheoremFour :
   FermatLastTheoremFor 4` and local `flt4Path` of the same type.
2. **Hypotheses/interfaces.** None beyond the fixed natural statement.
3. **Proof idea.** Reduce to `a⁴+b⁴=c²`; take a positive odd minimal
   primitive solution; classify two primitive Pythagorean triples; extract
   squares using coprimality; build a smaller solution; contradict minimality.
4. **Formal map.** Proof body in pinned
   `Mathlib.NumberTheory.FLT.Four`, terminal at source line 266; local wrapper
   in `FLT4Path.lean`.
5. **Trust boundary.** `M0-W`: checked wrapper around pinned mathlib; body is
   not repo-local.
6. **Axiom report.** `[propext, Classical.choice, Quot.sound]`; no `sorryAx`.
7. **H/M/R vector.** `[H1, M0-W, R0]` for `M0387-B4`. Internal package nodes
   use their own exact declarations and manifest vectors; the terminal cannot
   close a differently stated package.
8. **Independent ledger (9 steps).** (1) transport to integers; (2) bridge to
   `Fermat42`; (3) choose a minimal solution; (4) normalize parity/sign; (5)
   classify the first primitive triple; (6) classify the second; (7) prove
   coprimality and extract squares; (8) construct a strictly smaller solution;
   (9) contradict minimality and transport back.
9. **Composition rule.** Supplies the `4|n` branch inside `R05` and all
   divisible-by-four derivatives.
10. **Remaining debt/boundary.** Exponent four does not cover odd primes.

### M0387-B4-B4.8: bridge terminal

1. **Exact target.** `flt4BridgeTerminalPath {a b c : ℤ} (ha : a ≠ 0)
   (hb : b ≠ 0) : a ^ 4 + b ^ 4 ≠ c ^ 2`.
2. **Hypotheses/interfaces.** Nonzero integer bases `a` and `b`; no nonzero
   premise on `c` is needed.
3. **Proof idea.** Package the terminal infinite-descent contradiction for
   the bridge equation `a^4+b^4=c^2`.
4. **Formal map.** Local exact wrapper in `InternalCoveragePath.lean` around
   mathlib `not_fermat_42`, whose proof is in
   `Mathlib.NumberTheory.FLT.Four.lean`.
5. **Trust boundary.** `M0-W`: exact local wrapper, pinned mathlib proof body,
   no vendored copy.
6. **Axiom report.** `[propext, Classical.choice, Quot.sound]`.
7. **H/M/R vector.** `[H1, M0-W, R0]`.
8. **Independent ledger (4 steps).** (1) fix nonzero `a,b`; (2) suppose the
   bridge equality; (3) invoke the checked no-minimal-solution descent; (4)
   derive contradiction.
9. **Composition rule.** This bridge terminal is the key integer result used
   by mathlib to obtain `fermatLastTheoremFour`, then `flt4Path`.
10. **Remaining debt/boundary.** It excludes the bridge equation, not every
    exponent and not the exact FLT root.

#### Exponent-four internal descent source map

1. **Exact target.** Map the canonical packages to real hooks: B4.1
   `Fermat42`/`not_fermat_42`; B4.2 `Fermat42.exists_minimal`,
   `coprime_of_minimal`, `exists_odd_minimal`, `exists_pos_odd_minimal`; B4.3
   first `PythagoreanTriple.coprime_classification'`; B4.4 its second use;
   B4.5 `Int.isCoprime_of_sq_sum` and its primed variant; B4.6 repeated
   `Int.sq_of_gcd_eq_one`; B4.7 `Fermat42.not_minimal`.
2. **Hypotheses/interfaces.** A positive odd minimal `Fermat42` solution and
   primitive Pythagorean triple classification.
3. **Proof idea.** Successive classifications expose coprime products that are
   squares; the extracted roots form a smaller `Fermat42` witness.
4. **Formal map.** `Mathlib.NumberTheory.FLT.Four`,
   `Mathlib.NumberTheory.PythagoreanTriples`, and
   `Mathlib.RingTheory.Int.Basic`, all at the pinned mathlib revision.
5. **Trust boundary.** Imported proof bodies; no package prose is a replacement
   theorem.
6. **Axiom report.** Covered by terminal endpoint's accepted report.
7. **H/M/R vector.** Human status is conservatively `H1` and readability is
   `R0` for each internal package until primary-source statement/assumption
   crosswalks are audited. Machine status is declaration-specific: a node is `M0-W`
   only when the manifest carries an exact `InternalCoveragePath` wrapper for
   that package target; every other source-map package remains `M3`.
8. **Independent ledger references.** Existing
   `eligibles/n4_proof_process.md` has independent subledgers for bridge (10),
   minimal normalization (16), first classification (17), second
   classification (16), coprimality (13), square extraction (25), and smaller
   solution/strict comparison (18); all are below 100.
9. **Composition rule.** B4.1--B4.7 feed `not_fermat_42`, which feeds
   `fermatLastTheoremFour`, which feeds `flt4Path`.
10. **Remaining debt/boundary.** The proof body remains in mathlib, and these
    source packages do not prove the exact FLT root.

#### Exact internal endpoint vectors

The source map above contains both exact checked endpoints and readable-only
overlays. The rev-5.6 declaration-level split is:

- `M0387-B4-B4.2 = [H1, M0-W, R0]`, checked as
  `flt4PositiveOddMinimalPath`; it closes exactly positive odd minimal
  normalization.
- `M0387-B4-B4.5 = [H1, M0-W, R0]`, checked as
  `flt4CoprimeSquareSumSymmPath`; it closes exactly the product-coprimality
  bridge.
- `M0387-B4-B4.7 = [H1, M0-W, R0]`, checked as
  `flt4NoMinimalPath`; it closes exactly the no-positive-odd-minimal endpoint.
- `M0387-B4-B4.1`, `B4.3`, `B4.4`, and `B4.6` remain
  `[H1, M3, R0]`: their source hooks and ledgers are mapped, but no exact
  node-scoped local wrapper/type/axiom packet is recorded.

All three checked wrappers live in `InternalCoveragePath.lean`, retain their
proof bodies in pinned `Mathlib.NumberTheory.FLT.Four`, and report only the
accepted axiom baseline. None closes the full FLT root.

### M0387-B4-B4.9: integer transport and divisible exponent derivative

1. **Exact target.** Local `flt4IntPath : FermatLastTheoremWith ℤ 4` and
   `flt8ViaFlt4Path : FermatLastTheoremFor 8`.
2. **Hypotheses/interfaces.** `flt4Path`, integer equivalence, monotonicity,
   and the decidable witness `4 ∣ 8`.
3. **Proof idea.** Transport exponent four into integers; separately lift the
   exponent-four theorem along divisibility to exponent eight.
4. **Formal map.** Repo-local proof bodies in `FLT4Path.lean`; upstream
   interfaces `fermatLastTheoremFor_iff_int` and
   `FermatLastTheoremFor.mono`.
5. **Trust boundary.** Exact derived wrappers are repo-local terms around
   pinned mathlib (`M0-W` source boundary for their substantive proofs).
6. **Axiom report.** Accepted baseline only.
7. **H/M/R vector.** Each `[H1, M0-W, R0]`.
8. **Independent ledgers.** Integer (2 steps): take `flt4Path`; apply the
   forward equivalence. Exponent eight (3 steps): decide `4|8`; take
   `flt4Path`; apply monotonicity.
9. **Composition rule.** Provides exact public fixed-exponent conclusions;
   generalized divisible exponents use `R02` analogously.
10. **Remaining debt/boundary.** Two derived exponents are not an arbitrary
    exponent proof.

## Small exponents from the pinned external project

### M0387-SMALL-SMALL.1, M0387-SMALL-SMALL.2, M0387-SMALL-SMALL.3, and M0387-SMALL-SMALL.4

1. **Exact target.** Local exact wrappers `flt5Path`, `flt7Path`, `flt11Path`,
   and `flt13Path`, respectively proving `FermatLastTheoremFor 5`, `7`, `11`,
   and `13`.
2. **Hypotheses/interfaces.** None beyond each fixed natural exponent.
3. **Proof idea.** Each local theorem directly exposes the corresponding
   pinned `flt-regular` small-number terminal theorem.
4. **Formal map.** Local `SmallExponentsPath.lean`; upstream
   `fermatLastTheoremFive`, `fermatLastTheoremSeven`,
   `fermatLastTheoremEleven`, and `fermatLastTheoremThirteen` under
   `FltRegular/SmallNumbers/`.
5. **Trust boundary.** `M0-P`: exact theorem bodies live in the pinned external
   dependency and are checked through local wrappers; they are not vendored.
6. **Axiom report.** `[propext, Classical.choice, Quot.sound]`; placeholder
   scan passed in the pinned closure.
7. **H/M/R vector.** Each `[H1, M0-P, R0]`; exact primary human-source mapping
   for each upstream small-number formal route remains incomplete.
8. **Independent ledgers.** For each exponent: (1) import the exact upstream
   theorem; (2) compare its normalized type with the fixed-exponent target;
   (3) expose it through the local wrapper. The substantive upstream proof is
   a separate source boundary, not counted as these three wrapper steps.
9. **Composition rule.** Feed the prime rows of `SMALL.5`; by monotonicity they
   also cover `10,14,15` as appropriate.
10. **Remaining debt/boundary.** Four primes do not establish every odd prime.

### M0387-SMALL and M0387-SMALL-SMALL.5: interval 3 through 16

1. **Exact target.** `fltSmallExponentsPath {n} (hn : n ∈ Finset.Icc 3 16) :
   FermatLastTheoremFor n`.
2. **Hypotheses/interfaces.** A finite interval membership proof; terminal
   theorems at `3,4,5,7,11,13`; exponent monotonicity.
3. **Proof idea.** Finite-case split. Prime/base exponents use their terminal
   theorems; `6,8,9,10,12,14,15,16` lift from divisors `3,4,5,7`.
4. **Formal map.** Local wrapper in `SmallExponentsPath.lean`; upstream
   `FLT_small` in `FltRegular/SmallNumbers/SmallNumbers.lean`.
5. **Trust boundary.** `M0-P`: upstream proof in pinned `flt-regular`, checked
   through a local exact wrapper.
6. **Axiom report.** Accepted baseline only; no placeholder in covered source.
7. **H/M/R vector.** `[H1, M0-P, R0]`.
8. **Independent ledger (8 steps).** (1) split `n=3..16`; (2) use B3 at `3,6,9`;
   (3) use B4 at `4,8,12,16`; (4) use exponent five at `5,10,15`; (5) use
   exponent seven at `7,14`; (6) use exponent eleven; (7) use exponent
   thirteen; (8) apply monotonicity in every composite case.
9. **Composition rule.** Exact finite family assembled from `B3`, `B4`, and
   `SMALL.1--SMALL.4`.
10. **Remaining debt/boundary.** The hypothesis `n ∈ [3,16]` is essential; it
    cannot supply the all-odd-prime family.

## Regular-prime branch

All regular-prime proof bodies below live in the pinned
`leanprover-community/flt-regular` dependency. The exact terminal wrapper is
machine closed locally; internal source packages are reconstructed so readers
can see what is imported, without pretending they were reproved here.

### M0387-RP-RP.1: regularity and class-group setup

1. **Exact target.** Define `IsRegularNumber n` by coprimality of `n` with the
   class number of the `n`-th cyclotomic field, define `IsRegularPrime p`, and
   supply `isPrincipal_of_isPrincipal_pow_of_coprime`.
2. **Hypotheses/interfaces.** Cyclotomic extensions, ring of integers, ideal
   class group, finite class number, and prime/coprime arithmetic.
3. **Proof idea.** If an ideal class raised to the `p`-th power is trivial and
   `p` is coprime to the class-group order, the class itself is trivial, so the
   ideal is principal.
4. **Formal map.** `FltRegular/NumberTheory/RegularPrimes.lean`:
   `IsRegularNumber`, `IsRegularPrime`,
   `isPrincipal_of_isPrincipal_pow_of_coprime`.
5. **Trust boundary.** Pinned external proof body (`M0-P` only where the exact
   declaration target is used); not vendored locally.
6. **Axiom report.** Covered by terminal accepted report; no `sorryAx` found.
7. **H/M/R vector.** `[H1, M3, R0]` for `M0387-RP-RP.1`: the upstream
   definitions/lemma are located, but this node has no exact repo-local
   declaration/type/axiom packet. Primary Kummer-source mapping also remains
   incomplete.
8. **Independent ledger (5 steps).** (1) move the ideal into the finite class
   group; (2) translate principal `I^p` to `p*[I]=0`; (3) use Bezout from
   coprimality with the group order; (4) derive `[I]=0`; (5) translate back to
   principality.
9. **Composition rule.** Supplies principalization in Case I and Case II.
10. **Remaining debt/boundary.** Regularity is a hypothesis and is not true for
    every prime.

### M0387-RP-RP.2: primitive MayAssume reduction

1. **Exact target.** `MayAssume.coprime`: divide an integer solution by the
   gcd of `{a,b,c}`, preserving the equation, gcd-one condition, and
   nonvanishing product. Auxiliary actual hooks include
   `FltRegular.p_dvd_c_of_ab_of_anegc` and `FltRegular.a_not_cong_b`.
2. **Hypotheses/interfaces.** Integer Fermat equation and `a*b*c ≠ 0`.
3. **Proof idea.** Cancel the common gcd power; auxiliary congruence lemmas
   choose a Case-I ordering where `a` is not congruent to `b` modulo `p`.
4. **Formal map.** `FltRegular/MayAssume/Lemmas.lean`. Importantly,
   `p_dvd_c_of_ab_of_anegc` and `a_not_cong_b` are in namespace `FltRegular`,
   not `MayAssume`.
5. **Trust boundary.** Pinned external body; no local reproof.
6. **Axiom report.** Terminal closure reports accepted baseline only.
7. **H/M/R vector.** `[H1, M0-P, R0]`: the exact package target is now
   recorded and probed through local `regularPrimePrimitivePath`. Auxiliary
   divisibility and noncongruence refinements remain source-map obligations;
   locating those hooks alone does not close separate nodes.
8. **Independent ledger (7 steps).** (1) define gcd `d`; (2) prove `d≠0`; (3)
   divide coordinates; (4) cancel `d^p`; (5) prove normalized gcd one; (6)
   preserve nonzero product; (7) use congruence/permutation lemmas to choose the
   Case-I normal form.
9. **Composition rule.** Produces the normalized triple used by `flt_regular`'s
   Case I/II split.
10. **Remaining debt/boundary.** Primitive normalization does not exclude a
    solution by itself.

### M0387-RP-RP.3, M0387-RP-RP.3.1, M0387-RP-RP.3.2, and M0387-RP-RP.3.3: Case I

1. **Exact target.** Upstream `CaseI.Statement` and terminal
   `CaseI.caseI`: under regularity and the Case-I condition
   `¬ p ∣ a*b*c`, exclude the Fermat equation for a primitive normalized
   integer triple.
2. **Hypotheses/interfaces.** Prime `p` (with small-prime cases dispatched),
   `IsRegularPrime p`, Case-I divisibility condition, and cyclotomic field
   ideals/units.
3. **Proof idea.** Factor the Fermat expression into cyclotomic factors; extract
   an ideal `p`-th power; use regularity to principalize; recover an element
   relation whose congruences contradict the normalized Case-I assumptions.
4. **Formal map.** `FltRegular/CaseI/Statement.lean`, exact hooks
   `SlightlyEasier`, `Statement`, `may_assume`, `ab_coprime`, `exists_ideal`,
   `is_principal_aux`, `is_principal`, `ex_fin_div`, `caseI_easier`, `caseI`.
5. **Trust boundary.** Pinned external proof body and cyclotomic/class-group
   mathlib foundations.
6. **Axiom report.** Accepted baseline only at the terminal closure; no
   placeholder found.
7. **H/M/R vector.** `M0387-RP-RP.3 = [H1, M0-P, R0]`, checked through the
   exact local `regularPrimeCaseIPath` wrapper. Its child source-map nodes
   remain `[H1, M3, R0]`; the package terminal is not reused for their
   different targets.
8. **Independent ledger (9 steps).** (1) normalize the triple; (2) prove
   pairwise/cyclotomic factor coprimality; (3) construct the factor ideal; (4)
   prove it is a `p`-th power; (5) invoke regularity; (6) principalize the
   root ideal; (7) choose a generator; (8) derive the finite-index/unit
   relation; (9) obtain the Case-I contradiction.
9. **Composition rule.** `RP.3.1 + RP.3.2 + RP.3.3 -> CaseI.caseI`; the
   terminal joins Case II in `RP.5`.
10. **Remaining debt/boundary.** Case I excludes only the branch where `p` does
    not divide the normalized coordinate product.

#### Case I leaf map

1. **Exact target.** RP.3.1 ideal extraction maps to `ab_coprime` and
   `exists_ideal`; RP.3.2 principalization maps to `is_principal_aux` and
   `is_principal`; RP.3.3 element recovery/close maps to `ex_fin_div`,
   `caseI_easier`, and `caseI`.
2. **Hypotheses/interfaces.** Exact fields of `CaseI.SlightlyEasier` and
   `CaseI.Statement`.
3. **Proof idea.** Separate factorization, class-group, and recovered-element
   contradictions so no high-risk call is hidden.
4. **Formal map.** Pinned Case I source above; longer leaf ledgers live in
   `eligibles/regular_primes_proof_process.md`.
5. **Trust boundary.** External `flt-regular` body, checked via the pin.
6. **Axiom report.** Inherits the accepted terminal report.
7. **H/M/R vector.** `[H1, R0]` readable source mapping; exact `M` status is
   declaration-specific in the manifest.
8. **Independent ledger references.** Ideal extraction (factorization,
   coprimality, `p`-th ideal power); principalization (class-group torsion and
   regularity); element close (generator/unit choice and congruence
   contradiction). Each recorded ledger is below 100 steps.
9. **Composition rule.** The three leaves compose in order into `CaseI.caseI`.
10. **Remaining debt/boundary.** Their proof bodies are not repo-local, and
    their historical source pinpoint remains `H1`.

### M0387-RP-RP.4, M0387-RP-RP.4.1, M0387-RP-RP.4.2, M0387-RP-RP.4.3, M0387-RP-RP.4.4, and M0387-RP-RP.4.5: Case II

1. **Exact target.** Upstream `CaseII.caseII`: under regularity and
   `p ∣ a*b*c`, exclude the primitive integer Fermat equation.
2. **Hypotheses/interfaces.** `IsRegularPrime p`, `p≠2`, normalized gcd one,
   nonzero product, and Case-II divisibility.
3. **Proof idea.** Move the divisible coordinate into a fixed position; in the
   cyclotomic field express factors using `π=ζ-1`; isolate a distinguished
   root/factor; principalize suitable ideal quotients; construct a new solution
   with a strictly smaller positive `π`-multiplicity; contradict infinite
   descent.
4. **Formal map.** `FltRegular/CaseII/Statement.lean` and
   `FltRegular/CaseII/InductionStep.lean`; terminal hooks
   `not_exists_solution`, `not_exists_solution'`,
   `not_exists_Int_solution`, `not_exists_Int_solution'`, `caseII`.
5. **Trust boundary.** Pinned external proof body, including cyclotomic ideal
   arithmetic and well-founded multiplicity.
6. **Axiom report.** Accepted baseline only; no placeholder found.
7. **H/M/R vector.** `M0387-RP-RP.4 = [H1, M0-P, R0]`, checked through the
   exact local `regularPrimeCaseIIPath` wrapper. Its five child source-map
   nodes remain `[H1, M3, R0]` because they lack individual local
   wrapper/type/axiom packets.
8. **Independent ledger (10 steps).** (1) normalize coordinate position; (2)
   translate divisibility to `π`; (3) factor into indexed ideals; (4) separate
   common `π`-part; (5) prove remaining ideals coprime; (6) extract ideal
   `p`-th roots; (7) identify the unique distinguished root; (8) principalize
   quotient ideals; (9) construct the descended solution; (10) lower positive
   multiplicity and contradict induction.
9. **Composition rule.** `RP.4.1--RP.4.5 -> CaseII.caseII`; combines with Case
   I in `RP.5`.
10. **Remaining debt/boundary.** Case II is conditional on regularity and does
    not cover irregular primes.

#### Case II leaf map

1. **Exact target.** RP.4.1 pi-language maps to `zeta_sub_one_dvd`,
   `span_pow_add_pow_eq`, `div_one_sub_zeta_mem`,
   `div_zeta_sub_one_Bijective`; RP.4.2 ideal factors maps to `prod_c`,
   `exists_ideal_pow_eq_c`, `root_div_zeta_sub_one_dvd_gcd_spec`,
   `c_div_principal`; RP.4.3 distinguished root maps to
   `zeta_sub_one_dvd_root`, `zeta_sub_one_dvd_root_spec`, `p_dvd_c_iff`,
   `p_dvd_a_iff`, `p_pow_dvd_c_eta_zero`, `p_pow_dvd_a_eta_zero`; RP.4.4 raw
   descent maps to `exists_solution` and `exists_solution'`; RP.4.5 maps to the
   `not_exists_*` family and `caseII`.
2. **Hypotheses/interfaces.** Exact cyclotomic field/ring-of-integers variables
   and positive multiplicity `m` used by `InductionStep.lean`.
3. **Proof idea.** The five leaves isolate language conversion, ideal
   factorization, unique exceptional factor, descent construction, and
   no-solution induction.
4. **Formal map.** Actual names above replace stale nonexistent names such as
   `find_root`, `find_root'`, bare `irreducible`, and `caseII_statement`.
5. **Trust boundary.** Pinned external body; not a local implementation.
6. **Axiom report.** Covered by the accepted terminal report.
7. **H/M/R vector.** `[H1, R0]` source mapping; exact machine labels follow
   declaration evidence in the manifest.
8. **Independent ledger references.** Existing regular-prime process prose
   supplies separate sub-100 ledgers for pi-language conversion, ideal-factor
   extraction, distinguished-root control, raw descent, and no-solution close.
9. **Composition rule.** RP.4.1 -> RP.4.2 -> RP.4.3 -> RP.4.4 -> RP.4.5.
10. **Remaining debt/boundary.** This is readable reconstruction of a pinned
    upstream body; it is not a repo-local reproof or a result for irregular
    primes.

### M0387-RP and M0387-RP-RP.5: terminal regular-prime wrapper

1. **Exact target.** Upstream and local exact types:
   `∀ {p : ℕ} [Fact p.Prime], IsRegularPrime p -> p ≠ 2 ->
   FermatLastTheoremFor p`; upstream `flt_regular`, local
   `regularPrimesPath`.
2. **Hypotheses/interfaces.** Prime instance, `IsRegularPrime p`, and `p≠2`.
3. **Proof idea.** Transport a hypothetical natural result to integers,
   primitive-normalize it, split on `p ∣ (a/d)(b/d)(c/d)`, and dispatch to
   Case II or Case I.
4. **Formal map.** Upstream `FltRegular/FltRegular.lean:14`; local
   `RegularPrimesPath.lean`. Correct merge dependencies are
   `MayAssume.coprime`, `FltRegular.caseI`, and `FltRegular.caseII`.
5. **Trust boundary.** `M0-P`: external proof body is pinned and checked through
   the local wrapper; not vendored.
6. **Axiom report.** `[propext, Classical.choice, Quot.sound]`; no `sorryAx` or
   custom axiom in the covered closure.
7. **H/M/R vector.** `[H1, M0-P, R0]`; incomplete primary Kummer-source
   crosswalk prevents `H0` here.
8. **Independent ledger (7 steps).** (1) transport to integers; (2) assume a
   solution; (3) normalize by gcd; (4) form the normalized product; (5) split
   on divisibility by `p`; (6) invoke Case II if divisible and Case I otherwise;
   (7) derive contradiction in both branches.
9. **Composition rule.** `RP.1 + RP.2 + RP.3 + RP.4 -> RP.5 -> RP`.
10. **Remaining debt/boundary.** The premise `IsRegularPrime p` leaves every
    irregular prime outside this theorem; hence it cannot inhabit `R04`.

## Trust-boundary nodes

### M0387-X-X.1, M0387-X-X.2, M0387-X-X.3, M0387-X-X.4, and M0387-T-T.1

1. **Exact target.** X.1 records the reproducible Lean kernel/toolchain; X.2
   records accepted axiom reports; X.3 records mathlib proof-body boundaries;
   X.4 records pinned `flt-regular` boundaries; T.1 records the checked special
   branch terminals, canonically represented by exact fixed-exponent wrappers.
2. **Hypotheses/interfaces.** Pins and exact declarations listed at the start
   of this file.
3. **Proof idea.** Make every imported proof-body and trust transition visible
   so a wrapper cannot be reported as a local reproof.
4. **Formal map.** `FLT3Path.lean`, `FLT4Path.lean`,
   `SmallExponentsPath.lean`, `RegularPrimesPath.lean`, their pinned upstream
   modules, and the stable machine audit.
5. **Trust boundary.** X.1/X.2 are governance evidence overlays (`M3`), not
   Lean theorem certificates; X.3 is `M0-W`; X.4 is `M0-P`; T.1 inherits the
   exact terminal source boundary.
6. **Axiom report.** Accepted reports only; the Imperial candidate's
   `knownin1980s` and `sorryAx` are isolated in
   `readable/external_candidate_ledger.md` and never enter this closure.
7. **H/M/R vector.** `X.1` and `X.2` are `[H1, M3, R0]` governance evidence
   overlays, `X.3` is `[H1, M0-W, R0]`, `X.4` is
   `[H1, M0-P, R0]`, and `T.1` is `[H1, M0-W, R0]`. `T.1` is an exact checked
   special-terminal record, not a root theorem.
8. **Independent ledger (5 steps).** (1) identify exact endpoint; (2) locate
   proof body; (3) freeze its revision; (4) check type/axioms/placeholders;
   (5) label local, mathlib, or pinned-external boundary without conflation.
9. **Composition rule.** Every machine-closed branch requires the appropriate
   X node; T.1 summarizes those terminals for later conditional composition.
10. **Remaining debt/boundary.** Trust records do not supply `W02--W07`, the
    all-odd-prime theorem, or an unconditional root declaration.

## Exact root status

The entries above maximize truthful local coverage. They close statement and
transport APIs, exponent boundaries, conditional assembly, `n=3`, `n=4`,
selected small exponents, the whole interval `3..16`, and every regular-prime
exponent. They do not close every odd prime. No exact local kernel-checked
declaration of type `FermatLastTheorem` exists without assuming
`OddPrimeExponentClosure`. Therefore the exact root is still `[H1, M2, R0]`,
not `M0-L`, `M0-W`, or `M0-P`.
