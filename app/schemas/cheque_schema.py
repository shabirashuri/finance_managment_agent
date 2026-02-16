from pydantic import BaseModel, Field
from typing import List, Optional


class CompanyCheque(BaseModel):
    cheque_number: Optional[str] = Field(None, description="Cheque number")
    payee_name: Optional[str] = Field(None, description="Person or company receiving payment")
    amount: Optional[float] = Field(None, description="Cheque amount")
    issue_date: Optional[str] = Field(None, description="Cheque issue date")


class CompanyChequeList(BaseModel):
    cheques: List[CompanyCheque]


class BankCheque(BaseModel):
    cheque_number: Optional[str] = Field(None, description="Cheque number")
    clearing_date: Optional[str] = Field(None, description="Date cheque was cleared")
    amount: Optional[float] = Field(None, description="Cleared amount")


class BankChequeList(BaseModel):
    cashed_cheques: List[BankCheque]
