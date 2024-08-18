'''
-----------------------------------------------------------------------
File: schemas/sections_schmas.py
Creation Time: Aug 18th 2024, 2:26 am
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
'''

from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

class Achievements(BaseModel):
    achievements: List[str] = Field(description="job relevant key accomplishments, awards, or recognitions that demonstrate your skills and abilities.")

class Certification(BaseModel):
    name: str = Field(description="The name of the certification.")
    by: str = Field(description="The organization or institution that issued the certification.")
    link: str = Field(description="A link to verify the certification.")

class Certifications(BaseModel):
    certifications: List[Certification] = Field(description="job relevant certifications that you have earned, including the name, issuing organization, and a link to verify the certification.")

class Education(BaseModel):
    degree: str = Field(description="The degree or qualification obtained and The major or field of study. e.g., Bachelor of Science in Computer Science.")
    university: str = Field(description="The name of the institution where the degree was obtained with location. e.g. Arizona State University, Tempe, USA")
    from_date: str = Field(description="The start date of the education period. e.g., Aug 2023")
    to_date: str = Field(description="The end date of the education period. e.g., May 2025")
    courses: List[str] = Field(description="Relevant courses or subjects studied during the education period. e.g. [Data Structures, Algorithms, Machine Learning]")

class Educations(BaseModel):
    education: List[Education] = Field(description="Educational qualifications, including degree, institution, dates, and relevant courses.")

class Link(BaseModel):
    name: str = Field(description="The name or title of the link.")
    link: str = Field(description="The URL of the link.")

class Project(BaseModel):
    name: str = Field(description="The name or title of the project."),
    type: str | None = Field(description="The type or category of the project, such as hackathon, publication, professional, and academic."),
    link: str = Field(description="A link to the project repository or demo.")
    resources: Optional[List[Link]] = Field(description="Additional resources related to the project, such as documentation, slides, or videos.")
    from_date: str = Field(description="The start date of the project. e.g. Aug 2023"),
    to_date: str = Field(description="The end date of the project. e.g. Nov 2023"),
    description: List[str] = Field(description="A list of 3 bullet points describing the project experience, tailored to match job requirements. Each bullet point should follow the 'Did X by doing Y, achieved Z' format, quantify impact, implicitly use STAR methodology, use strong action verbs, and be highly relevant to the specific job. Ensure clarity, active voice, and impeccable grammar.")

class Projects(BaseModel):
    projects: List[Project] = Field(description="Project experiences, including project name, type, link, resources, dates, and description.")

class SkillSection(BaseModel):
    name: str = Field(description="name or title of the skill group and competencies relevant to the job, such as programming languages, data science, tools & technologies, cloud & DevOps, full stack,  or soft skills.")
    skills: List[str] = Field(description="Specific skills or competencies within the skill group, such as Python, JavaScript, C#, SQL in programming languages.")

class SkillSections(BaseModel):
    skill_section: List[SkillSection] = Field(description="Skill sections, each containing a group of skills and competencies relevant to the job.")

class Experience(BaseModel):
    role: str = Field(description="The job title or position held. e.g. Software Engineer, Machine Learning Engineer.")
    company: str = Field(description="The name of the company or organization.")
    location: str = Field(description="The location of the company or organization. e.g. San Francisco, USA.")
    from_date: str = Field(description="The start date of the employment period. e.g., Aug 2023")
    to_date: str = Field(description="The end date of the employment period. e.g., Nov 2025")
    description: List[str] = Field(description="A list of 3 bullet points describing the work experience, tailored to match job requirements. Each bullet point should follow the 'Did X by doing Y, achieved Z' format, quantify impact, implicitly use STAR methodology, use strong action verbs, and be highly relevant to the specific job. Ensure clarity, active voice, and impeccable grammar.")

class Experiences(BaseModel):
    work_experience: List[Experience] = Field(description="Work experiences, including job title, company, location, dates, and description.")

class Media(BaseModel):
    linkedin: Optional[HttpUrl] = Field(description="LinkedIn profile URL")
    github: Optional[HttpUrl] = Field(description="GitHub profile URL")
    medium: Optional[HttpUrl] = Field(description="Medium profile URL")
    devpost: Optional[HttpUrl] = Field(description="Devpost profile URL")

class ResumeSchema(BaseModel):
    name: str = Field(description="The full name of the candidate.")
    summary: Optional[str] = Field(description="A brief summary or objective statement highlighting key skills, experience, and career goals.")
    phone: str = Field(description="The contact phone number of the candidate.")
    email: str = Field(description="The contact email address of the candidate.")
    media: Media = Field(description="Links to professional social media profiles, such as LinkedIn, GitHub, or personal website.")
    work_experience: List[Experience] = Field(description="Work experiences, including job title, company, location, dates, and description.")
    education: List[Education] = Field(description="Educational qualifications, including degree, institution, dates, and relevant courses.")
    skill_section: List[SkillSection] = Field(description="Skill sections, each containing a group of skills and competencies relevant to the job.")
    projects: List[Project] = Field(description="Project experiences, including project name, type, link, resources, dates, and description.")
    certifications: List[Certification] = Field(description="job relevant certifications that you have earned, including the name, issuing organization, and a link to verify the certification.")
    achievements: List[str] = Field(description="job relevant key accomplishments, awards, or recognitions that demonstrate your skills and abilities.")