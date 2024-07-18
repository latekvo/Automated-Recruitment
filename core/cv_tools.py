from unstructured.partition.auto import partition
from unstructured.partition.utils.constants import PartitionStrategy


def read_cv_from_file():
    # convert cv into a well-structured text blob
    pass


def read_cv_from_path(cv_path):
    # convert cv into a well-structured document
    elements = partition(
        filename=cv_path,
        content_type="application/pdf",
        strategy=PartitionStrategy.OCR_ONLY,
    )
    print("\n\n".join([str(el) for el in elements]))


def split_cv():
    # extract all the covered points of interest and store them in a single blob
    pass


def section_classifier():
    # classify what kind of section the provided chunk of text is
    # input can be either education, project, experience etc
    pass
