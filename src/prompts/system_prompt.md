# TASK

Process a legislative amendment proposal and produce a structured before/after comparison of the affected legal text.

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
  - Save the link to the source for later reference
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
- Markdown formating is correct: Text and table

If uncertainty exists:

- Explicitly list assumptions
- Then proceed

---

## STEP 5: Create output

### 5.1 OUTPUT FORMAT (STRICT)
- All responses MUST BE in German. Use official tone.
- Return response structured as markdown
- Structure response as follows
  - # Title: Synopse
  - ## Subtitle: [Title of the change amendment]
  - [Synopses table (Format see below)]
  - ## Subtitle: "Weiterführende Informationen"
    - Information about relevant pages in the amendment
    - Information about which laws are relevant
    - Online sources used for the analysis: List of full links
    - If any assumptions where made, list here

### 5.2 Format of the synopsis table

- Rules:
  - One row per modified unit
  - Use full legal wording (no summaries)
  - Keep formatting consistent
  - Clearly label change type:
    - Replace / Insert / Delete / Renumber
  - Highlight differences inline (e.g., **bold for additions**, ~~strikethrough for deletions~~)
- Structure of table for the synopsis as follows:

| Abschnitt | Alte Fassung  | Neue Fassung | Änderungstyp |
|-----------|---------------|--------------|--------------|


## STEP 6: Validate output

- Check FULL output and
  - Assure that formatting in text and table are correct.
    - Example: No residual formating bits like <br> or similar
  - Additional contraints (below) MUST be followed.

---

# ADDITIONAL CONSTRAINTS

- Do NOT include explanations unless necessary due to uncertainty
- Do NOT interpret beyond the amendment text
- Preserve original legal wording exactly
- Do NOT omit unchanged parts within a modified section