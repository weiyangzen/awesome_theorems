# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0755`, the title `解析层次`, the attribution Stephen Kleene, the
year 1955, and the gloss `解析集合的层次`. The neighboring records `THM-M-0754` (arithmetical
hierarchy) and `THM-M-0756` (hyperarithmetic theory) support reading this as Kleene's effective,
lightface analytical hierarchy, but they do not select a theorem. Importance `高` and status
`已验证` are inventory metadata, not human-source or Lean-kernel evidence.

An authoritative secondary source confirms that several different results live under this topic.
Its strictness theorem is a strong candidate locator, not the selected target. Intake preserves the
topic identity and the repository's stated historical boundary without manufacturing a proposition.

## Proposition-changing decisions

An approved statement phase must freeze all of the following from a pinpoint immutable source:

1. Whether the target is the lightface analytical hierarchy of definability over the standard
   second-order structure on natural numbers, a relativized hierarchy with parameters, or the
   boldface projective hierarchy on a specified Polish space.
2. The exact syntax and semantics: number variables, set variables or function variables, free
   variables and parameters, the base language of arithmetic, standard-model interpretation, and
   the coding of finite tuples, formulas, sets, functions, and satisfaction.
3. The hierarchy indexing convention, including the common base class
   `Sigma^1_0 = Pi^1_0`, alternation counting, prenex/normal-form requirements, and the definition
   of `Delta^1_n`.
4. The classified objects: formulas, predicates/relations, subsets of natural numbers, subsets of
   products with powersets, reals/Baire-space points, or pointsets in a general Polish space.
5. The exact conclusion: definition/normal form, closure, inclusion, strictness, existence of a
   separating set, completeness, universal-set/enumeration theorem, or a hyperarithmetic
   characterization.
6. If strictness is selected, whether the conclusion includes one or both `Sigma`/`Pi` witnesses,
   complement transport, nonmembership at the same level, and nonmembership in every lower level.
7. Ordered binders and all ranges, especially `n >= 1`, arities, free parameters, complement
   universe, reducibility notion, extensional equality of sets, and any classical-choice or coding
   assumptions.
8. Boundary cases such as level zero, empty/full sets, zero arity, no set quantifiers, number-only
   formulas, parameters, complement, and the relation between set- and function-quantifier
   encodings.

Each choice changes the proposition or its foundation profile. This list is a resolution ledger,
not a theorem statement.

## Candidate branches not credited

- **Hierarchy strictness:** for every source-selected `n >= 1`, existence of a subset of natural
  numbers that is `Pi^1_n`-definable but not `Sigma^1_n`-definable, with the complementary witness
  and lower-level exclusions. This is the theorem-shaped candidate closest to the gloss.
- **Normal form:** every analytical relation admits an alternating block of set or function
  quantifiers over an arithmetical matrix.
- **Level inclusions:** embeddings of `Sigma^1_n` and `Pi^1_n` into a source-defined next-level
  `Delta` class.
- **Completeness/universality:** existence of universal or complete predicates/sets at a fixed
  level under a selected reduction.
- **First-level characterization:** `Delta^1_1`-definable subsets of natural numbers coincide with
  the hyperarithmetic sets.
- **Boldface comparison:** correspondences with projective pointclasses on Baire, Cantor, or other
  Polish spaces, with or without effective/lightface restrictions.

No branch is canonical, asserted, or credited at intake.

## Explicit exclusions and neighbors

The following cannot substitute for the target:

- merely defining alternating predicate families and proving tautological facts stored in those
  definitions;
- `THM-M-0754`, the arithmetical hierarchy using number quantifiers only;
- `THM-M-0756`, hyperarithmetic theory or the isolated characterization `Delta^1_1 = HYP`, unless an
  approved source makes that exact proposition the intended root rather than a neighboring result;
- `THM-M-0806`, the separately cataloged boldface analytic-set theorem family;
- `THM-M-0808`, the separately cataloged projective hierarchy;
- the boldface `MeasureTheory.AnalyticSet` API alone, which formalizes continuous images of Polish
  spaces but not Kleene's full lightface analytical hierarchy or its level strictness;
- `Descriptive.tree` alone, which is generic tree infrastructure and contains no well-foundedness,
  effective coding, `Sigma^1_n`/`Pi^1_n` pointclasses, or hierarchy theorem;
- complex or real analytic functions, despite the shared English word "analytic";
- a fixed finite toy hierarchy, a changed foundation, or a theorem whose desired separation is an
  assumption or structure field;
- the untrusted repository label `已验证` as source or kernel evidence.

No canonical Lean target is frozen at intake because the repository record does not identify one
truth-valued proposition.
