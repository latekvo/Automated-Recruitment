from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

sub_summary_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an HR assistant."
            "Your job is to create a general summary of most important job interview points."
            "Use provided job interview transcript to summarize the candidate to the best of your ability."
            "Provide dense description of candidate's abilities, knowledge and suitability for a job."
            "DO NOT BELIEVE WHAT THE CANDIDATE SAYS AT FACE VALUE, instead, evaluate him based on his monologue."
            "Candidate must provide a meaningful transcript which is long enough to draw conclusions from it.",
        ),
        (
            "user",
            "Job interview transcript: "
            "```"
            "Question: {question}"
            "{transcript}"
            "```"
            "Summarize this transcript.",
        ),
    ]
)

general_summary_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a head HR manager."
            "You are given a set of discriptions of a given candidate, your job is to combine them."
            "Use provided descriptions to create a meaningful rapport about the given candidate."
            "Provide dense description of candidate's abilities, knowledge and suitability for a job.",
        ),
        (
            "user",
            "Candidate descriptions: "
            "```"
            "{joined_summaries}"
            "```"
            "Provide dense description of candidate's suitability for the job.",
        ),
    ]
)

llm = Ollama(model="mistral:7b-instruct-q4_K_S")
output_parser = StrOutputParser()

# pass {"transcript": str} when invoking
sub_chain = sub_summary_prompt | llm | output_parser
general_chain = general_summary_prompt | llm | output_parser


def generate_sub_summary(question: str, transcript: str) -> str:
    return sub_chain.invoke(
        {
            "question": question,
            "transcript": transcript,
        }
    )


def summarize_list_of_sub_summaries(summary_list: list[str]):
    joined_summaries = ""
    for summary in summary_list:
        joined_summaries += "\n---\n"
        joined_summaries += summary

    return general_chain.invoke(
        {
            "joined_summaries": joined_summaries,
        }
    )
