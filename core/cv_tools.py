from __future__ import annotations

from warnings import deprecated

from langchain_core.pydantic_v1 import BaseModel, Field

from unstructured.partition.auto import partition
from unstructured.partition.utils.constants import PartitionStrategy
from unstructured.cleaners.core import group_broken_paragraphs
from unstructured.cleaners.core import clean

from core.cv_extractors import (
    extract_education,
    extract_commercial_experience,
    extract_private_experience,
    extract_searchable_data,
    extract_social_profiles,
    extract_websites,
)
from core.cv_structures import (
    StructuredCV,
    ClassifiedChunkList,
    classification_prompt,
)
from core.llm_loader import get_llm
from core.utils import ensure_workflow_output


def read_cv_from_path(cv_path: str) -> list[str]:
    # convert cv into raw chunks of text
    elements = partition(
        filename=cv_path,
        content_type="application/pdf",
        strategy=PartitionStrategy.HI_RES,
        paragraph_grouper=group_broken_paragraphs,
    )

    clean_elements = [
        clean(
            str(e),
            extra_whitespace=True,
            dashes=True,
            bullets=True,
            trailing_punctuation=True,
            lowercase=True,
        )
        for e in elements
    ]

    return clean_elements


class DeterminedClassification(BaseModel):
    """Classification of a chunks into CV categories."""

    category: str = Field(
        description=(
            "The CV category to which the text belongs. "
            "If provided text intersects 2 categories, select the first one."
        ),
        required=False,  # couldn't determine and that's normal
        default=None,
    )
    second_category: str = Field(
        description=(
            "When 2 categories appear to be present in provided chunk of text, select the second one. "
            "Otherwise, leave empty. "
        ),
        required=False,
        default=None,
    )


@deprecated("This function has been deprecated, use extract_cv_entries() instead.")
def classify_chunk(text: str) -> DeterminedClassification:
    # check if chunk of text is a header or not
    classification_llm = get_llm()
    structured_llm = classification_llm.with_structured_output(DeterminedClassification)
    workflow = classification_prompt | structured_llm
    return ensure_workflow_output(workflow, {"data": text})


@deprecated("This function has been deprecated, use extract_cv_entries() instead.")
def classify_cv_chunks(
    text_chunks: list[str],
) -> ClassifiedChunkList:
    # group extracted CV slices into labeled fragments
    # FIXME [!!!]: after running this once, we need a much more efficient approach
    # took over an hour so far for one CV and still hasn't finished
    # approaches from fastest to slowest, accuracy inversely proportional:
    # - one pass extraction of everything
    # - extract every category aspect every pass
    # - identify section positions in one pass, the extract each section individually
    # the last approach looks the best, we can number every single line and then ask one ai for ranges
    # this wouldn't require restructuring the rest of my code

    grouped_chunks: list[list[str]] = [[]]
    chunk_grouping_amount = 5

    # regroup all chunks into larger segments,
    # single entry frequently spans across multiple lines
    for chunk in text_chunks:
        if len(grouped_chunks[-1]) >= chunk_grouping_amount:
            grouped_chunks.append([])

        grouped_chunks[-1].append(chunk)

    classified_chunks: ClassifiedChunkList = []

    for grouped_chunk in grouped_chunks:
        print(
            f"classification progress: {len(classified_chunks)}/{len(grouped_chunks)*chunk_grouping_amount}"
        )
        classification = classify_chunk("\n".join(grouped_chunk))

        # no classification
        if classification.category is None:
            continue

        # simple classification
        if classification.second_category is None:
            for chunk in grouped_chunk:
                classified_chunks.append([classification.category, chunk])

        # double-category, classify each line individually
        chunk_iterator = 0
        for chunk in grouped_chunk:
            sub_classification = classify_chunk(chunk)
            category = sub_classification.category

            # if category couldn't be found,
            # classify it as the closest primary category
            if category is None:
                if chunk_iterator < chunk_grouping_amount / 2:
                    category = classification.category
                else:
                    category = classification.second_category

            classified_chunks.append([category, chunk])
            chunk_iterator += 1

            continue

    return classified_chunks


@deprecated("This function has been deprecated, use extract_cv_entries() instead.")
def coagulate_cv_chunks(classified_chunks: ClassifiedChunkList) -> ClassifiedChunkList:
    coagulated_list: ClassifiedChunkList = []
    previous_classification = None

    for chunk in classified_chunks:
        if chunk[0] != previous_classification:
            coagulated_list.append([chunk[0], ""])
            previous_classification = chunk[0]
        coagulated_list[-1][1] += chunk[1]

    return coagulated_list


# Splitting approaches:
# - divide cv into entries, ask AI what kind of entry it is, they'll usually be grouped closely
# - divide cv into sections, then feed entire sections to AI


@deprecated("This function has been deprecated, use extract_cv_entries() instead.")
def process_cv(cv_path: str) -> StructuredCV:
    extracted_cv = StructuredCV()

    raw_cv_chunks = read_cv_from_path(cv_path)
    grouped_chunks = classify_cv_chunks(raw_cv_chunks)
    for chunk in grouped_chunks:
        section, text = chunk

        if section == "work":
            extracted_cv.commercial_experience += extract_commercial_experience(text)
        if section == "project":
            extracted_cv.private_experience += extract_private_experience(text)
        if section == "education":
            extracted_cv.degrees += extract_education(text)
        if section == "socials":
            extracted_cv.socials += extract_social_profiles(text)
        if section == "websites":
            extracted_cv.websites += extract_websites(text)
        if section == "other_poi":
            extracted_cv.other_poi += extract_searchable_data(text)

    return extracted_cv
