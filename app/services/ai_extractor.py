from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from app.services.llm_service import get_llm
from app.schemas.cheque_schema import (
    CompanyChequeList,
    BankChequeList
)


def extract_company_cheques(raw_text: str):

    parser = PydanticOutputParser(pydantic_object=CompanyChequeList)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a financial document extraction expert. "
            "Extract only issued cheque details from the document. "
            "Ignore unrelated data."
        ),
        (
            "human",
            "Extract cheque data from this document:\n\n{document}\n\n{format_instructions}"
        )
    ])

    chain = prompt | get_llm() | parser

    result = chain.invoke({
        "document": raw_text,
        "format_instructions": parser.get_format_instructions()
    })

    return result


def extract_bank_cheques(raw_text: str):

    parser = PydanticOutputParser(pydantic_object=BankChequeList)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a banking document expert. "
            "Extract only cleared cheque details from the bank statement. "
            "Ignore unrelated transactions."
        ),
        (
            "human",
            "Extract cleared cheque data from this bank statement:\n\n{document}\n\n{format_instructions}"
        )
    ])

    chain = prompt | get_llm() | parser

    result = chain.invoke({
        "document": raw_text,
        "format_instructions": parser.get_format_instructions()
    })

    return result
