# Tiebreaker: Choosing Between Equivalent Collections

## The heuristic
When two or more collections appear to measure the same variable at similar quality, apply these tiebreakers in order:

1. **Prefer longer archive** — more temporal depth enables trend analysis and climatology
2. **Prefer higher spatial completeness** — fewer gaps is more useful than marginally finer resolution
3. **Prefer the most recent algorithm version** — check collection version number in the short name (e.g., V061 > V006); newer versions incorporate calibration improvements and bug fixes
4. **Prefer the instrument with broader literature adoption** — if papers in Semantic Scholar consistently cite one product over another, recommend that one; it signals community trust and established validation
5. **Prefer the collection with richer CMR metadata** — a collection with complete temporal/spatial/variable documentation is more likely to be actively maintained

## When it applies
Any time two or more CMR collections are returned for the same variable and no single one is clearly superior on the researcher's stated criteria.

## Exceptions
- If the researcher has stated an instrument preference, honor it — do not override with this tiebreaker
- If temporal coverage is the binding constraint (e.g., "I need data before 2010"), archive length is decisive, not a tiebreaker
- If the science question is highly spatial (e.g., field-scale, urban), resolution may outweigh completeness in step 2

## What to do
When recommending a collection that was selected via tiebreaker, briefly explain which criterion broke the tie. Example: "I recommend MOD11A1 over MYD11A1 because Terra's archive extends to Feb 2000, giving you 2.5 additional years of data."
