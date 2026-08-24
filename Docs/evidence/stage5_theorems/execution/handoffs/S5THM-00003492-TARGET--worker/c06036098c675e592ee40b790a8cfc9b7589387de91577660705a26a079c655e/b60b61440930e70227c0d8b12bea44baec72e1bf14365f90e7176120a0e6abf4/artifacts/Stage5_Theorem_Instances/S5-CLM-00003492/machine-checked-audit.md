# Machine-checked audit candidate

Root declaration: `AwesomeTheorems.Stage5.S5_CLM_00003492.maximalLength_le_audit`.

The root has the frozen proposition with provider-local names expanded: for every natural `n`, the supremum of lengths of lists of triples whose entries lie in `[1,n]` and whose earlier/later elements increase in two distinct coordinates is at most `n ^ 2`.

The declaration graph is closed locally:

- `source_set_membership_iff` and `maximalLength_le_statement` normalize the statement by set extensionality.
- `exists_pair_of_mem_Icc` maps every position to its first-coordinate pair in the `n × n` box and applies finite pigeonhole.
- `not_pairwise_step_of_first_two_ge` proves that equality of those coordinates rules out any two-coordinate strict increase.
- `maximalLength_le` applies the collision in the appropriate index order and closes the natural supremum with `csSup_le`.
- `Audit.lean` repeats the independent proof in a provider-native standalone compilation unit, then asks the kernel for its exact provider type and axiom census.

No `sorry`, `admit`, `axiom`, `opaque`, unsafe declaration, local semantic definition, abbreviation, notation, macro, coercion, namespace alias, instance, or provider proof-body reference appears in active declaration code. Each Lean file independently imports the exact frozen provider module and references the exact provider declaration, so Master can replay every artifact directly in the sealed provider environment.

This worker did not run Lean, Lake, or Elan. Therefore the declared M0-L level and cold replay are a candidate for canonical Master recomputation, not a worker claim of canonical acceptance.
