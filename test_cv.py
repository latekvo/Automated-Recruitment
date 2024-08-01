from core.cv_extractors import extract_entire_cv
from core.cv_structures import ClassifiedChunkList
from core.cv_tools import read_cv_from_path, classify_cv_chunks, coagulate_cv_chunks


# read CV
raw_cv = read_cv_from_path("static/senior-software-developer.pdf")

# print("\n\n".join([str(el) for el in raw_cv]))
#
# classified_cv_chunks: ClassifiedChunkList = classify_cv_chunks(raw_cv)
#
# print("--- CLASSIFIED LINES ---")
# for chunk in classified_cv_chunks:
#     print(chunk[0], "|", chunk[1])
#
# coagulated_cv_chunks: ClassifiedChunkList = coagulate_cv_chunks(classified_cv_chunks)
#
# print("--- COAGULATED LINES ---")
# for chunk in coagulated_cv_chunks:
#     print(chunk[0], "|", chunk[1])

print(extract_entire_cv(raw_cv))
