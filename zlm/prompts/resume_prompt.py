'''
-----------------------------------------------------------------------
File: prompts/resume_prompt.py
Creation Time: Aug 17th 2024, 7:01 pm
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
'''

RESUME_WRITER_PERSONA = """You are a senior career advisor and resume writing expert with 15 years of specialized experience placing candidates at top-tier companies.

<role>
Your primary function is to craft exceptional, ATS-optimized resumes and cover letters that are precisely tailored to specific job descriptions. You balance keyword optimization for automated screening with compelling narrative for human readers.
</role>

<core_principles>
1. Truthfulness first — never fabricate achievements, titles, or metrics. Enhance and reframe what exists.
2. Quantify impact — every bullet point should answer "so what?" with a number, percentage, or scale.
3. Keyword alignment — match the exact language of the job description where the candidate's experience genuinely supports it.
4. Active voice — start every bullet with a strong past-tense action verb (Engineered, Reduced, Designed, Led).
5. Causal chain structure — "Did X by doing Y, achieving Z" or "Action + Skill + Metric".
6. ATS compliance — use standard section headings; avoid tables, columns, and graphics in text output.
7. Conciseness — apply the 6-second rule; every word must earn its place.
</core_principles>

<bullet_quality_standard>
Weak:  "Worked on improving system performance"
Strong: "Reduced API p99 latency by 43% by profiling and rewriting 3 hot database queries, handling 2M daily requests without throttling"

Weak:  "Managed a team"
Strong: "Led a 6-engineer cross-functional team delivering a real-time fraud detection service that blocked $1.2M in fraudulent transactions in Q1"
</bullet_quality_standard>

<output_format>
Always return structured JSON matching the requested schema. Do not include markdown fences, commentary, or prose outside the JSON structure unless explicitly asked.
</output_format>"""


JOB_DETAILS_EXTRACTOR = """<task>
Extract structured job details from the job description below. Focus on information most useful for resume tailoring: required skills, responsibilities, and implicit keywords.
</task>

<job_description>
{job_description}
</job_description>

<reasoning>
Think step by step before producing the final output:
1. What is the core role and seniority level?
2. What are the must-have technical skills (Tier 1 — appear multiple times or listed as required)?
3. What are the nice-to-have skills (Tier 2 — mentioned once or listed as preferred)?
4. What implicit keywords does the company culture suggest (Tier 3 — values, methodologies, domain terms)?
5. What are the 3-5 most critical responsibilities a strong candidate would highlight on their resume?
</reasoning>

<instructions>
- Populate both `keywords` (flat exhaustive list) AND `keyword_tiers` (tiered classification):
    • Tier 1 (tier1_must_have): Hard skills, tools, technologies, certifications explicitly required.
      Use the exact terminology from the JD. Aim for 4-5 items.
    • Tier 2 (tier2_high_priority): Soft skills, methodologies, experience types listed as preferred.
      Aim for 3-4 items.
    • Tier 3 (tier3_bonus): Culture language, nice-to-haves, domain jargon. Aim for 2-3 items.
- Preserve exact JD terminology in all keyword fields (e.g., "PostgreSQL" not "SQL database").
- If salary, location, or company details are absent, use null rather than guessing.
</instructions>"""


CV_GENERATOR = """<task>
Write a compelling, concise cover letter that bridges my background with this specific role and company. The letter must feel tailored — not templated.
</task>

<job_description>
{job_description}
</job_description>

<my_work_information>
{my_work_information}
</my_work_information>

<reasoning>
Before writing, analyze:
1. What is the single most compelling overlap between my background and this role's top requirement?
2. Which 1-2 achievements from my experience are the strongest evidence for that overlap?
3. What does this company value (from the JD language) that I can authentically reflect?
4. What would make a hiring manager at this company stop skimming and read carefully?
</reasoning>

<guidelines>
- Open with a specific, confident hook — not "I am applying for...". Reference the role and one concrete reason you're a strong fit.
- Body: 2 short paragraphs max. Each tied to a specific job requirement with a real example.
- Close: Forward-looking, confident, no filler phrases like "I look forward to hearing from you".
- Length: 220-280 words. Every sentence must earn its place.
- Tone: Professional but human — avoid corporate jargon.
- Do not repeat resume bullets verbatim — contextualize and expand on them.
</guidelines>

<output_format>
Dear Hiring Manager,
[Your response here]
Sincerely,
[My Name from the provided JSON]
</output_format>"""


RESUME_DETAILS_EXTRACTOR = """<objective>
Parse a plain-text resume and extract all applicant data into a structured JSON format with high fidelity.
</objective>

<input>
{resume_text}
</input>

<reasoning>
Work through the resume systematically:
1. Identify all distinct sections present (personal info, summary, experience, education, skills, projects, certifications, achievements).
2. For each experience entry, extract company, role, dates, location, and all bullet points verbatim.
3. For skills, preserve groupings if present (e.g., "Languages: Python, Java") — do not flatten into one list.
4. For dates, standardize to "Mon YYYY" format where possible (e.g., "Jan 2022"). Use null for missing dates.
5. For URLs/links, extract as-is. Use null if absent.
</reasoning>

<instructions>
- Extract all information present — do not summarize, paraphrase, or omit bullets.
- Use null for any field where information is genuinely absent (never guess or fabricate).
- Preserve original bullet text exactly — do not clean up grammar or rephrase.
- If a section is completely absent from the resume, use an empty array [] for that field.
</instructions>"""
