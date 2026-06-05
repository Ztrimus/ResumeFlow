'''
-----------------------------------------------------------------------
File: prompts/sections_prompt.py
Creation Time: Aug 17th 2024, 7:01 pm
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
'''

# ---------------------------------------------------------------------------
# Shared few-shot bullet examples (referenced in EXPERIENCE and PROJECTS)
# ---------------------------------------------------------------------------
_BULLET_EXAMPLES = """
<few_shot_examples>
  <example id="1">
    <original>Managed database systems</original>
    <job_keyword>PostgreSQL, query optimization</job_keyword>
    <rewritten>Reduced query latency by 40% by redesigning 15 high-frequency PostgreSQL indexes, cutting p99 response time from 800ms to 480ms across 3 production services handling 2M daily requests</rewritten>
    <pattern>Action(Reduced) + Skill(redesigning PostgreSQL indexes) + Metric(40% latency drop, scale)</pattern>
  </example>
  <example id="2">
    <original>Worked on machine learning models</original>
    <job_keyword>scikit-learn, model accuracy, production deployment</job_keyword>
    <rewritten>Improved fraud detection precision from 71% to 89% by retraining a gradient-boosted classifier (scikit-learn) on 18 months of transaction data, deployed to production via Docker and AWS SageMaker</rewritten>
    <pattern>Action(Improved) + Skill(retraining gradient-boosted classifier) + Metric(precision delta, deployment context)</pattern>
  </example>
  <example id="3">
    <original>Led a team of engineers</original>
    <job_keyword>cross-functional collaboration, Agile, delivery</job_keyword>
    <rewritten>Led a 6-engineer cross-functional team (FE, BE, ML) delivering a real-time recommendation engine in 10 weeks using Agile sprints, increasing user engagement by 23% at launch</rewritten>
    <pattern>Action(Led) + Skill(cross-functional Agile delivery) + Metric(team size, timeline, business outcome)</pattern>
  </example>
</few_shot_examples>"""


ACHIEVEMENTS = """<task>
Write the "achievements" section of a JSON resume for a candidate applying to the role described below. Select and frame achievements that directly signal value for this specific position.
</task>

<candidate_achievements>
{section_data}
</candidate_achievements>

<job_description>
{job_description}
</job_description>

<reasoning>
Before selecting achievements:
1. Which achievements demonstrate skills or outcomes explicitly mentioned in the job description?
2. Which achievements show scale, recognition, or competitive performance most relevant to this role?
3. Which should be dropped or deprioritized because they have no relevance to this position?
</reasoning>

<instructions>
- Include only achievements that strengthen this application — omit unrelated ones.
- Preserve the factual content exactly; do not fabricate awards or prizes.
- Use active, specific language. Quantify where numbers are present or implied.
- Order by relevance to the job description, most relevant first.
</instructions>

<example>
"achievements": [
  "1st place, Prompt Engineering Hackathon 2023 (Humanities track) — outperformed 120 teams",
  "Won E-Yantra Robotics Competition 2018 — IIT Bombay, Top 5 nationally",
  "Received 'Extra Miler 2021' award at Winjit Technologies for on-time delivery of 3 critical client projects"
]
</example>"""


CERTIFICATIONS = """<task>
Write the "certifications" section of a JSON resume for a candidate applying to the role described below. Prioritize certifications most relevant to the job requirements.
</task>

<candidate_certifications>
{section_data}
</candidate_certifications>

<job_description>
{job_description}
</job_description>

<reasoning>
Before selecting certifications:
1. Which certifications directly validate skills listed as required or preferred in the job description?
2. Are there certifications from recognized issuers (AWS, Google, Coursera partnered universities) that signal credibility for this role?
3. Should any unrelated certifications be dropped to keep the section concise?
</reasoning>

<instructions>
- Preserve certification names, issuers, and links exactly as provided.
- Order by relevance to the job description, most relevant first.
- Do not invent or modify certification details.
</instructions>

<example>
"certifications": [
  {{
    "name": "Deep Learning Specialization",
    "by": "DeepLearning.AI, Coursera",
    "link": "https://www.coursera.org/account/accomplishments/specialization/G3WPNWRYX628"
  }},
  {{
    "name": "AWS Certified Solutions Architect – Associate",
    "by": "Amazon Web Services",
    "link": "https://www.credly.com/badges/..."
  }}
]
</example>"""


EDUCATIONS = """<task>
Write the "education" section of a JSON resume for a candidate applying to the role described below.
</task>

<candidate_education>
{section_data}
</candidate_education>

<job_description>
{job_description}
</job_description>

<reasoning>
Before structuring the education section:
1. Does the job description specify a degree requirement? Does the candidate meet or exceed it?
2. Are there specific coursework items that directly map to required skills in the JD? Surface those.
3. Should GPA be included? Include it if 3.5+ and the role is entry/mid level; omit for senior roles unless exceptional.
</reasoning>

<instructions>
- Preserve all factual details (institution, degree, dates, GPA) exactly as provided.
- For coursework, select courses most relevant to the job description — do not list all courses.
- Use standardized date format: "Mon YYYY" (e.g., "Aug 2023").
- Order education entries reverse-chronologically (most recent first).
</instructions>

<example>
"education": [
  {{
    "degree": "Master of Science — Computer Science (Thesis)",
    "university": "Arizona State University, Tempe, USA",
    "from_date": "Aug 2023",
    "to_date": "May 2025",
    "grade": "3.8/4.0",
    "coursework": [
      "Operational Deep Learning",
      "Software Verification, Validation and Testing",
      "Social Media Mining"
    ]
  }}
]
</example>"""


