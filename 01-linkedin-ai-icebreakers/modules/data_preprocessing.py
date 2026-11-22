"""Module for processing LinkedIn profile data.
we are making personal,employment,education,certification etc information,
into separate llama index Document object so that we preserve the context before we split into nodes,
instead of combining everything together"""

import logging
from typing import Dict, List, Any, Optional

from llama_index.core import Document, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter

from modules.llm_interface import create_openai_embedding
import config

logger = logging.getLogger(__name__)


def normalize_harvestapi_profile(raw_profile):
    """Convert HarvestAPI profile data into the existing standard schema."""

    full_name=" ".join(part for part in[raw_profile.get("firstName",""),raw_profile.get("lastName","")] if part)

    # Normalize experience records
    position_groups = []
    for experience in raw_profile.get("experience", []):
        start_date = experience.get("startDate") or {}
        end_date = experience.get("endDate") or {}

        position_groups.append({
            "company": {
                "name": experience.get("companyName", "")
            },
            "profile_positions": [{
                "title": experience.get("position", ""),
                "employment_type": experience.get("employmentType", ""),
                "location": experience.get("location", ""),
                "description": experience.get("description", ""),
                "date": {
                    "start": start_date.get("text", ""),
                    "end": end_date.get("text", "")
                }
            }]
        })

    # Normalize education records
    educations = []

    for education in raw_profile.get("education", []):
        start_date = education.get("startDate") or {}
        end_date = education.get("endDate") or {}

        educations.append({
            "school": {
                "name": education.get("schoolName", "")
            },
            "degree_name": education.get("degree", ""),
            "field_of_study": education.get("fieldOfStudy", ""),
            "date": {
                "start": start_date.get("text", ""),
                "end": end_date.get("text", "")
            }
        })

    # Normalize skills
    skills = [
        skill.get("name", "")
        for skill in raw_profile.get("skills", [])
        if skill.get("name")
    ]

    # Normalize certifications
    certifications = [
        {
            "name": cert.get("title", ""),
            "authority": cert.get("issuedBy", "")
        }
        for cert in raw_profile.get("certifications", [])
    ]

    location = raw_profile.get("location") or {}

    return {
        "full_name": full_name,
        "title": raw_profile.get("headline", ""),
        "headline": raw_profile.get("headline", ""),
        "summary": raw_profile.get("about", ""),
        "industry": "",
        "location": {
            "default": location.get("linkedinText", "")
        },
        "position_groups": position_groups,
        "educations": educations,
        "skills": skills,
        "certifications": certifications
    }




def split_profile_data(
    profile_data: Dict[str, Any]
) -> List:

    try:
        documents = []

        # Personal information
        personal_info = [
            f"Name: {profile_data.get('full_name', '')}",
            f"Title: {profile_data.get('title', '')}",
            f"Headline: {profile_data.get('headline', '')}",
            f"Summary: {profile_data.get('summary', '')}",
            f"Industry: {profile_data.get('industry', '')}",
            f"Location: {profile_data.get('location', {}).get('default', '')}",
        ]

        personal_text = "\n".join(
            item for item in personal_info
            if item.split(": ", 1)[-1].strip()
        )

        if personal_text:
            documents.append(
                Document(
                    text=personal_text,
                    metadata={"section": "personal"}
                )
            )

        # Employment information
        for group in profile_data.get("position_groups", []):

            company_data = group.get("company", {})
            if isinstance(company_data, dict):
                company = company_data.get("name", "")
            else:
                company = company_data or ""

            for position in group.get("profile_positions", []):

                position_info = [
                    f"Company: {company or position.get('company', '')}",
                    f"Position: {position.get('title', '')}",
                    f"Employment Type: {position.get('employment_type', '')}",
                    f"Location: {position.get('location', '')}",
                    f"Start Date: {position.get('date', {}).get('start', '')}",
                    f"End Date: {position.get('date', {}).get('end', '')}",
                    f"Description: {position.get('description', '')}"
                ]

                experience_text = "\n".join(
                    item for item in position_info
                    if item.split(": ", 1)[-1].strip()
                )

                if experience_text:
                    documents.append(
                        Document(
                            text=experience_text,
                            metadata={
                                "section": "experience",
                                "company": company or position.get("company", ""),
                                "position": position.get("title", "")
                            }
                        )
                    )

        # Education
        for education in profile_data.get("educations", []):

            school = education.get("school", {}).get("name", "")
            dates = education.get("date", {})

            education_info = [
                f"Institution: {school}",
                f"Degree: {education.get('degree_name', '')}",
                f"Field of Study: {education.get('field_of_study', '')}",
                f"Start Date: {dates.get('start', '')}",
                f"End Date: {dates.get('end', '')}"
            ]

            education_text = "\n".join(
                item for item in education_info
                if item.split(": ", 1)[-1].strip()
            )

            if education_text:
                documents.append(
                    Document(
                        text=education_text,
                        metadata={"section": "education"}
                    )
                )

        # Skills
        skills = profile_data.get("skills", [])

        if skills:
            documents.append(
                Document(
                    text="Skills: " + ", ".join(skills),
                    metadata={"section": "skills"}
                )
            )

        # Certifications
        for certification in profile_data.get("certifications", []):

            certification_info = [
                f"Certification: {certification.get('name', '')}",
                f"Issued By: {certification.get('authority', '')}"
            ]

            certification_text = "\n".join(
                item for item in certification_info
                if item.split(": ", 1)[-1].strip()
            )

            if certification_text:
                documents.append(
                    Document(
                        text=certification_text,
                        metadata={"section": "certification"}
                    )
                )

        # Split documents into nodes
        splitter = SentenceSplitter(
            chunk_size=config.CHUNK_SIZE
        )

        nodes = splitter.get_nodes_from_documents(documents)

        logger.info(
            f"Created {len(documents)} documents "
            f"and {len(nodes)} nodes from profile data."
        )

        return nodes

    except Exception:
        logger.exception("Error in split_profile_data")
        raise


def create_vector_database(
    nodes: List
) -> Optional[VectorStoreIndex]:

    try:
        if not nodes:
            raise ValueError("Nodes are needed to create a vector store.")

        embedding_model = create_openai_embedding()

        vector_index = VectorStoreIndex(
            nodes=nodes,
            embed_model=embedding_model,
            show_progress=True
        )

        logger.info("Vector database created successfully.")

        return vector_index

    except Exception:
        logger.exception("Error in create_vector_database")
        return None


    




