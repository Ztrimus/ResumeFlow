ACHIEVEMENTS ="""You are going to write a JSON resume section of "Achievements" for an applicant applying for job posts.

Step to follow:
1. Analyze my achievements details to match job requirements.
2. Create a JSON resume section that highlights strongest matches
3. Optimize JSON section for clarity and relevance to the job description.

Instructions:
1. Focus: Craft relevant achievements aligned with the job description.
2. Honesty: Prioritize truthfulness and objective language.
3. Specificity: Prioritize relevance to the specific job over general achievements.
4. Style:
  4.1. Voice: Use active voice whenever possible.
  4.2. Proofreading: Ensure impeccable spelling and grammar.

<achievements>
{section_data}
</achievements>

<job_description>
{job_description}
</job_description>

<example>
  "achievements": [
    "Won E-yantra Robotics Competition 2018 - IITB.",
    "1st prize in “Prompt Engineering Hackathon 2023 for Humanities”",
    "Received the 'Extra Miller - 2021' award at Winjit Technologies for outstanding performance.",
    [and So on ...]
  ]
</example>

{format_instructions}
"""

CERTIFICATIONS = """You are going to write a JSON resume section of "Certifications" for an applicant applying for job posts.

Step to follow:
1. Analyze my certification details to match job requirements.
2. Create a JSON resume section that highlights strongest matches
3. Optimize JSON section for clarity and relevance to the job description.

Instructions:
1. Focus: Include relevant certifications aligned with the job description.
2. Proofreading: Ensure impeccable spelling and grammar.

<CERTIFICATIONS>
{section_data}
</CERTIFICATIONS>

<job_description>
{job_description}
</job_description>

<example>
  "certifications": [
    {{
      "name": "Deep Learning Specialization",
      "by": "DeepLearning.AI, Coursera Inc.",
      "link": "https://www.coursera.org/account/accomplishments/specialization/G3WPNWRYX628"
    }},
    {{
      "name": "Server-side Backend Development",
      "by": "The Hong Kong University of Science and Technology.",
      "link": "https://www.coursera.org/account/accomplishments/verify/TYMQX23D4HRQ"
    }}
    ...
  ],
</example>

{format_instructions}
"""

EDUCATIONS = """You are going to write a JSON resume section of "Education" for an applicant applying for job posts.

Step to follow:
1. Analyze my education details to match job requirements.
2. Create a JSON resume section that highlights strongest matches
3. Optimize JSON section for clarity and relevance to the job description.

Instructions:
- Maintain truthfulness and objectivity in listing experience.
- Prioritize specificity - with respect to job - over generality.
- Proofread and Correct spelling and grammar errors.
- Aim for clear expression over impressiveness.
- Prefer active voice over passive voice.

<Education>
{section_data}
</Education>

<job_description>
{job_description}
</job_description>

<example>
"education": [
  {{
    "degree": "Masters of Science - Computer Science (Thesis)",
    "university": "Arizona State University, Tempe, USA",
    "from_date": "Aug 2023",
    "to_date": "May 2025",
    "grade": "3.8/4",
    "coursework": [
      "Operational Deep Learning",
      "Software verification, Validation and Testing",
      "Social Media Mining",
      [and So on ...]
    ]
  }}
  [and So on ...]
],
</example>

{format_instructions}
"""


PROJECTS="""You are going to write a JSON resume section of "Project Experience" for an applicant applying for job posts.

Step to follow:
1. Analyze my project details to match job requirements.
2. Create a JSON resume section that highlights strongest matches
3. Optimize JSON section for clarity and relevance to the job description.

Instructions:
1. Focus: Craft three highly relevant project experiences aligned with the job description.
2. Content:
  2.1. Bullet points: 3 per experience, closely mirroring job requirements.
  2.2. Impact: Quantify each bullet point for measurable results.
  2.3. Storytelling: Utilize STAR methodology (Situation, Task, Action, Result) implicitly within each bullet point.
  2.4. Action Verbs: Showcase soft skills with strong, active verbs.
  2.5. Honesty: Prioritize truthfulness and objective language.
  2.6. Structure: Each bullet point follows "Did X by doing Y, achieved Z" format.
  2.7. Specificity: Prioritize relevance to the specific job over general achievements.
3. Style:
  3.1. Clarity: Clear expression trumps impressiveness.
  3.2. Voice: Use active voice whenever possible.
  3.3. Proofreading: Ensure impeccable spelling and grammar.

<PROJECTS>
{section_data}
</PROJECTS>

<job_description>
{job_description}
</job_description>

<example>
"projects": [
    {{
      "name": "Search Engine for All file types - Sunhack Hackathon - Meta & Amazon Sponsored",
      "type": "Hackathon",
      "link": "https://devpost.com/software/team-soul-1fjgwo",
      "from_date": "Nov 2023",
      "to_date": "Nov 2023",
      "description": [
        "1st runner up prize in crafted AI persona, to explore LLM's subtle contextual understanding and create innovative collaborations between humans and machines.",
        "Devised a TabNet Classifier Model having 98.7% accuracy in detecting forest fire through IoT sensor data, deployed on AWS and edge devices 'Silvanet Wildfire Sensors' using technologies TinyML, Docker, Redis, and celery.",
        [and So on ...]
      ]
    }}
    [and So on ...]
  ]
  </example>
  
  {format_instructions}
  """

