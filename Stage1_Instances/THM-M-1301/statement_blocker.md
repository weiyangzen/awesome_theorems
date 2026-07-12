# Statement-phase blocker

Item: `S56-M-1301-STATEMENT`

Verdict: blocked. No canonical Lean proposition can be elaborated without choosing mathematics that
the repository does not specify.

## First failed gate

The rev-5.6 exact-statement gate fails before Lean elaboration. The catalogue gives only the label
"Bony paraproduct decomposition" and the gloss "paradifferential methods for nonlinear PDE". The
gloss has no domain, ordered binders, hypotheses, or conclusion. It therefore does not determine a
Lean proposition.

The primary discovery source confirms that several non-interchangeable propositions are nearby.
Bony (1981), section 2 contains, among others:

- Theorem 2.1, boundedness and regularization properties of two paramultiplication operators;
- Theorem 2.3, composition of paramultiplication operators modulo a regularizing remainder;
- Theorem 2.5(a), product decompositions in Holder spaces, with different formulas for positive
  and negative regularity;
- Theorem 2.5(b), product decompositions and remainder estimates in Sobolev spaces.

Selecting Theorem 2.5(a), one branch of it, or a modern three-term Besov identity would be a source
selection, not an elaboration of an already identified target. It could also collide with the
separate catalogue item `THM-M-1303` ("paraproduct"). Rev-5.6 forbids silently broadening or
substituting a theorem, so no `.lean` declaration was manufactured.

## Lean availability boundary

The pinned mathlib tree contains tempered distributions and Fourier transforms, but the scoped
search found no declaration or module named for Bony or paraproducts. The nearby repository file
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_182.lean` only places paraproduct continuity in an
abstract proposition field; it does not define the operators or state this target. Consequently it
cannot supply an exact statement or receive statement identity credit.

Because the mathematical proposition is not frozen, there is no truthful minimal import, canonical
Lean expression, elaborated-expression hash, mutation suite, or environment fingerprint to record.
The machine debt remains `M4`; theorem completion remains false.

## Retry condition

The master/source-audit lane must resolve the catalogue collision and approve one pinpointed source
result, including the domain, cutoff convention, input spaces, compact-support requirements,
regularity ranges, remainder topology and estimate, and every integer-regularity convention. After
that decision, this node can define the missing analytic objects (or identify pinned definitions),
elaborate the exact expression, and run the four required mutation classes.

## Validation evidence

Base revision: `ec658bada2ff8177de66f000a68d04a9310f8880`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard and 1546-target projection consistent |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, uniform L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1301` | 0 | rank 469, planned, theorem incomplete |
| `rg -n -i 'paraproduct|Littlewood.Paley|LittlewoodPaley|dyadic.*decom' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching pinned mathlib source declaration/module |

The `rg` exit code is recorded as scoped negative discovery evidence, not kernel evidence. No Lean
command is claimed because there is no exact target to elaborate. No worker self-test manifest is
emitted for this blocked phase.
