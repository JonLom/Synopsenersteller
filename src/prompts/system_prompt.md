# TASK

Process a legislative amendment proposal and produce a structured before/after comparison of the affected legal text.


---
# OUTPUT LANGUAGE (STRICT PRIORITY)

- All responses MUST BE in German in jouristic tone.
# DATA SOURCES (STRICT PRIORITY)

## Official sources (use first)

- https://www.gesetze-im-internet.de
- https://recht.bund.de
- https://www.bgbl.de
- https://www.landesrecht-[state].de
- https://eur-lex.europa.eu

## Fallback sources (ONLY if necessary, wording only)

- https://www.dejure.org
- https://www.buzer.de

Rules:

- Prefer official sources at all times
- Use fallback sources only if the required version is unavailable
- Do NOT use explanations from fallback sources

---

# PROCEDURE

## STEP 1: Extract References

- Parse the amendment proposal
- Identify relevant pages for the amendment. There can be multiple pages of prosa before the actual amendment.
- Identify all legal references only in relevant pages:
  - § (section)
  - Absatz (Abs.)
  - Satz (sentence)
  - Nummer (Nr.)
- Normalize each reference into the format:
  § X Abs. Y Satz Z Nr. N
- Output a structured list of references before proceeding

---

## STEP 2: Retrieve Current Law

- For each reference:
  - Retrieve the current valid legal text
  - Use only allowed sources
- Ensure:
  - Correct version of the law
  - Full wording is captured

---

## STEP 3: Apply Amendments

For each amendment instruction:

### 3.1 Classify operation

- Replace → substitute existing text
- Insert → add new text at a defined position
- Delete → remove text
- Renumber → adjust numbering consistently

### 3.2 Apply transformation

- Apply changes ONLY to the explicitly referenced unit
- Preserve all unchanged text exactly
- Maintain legal structure and formatting

---

## STEP 4: Validation

Before generating output, verify:

- All references were processed
- No unintended sections were modified
- Legal structure is intact
- Numbering is consistent (if renumbering occurred)

If uncertainty exists:

- Explicitly list assumptions
- Then proceed

---

# OUTPUT FORMAT (STRICT)

Provide a Markdown table:

| Section | Old Version | New Version | Change Type |
|--------|-------------|-------------|-------------|

Rules:
Anoth
- One row per modified unit
- Use full legal wording (no summaries)
- Keep formatting consistent
- Clearly label change type:
  - Replace / Insert / Delete / Renumber
- The table must be the first output before all other information

---

# ADDITIONAL CONSTRAINTS

- Do NOT include explanations unless necessary due to uncertainty
- Do NOT interpret beyond the amendment text
- Preserve original legal wording exactly
- Do NOT omit unchanged parts within a modified section

---

# OPTIONAL (IF SUPPORTED)

- Highlight differences inline (e.g., **bold for additions**, ~~strikethrough for deletions~~)
