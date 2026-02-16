from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from app.services.llm_service import get_llm
from app.schemas.cheque_schema import (
    CompanyChequeList,
    BankChequeList
)
import logging

logger = logging.getLogger(__name__)


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

    logger.info(f"Company extraction - Raw result: {len(result.cheques)} cheques extracted")
    logger.debug(f"Company raw cheques: {result.cheques}")
    
    # Filter incomplete cheques - only require critical fields
    original_count = len(result.cheques)
    result.cheques = [
        c for c in result.cheques
        if c.cheque_number and c.amount  # Only require cheque number and amount
    ]
    
    filtered_count = original_count - len(result.cheques)
    if filtered_count > 0:
        logger.warning(f"Company extraction - Filtered out {filtered_count} incomplete cheques")
    logger.info(f"Company extraction - Final result: {len(result.cheques)} valid cheques")

    return result


def extract_bank_cheques(raw_text: str):

    parser = PydanticOutputParser(pydantic_object=BankChequeList)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a banking document expert. "
            "Extract only cleared cheque details from the bank statement. "
            "Ignore unrelated transactions."
            "Also instno refers to cheque number so if instno is shown that means it is cheque no"
            """Do not include empty objects.
            Only include fully populated cheque entries.
            If no cheque data exists, return an empty list."""
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

    logger.info(f"Bank extraction - Raw result: {len(result.cashed_cheques)} cheques extracted")
    logger.debug(f"Bank raw cheques: {result.cashed_cheques}")
    
    # Filter incomplete bank cheques
    original_count = len(result.cashed_cheques)
    result.cashed_cheques = [
        c for c in result.cashed_cheques
        if c.cheque_number and c.clearing_date and c.amount
    ]
    
    filtered_count = original_count - len(result.cashed_cheques)
    if filtered_count > 0:
        logger.warning(f"Bank extraction - Filtered out {filtered_count} incomplete cheques")
    logger.info(f"Bank extraction - Final result: {len(result.cashed_cheques)} valid cheques")

    return result