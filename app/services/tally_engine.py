from typing import Dict, List


def tally_cheques(company_data, bank_data) -> Dict:

    company_cheques = company_data.cheques
    bank_cheques = bank_data.cashed_cheques

    bank_lookup = {c.cheque_number: c for c in bank_cheques}

    cashed = []
    pending = []
    mismatched = []

    total_issued_amount = 0
    total_cashed_amount = 0
    total_pending_amount = 0

    for cheque in company_cheques:
        total_issued_amount += cheque.amount

        bank_match = bank_lookup.get(cheque.cheque_number)

        if bank_match:

            if abs(bank_match.amount - cheque.amount) > 0.01:
                mismatched.append({
                    "cheque_number": cheque.cheque_number,
                    "issued_amount": cheque.amount,
                    "bank_amount": bank_match.amount
                })
            else:
                cashed.append({
                    "cheque_number": cheque.cheque_number,
                    "payee_name": cheque.payee_name,
                    "amount": cheque.amount,
                    "issue_date": cheque.issue_date,
                    "clearing_date": bank_match.clearing_date
                })

                total_cashed_amount += cheque.amount
        else:
            pending.append({
                "cheque_number": cheque.cheque_number,
                "payee_name": cheque.payee_name,
                "amount": cheque.amount,
                "issue_date": cheque.issue_date
            })

            total_pending_amount += cheque.amount

    result = {
        "summary": {
            "total_issued": len(company_cheques),
            "total_cashed": len(cashed),
            "total_pending": len(pending),
            "total_mismatched": len(mismatched),
            "amount_issued": round(total_issued_amount, 2),
            "amount_cashed": round(total_cashed_amount, 2),
            "amount_pending": round(total_pending_amount, 2),
        },
        "cashed": cashed,
        "pending": pending,
        "mismatched_amount": mismatched
    }

    return result
