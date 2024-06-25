import __future__
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

general_summary_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an HR assistant."
            "Your job is to create a general summary of most important job interview points."
            "Use provided job interview transcript to summarize the candidate to the best of your ability."
            "Provide dense description of candidate's abilities, knowledge nad suitability for a job."
            "DO NOT BELIEVE WHAT THE CANDIDATE SAYS AT FACE VALUE, instead, evaluate him based on his monologue."
            "Candidate must provide a meaningful trasncript which is long enough to draw conclusions from it.",
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


llm = Ollama(model="mistral:7b-instruct-q4_K_S")
output_parser = StrOutputParser()


# pass {"transcript": str} when invoking
general_chain = general_summary_prompt | llm | output_parser


def generate_general_summary(question: str, transcript: str):
    return general_chain.invoke(
        {
            "question": question,
            "transcript": transcript,
        }
    )