SKILLS="""You are going to write a JSON resume section of "Skills" for an applicant applying for job posts.

Step to follow:
1. Analyze my Skills details to match job requirements.
2. Create a JSON resume section that highlights strongest matches.
3. Optimize JSON section for clarity and relevance to the job description.

Instructions:
- Specificity: Prioritize relevance to the specific job over general achievements.
- Proofreading: Ensure impeccable spelling and grammar.

<SKILL_SECTION>
{section_data}
</SKILL_SECTION>

<job_description>
{job_description}
</job_description>

<example>
"skill_section": [
    {{
      "name": "Programming Languages",
      "skills": ["Python", "JavaScript", "C#", and so on ...]
    }},
    {{
      "name": "Cloud and DevOps",
      "skills": [ "Azure", "AWS", and so on ... ]
    }},
    and so on ...
  ]
</example>
  
  {format_instructions}
  """


EXPERIENCE="""You are going to write a JSON resume section of "Work Experience" for an applicant applying for job posts.

Step to follow:
1. Analyze my Work details to match job requirements.
2. Create a JSON resume section that highlights strongest matches
3. Optimize JSON section for clarity and relevance to the job description.

Instructions:
1. Focus: Craft three highly relevant work experiences aligned with the job description.
2. Content:
  2.1. Bullet points: 3 per experience, closely mirroring job requirements.
  2.2. Impact: Quantify each bullet point for measurable results.
  2.3. Storytelling: Utilize STAR methodology (Situation, Task, Action, Result) implicitly within each bullet point.
  2.4. Action Verbs: Showcase soft skills with strong, active verbs.
  2.5. Honesty: Prioritize truthfulness and objective language.
  2.6. Structure: Each bullet point follows "Did X by doing Y, achieved Z" format.
  2.7. Specificity: Prioritize relevance to the specific job over general achievements.
3. Style:
  3.1. Clarity: Clear expression trumps impressiveness.
  3.2. Voice: Use active voice whenever possible.
  3.3. Proofreading: Ensure impeccable spelling and grammar.

<work_experience>
{section_data}
</work_experience>

<job_description>
{job_description}
</job_description>

<example>
"work_experience": [
    {{
      "role": "Software Engineer",
      "company": "Winjit Technologies",
      "location": "Pune, India"
      "from_date": "Jan 2020",
      "to_date": "Jun 2022",
      "description": [
        "Engineered 10+ RESTful APIs Architecture and Distributed services; Designed 30+ low-latency responsive UI/UX application features with high-quality web architecture; Managed and optimized large-scale Databases. (Systems Design)",  
        "Initiated and Designed a standardized solution for dynamic forms generation, with customizable CSS capabilities feature, which reduces development time by 8x; Led and collaborated with a 12 member cross-functional team. (Idea Generation)"  
        and so on ...
      ]
    }},
    {{
      "role": "Research Intern",
      "company": "IMATMI, Robbinsville",
      "location": "New Jersey (Remote)"
      "from_date": "Mar 2019",
      "to_date": "Aug 2019",
      "description": [
        "Conducted research and developed a range of ML and statistical models to design analytical tools and streamline HR processes, optimizing talent management systems for increased efficiency.",
        "Created 'goals and action plan generation' tool for employees, considering their weaknesses to facilitate professional growth.",
        and so on ...
      ]
    }}
  ],
</example>

{format_instructions}
"""