'''
-----------------------------------------------------------------------
File: schemas/job_details_schema.py
Creation Time: Aug 17th 2024, 8:18 pm
Author: Saurabh Zinjad
Developer Email: saurabhzinjad@gmail.com
Copyright (c) 2023-2024 Saurabh Zinjad. All rights reserved | https://github.com/Ztrimus
-----------------------------------------------------------------------
'''

from typing import List
from pydantic import BaseModel, Field


class KeywordTiers(BaseModel):
    """Keywords from a job description classified by priority for resume tailoring."""

    tier1_must_have: List[str] = Field(
        description=(
            "Hard skills, specific tools, technologies, and certifications explicitly listed "
            "as required. These MUST appear in the tailored resume. 4-5 keywords."
        )
    )
    tier2_high_priority: List[str] = Field(
        description=(
            "Soft skills, experience types, and methodologies listed as preferred or strongly "
            "desired. Include where the candidate's background genuinely supports them. 3-4 keywords."
        )
    )
    tier3_bonus: List[str] = Field(
        description=(
            "Company culture language, nice-to-haves, and industry-specific terminology. "
            "Weave into the cover letter and summary where authentic. 2-3 keywords."
        )
    )


class JobDetails(BaseModel):
    job_title: str = Field(description="The specific role, its level, and scope within the organization.")
    job_purpose: str = Field(description="A high-level overview of the role and why it exists in the organization.")
    keywords: List[str] = Field(description="All key expertise, skills, and requirements the job demands (flat list).")
    keyword_tiers: KeywordTiers = Field(
        description=(
            "Keywords classified into three priority tiers for precise resume tailoring. "
            "Tier 1 = must-have hard skills, Tier 2 = preferred soft skills/methodologies, "
            "Tier 3 = culture/bonus language."
        )
    )
    job_duties_and_responsibilities: List[str] = Field(description="Focus on essential functions, their frequency and importance, level of decision-making, areas of accountability, and any supervisory responsibilities.")
    required_qualifications: List[str] = Field(description="Including education, minimum experience, specific knowledge, skills, abilities, and any required licenses or certifications.")
    preferred_qualifications: List[str] = Field(description="Additional \"nice-to-have\" qualifications that could set a candidate apart.")
    company_name: str = Field(description="The name of the hiring organization.")
    company_details: str = Field(description="Overview, mission, values, or way of working that could be relevant for tailoring a resume or cover letter.")