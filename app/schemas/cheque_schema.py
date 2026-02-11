from pydantic import BaseModel, Field
from typing import List


class CompanyCheque(BaseModel):
    cheque_number: str = Field(..., description="Cheque number")
    payee_name: str = Field(..., description="Person or company receiving payment")
    amount: float = Field(..., description="Cheque amount")
    issue_date: str = Field(..., description="Cheque issue date")


class CompanyChequeList(BaseModel):
    cheques: List[CompanyCheque]


class BankCheque(BaseModel):
    cheque_number: str = Field(..., description="Cheque number")
    clearing_date: str = Field(..., description="Date cheque was cleared")
    amount: float = Field(..., description="Cleared amount")


class BankChequeList(BaseModel):
    cashed_cheques: List[BankCheque]
