# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| A number field has a maximal unramified abelian extension | D. Hilbert, *Die Theorie der algebraischen Zahlkorper*, Jahresbericht der DMV 4 (1897), the historical Zahlbericht; modern theorem location still requires edition/page verification | `AwesomeTheorems.Stage1.S1_M_075.HilbertClassFieldExists` | Historical primary-source family identified, but no accepted edition/page/assumption/errata mapping: `H1` |
| Finite-prime unramifiedness | J. Neukirch, *Algebraic Number Theory*, Chapter VI (global class field theory); exact theorem/page depends on edition and remains to be pinned | `IsEverywhereUnramifiedAtFinitePrimes K H` | The legacy predicate quantifies over prime ideals of the ring of integers; exact agreement and infinite-place convention remain unchecked |
| Abelian Galois extension | Same global class-field-theory characterization | `IsAbelianGaloisExtension K H` | Candidate encoding requires exact API/type and multiplication-convention audit |
| Artin reciprocity identifies the class group with the Galois group | E. Artin, *Beweis des allgemeinen Reziprozitatsgesetzes*, Abhandlungen aus dem Mathematischen Seminar der Universitat Hamburg 5 (1927), pp. 353-363; modern quotient/narrow-class conventions require cross-checking | `Nonempty ((H ≃ₐ[K] H) ≃* ClassGroup (𝓞 K))` inside `HilbertClassFieldCore` | Candidate only; map direction, automorphism-group identification, modulus, and finite/infinite convention are not frozen |
| Maximality and uniqueness over `K` | Standard Hilbert-class-field consequence of global reciprocity; a pinpoint modern source is still required | `HilbertClassFieldCore.maximal`; legacy uniqueness interfaces | Existing interfaces are discovery material and do not construct the field or prove uniqueness |

The repository source wording, "the maximal unramified abelian extension of a number field," is
too compressed to serve as an exact formal statement. This intake reads it as the finite Hilbert
class field, unramified at finite primes, not as the generally infinite maximal unramified
extension or as a local-class-field theorem. The statement phase must either confirm this reading
against pinned sources or record a source-scope blocker; it may not silently select an easier
variant.

The legacy file
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_075.lean` supplies useful candidate predicates,
but it is explicitly unaccepted under the uniform L0 baseline. Exact elaboration, normalized
expression identity, binder/universe audit, checked transports, and mutations of abelianity,
unramifiedness, maximality, reciprocity, and the base-field domain are deferred to the dependent
statement phase.

Discovery links, not immutable evidence receipts:

- Hilbert's Zahlbericht bibliographic record: <https://eudml.org/doc/144593>
- Artin's reciprocity paper bibliographic record: <https://eudml.org/doc/159218>
- Neukirch publisher record: <https://link.springer.com/book/10.1007/978-3-662-03983-0>

No `H0` claim is made. Required follow-up includes scanned-edition hashes, exact pages and theorem
numbers, translation/notation mapping, premise and convention crosswalk, errata search, and an
independent source reviewer.
