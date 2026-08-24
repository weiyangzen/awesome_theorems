# S5-CLM-00003587 process audit

The worker processed only the frozen `S5THM-00003587-TARGET` claim in its
fresh task generation.  Intake binds `Erdos1037.erdos_1037` to provider
revision `2270d31e8dd611521f979de6d86da364930b7669`, its source file digest,
declaration digest, and Stage6 alias `S6-CLM-00000467` / `S6-VAR-00003963`.

The statement, proof, and audit Lean surfaces import the exact provider
module and transport the qualified source declaration without local
definitions, aliases, parser extensions, or substitution hypotheses.  The
crosswalk records the semantic environment and empty substitution/shadow
sets.  Machine and readability ledgers are sealed separately; the release
decision remains provisional until canonical-Master acceptance.