PROJECTS = """<task>
Write the "projects" section of a JSON resume for a candidate applying to the role described below. Select and rewrite projects to maximize alignment with the job requirements.
</task>

<candidate_projects>
{section_data}
</candidate_projects>

<job_description>
{job_description}
</job_description>

<reasoning>
Work through this analysis before writing:
1. Which 2-3 projects most directly demonstrate skills required by this job description?
2. For each selected project, which existing bullets can be rewritten to better surface relevant keywords?
3. What metrics or outcomes are implied but not stated? (e.g., "built for 1000 users" → "scaled to 1K users")
4. Which projects should be excluded because they have no relevance to this role?
</reasoning>

<instructions>
- Select 2-3 most relevant projects. Drop irrelevant ones.
- Each project: 2-3 bullet points using Action + Skill + Metric format.
- Weave in job description keywords naturally — never keyword-stuff.
- Quantify every bullet where possible. If no metric exists, add scale/context.
- Do not fabricate project details, links, or outcomes.
- Dates: "Mon YYYY" format.
</instructions>
""" + _BULLET_EXAMPLES + """
<output_schema>
"projects": [
  {{
    "name": "<project name>",
    "type": "<Hackathon | Personal | Academic | Open Source>",
    "link": "<url or null>",
    "from_date": "<Mon YYYY or null>",
    "to_date": "<Mon YYYY or null>",
    "description": [
      "<bullet 1: Action + Skill + Metric>",
      "<bullet 2: Action + Skill + Metric>"
    ]
  }}
]
</output_schema>"""


SKILLS = """<task>
Write the "skill_section" of a JSON resume for a candidate applying to the role described below. Organize and prioritize skills to match the job requirements.
</task>

<candidate_skills>
{section_data}
</candidate_skills>

<job_description>
{job_description}
</job_description>

<reasoning>
Before organizing skills:
1. What are the Tier 1 technical skills in the job description (explicitly required)? Ensure these appear prominently.
2. What skill groupings make the most sense for this role? (e.g., an ML role: Languages / ML Frameworks / Cloud / Tools)
3. Are there skills in the candidate's profile that are irrelevant noise for this specific role?
</reasoning>

<instructions>
- Group skills into 3-5 logical categories relevant to the role.
- List Tier 1 job keywords first within each category.
- Remove skills with no relevance to the target role — a focused skill section beats a long one.
- Preserve exact tool/library names (e.g., "PyTorch" not "deep learning framework").
</instructions>

<example>
"skill_section": [
  {{
    "name": "Languages",
    "skills": ["Python", "TypeScript", "SQL", "Bash"]
  }},
  {{
    "name": "ML & Data",
    "skills": ["PyTorch", "scikit-learn", "Pandas", "NumPy", "Hugging Face"]
  }},
  {{
    "name": "Cloud & DevOps",
    "skills": ["AWS (EC2, S3, Lambda)", "Docker", "Kubernetes", "GitHub Actions"]
  }}
]
</example>"""


EXPERIENCE = """<task>
Write the "work_experience" section of a JSON resume for a candidate applying to the role described below. Rewrite bullets to maximize alignment with job requirements while staying truthful.
</task>

<candidate_experience>
{section_data}
</candidate_experience>

<job_description>
{job_description}
</job_description>

<reasoning>
Work through this analysis before writing:
1. Which 2-3 work experiences are most relevant to this role? Which should be de-emphasized or omitted?
2. For each selected experience, identify which original bullets already align with the JD and which need rewriting.
3. What Tier 1 keywords from the JD can be woven into bullets truthfully based on what the candidate actually did?
4. Where are the opportunities to add missing metrics (scale, speed, size, reduction, improvement)?
5. Are there soft skills (leadership, cross-functional work, mentoring) the JD values that can be evidenced by existing work?
</reasoning>

<instructions>
- Include 2-3 most relevant experiences. Preserve all factual details (company, role, dates, location).
- Each experience: 3 bullet points using Action + Skill + Metric format.
- Start each bullet with a strong past-tense action verb.
- Naturally incorporate Tier 1 job description keywords — no keyword stuffing.
- Quantify every bullet (numbers, percentages, scale, time saved). If original has no metric, add reasonable context.
- Do not change job titles, companies, or dates. Do not fabricate outcomes.
- Order experiences reverse-chronologically.
</instructions>
""" + _BULLET_EXAMPLES + """
<output_schema>
"work_experience": [
  {{
    "role": "<exact job title>",
    "company": "<exact company name>",
    "location": "<City, Country or Remote>",
    "from_date": "<Mon YYYY>",
    "to_date": "<Mon YYYY or Present>",
    "description": [
      "<bullet 1: Action + Skill + Metric>",
      "<bullet 2: Action + Skill + Metric>",
      "<bullet 3: Action + Skill + Metric>"
    ]
  }}
]
</output_schema>"""
