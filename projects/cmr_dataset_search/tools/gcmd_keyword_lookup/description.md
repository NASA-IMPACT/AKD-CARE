Retrieves controlled vocabulary terms from the local GCMD vocabulary file (gcmd.json) to normalize free-text variable names into GCMD-standard Science Keywords, and to expand synonyms before CMR search. Can also look up valid instrument and platform short names.

Primary access pattern: read from gcmd.json (bundled with the agent workspace). Do NOT call the live KMS API — the local file is the authoritative source.

gcmd.json covers three concept schemes:
- Science Keywords (Category > Topic > Term > Variable_Level_1 > Variable_Level_2 > Variable_Level_3 > Detailed_Variable)
- Instruments (Short_Name, Long_Name, URIs)
- Platforms (Short_Name, Long_Name, URIs)

Known issues:
- Hierarchy depth is inconsistent — Variable_Level_3 and Detailed_Variable often absent
- May not include the newest missions (file refresh cadence TBD)

If a term is not found in gcmd.json, fall back to using the original free-text term for CMR search. Do not call the live KMS API as a fallback.
