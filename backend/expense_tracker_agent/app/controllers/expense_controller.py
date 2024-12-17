import logging
from typing import List
from sqlmodel import Session, select, and_
from fastapi import HTTPException, status, Depends

from app.models.expense import Expense
from ..schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseInDB
from app.auth.auth import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def get_expenses(session: Session, current_user: User = Depends(get_current_user)) -> List[ExpenseInDB]:
    expenses = session.exec(select(Expense).where(Expense.user_id == current_user.id)).all()
    return [ExpenseInDB.from_orm(expense) for expense in expenses]

def create_expense(session: Session, expense_data: ExpenseCreate, current_user: User = Depends(get_current_user)) -> ExpenseInDB:
    try:
        db_expense = Expense(**expense_data.dict())
        db_expense.user_id = current_user.id  # Important: Assign user ID
        session.add(db_expense)
        session.commit()
        session.refresh(db_expense)
        return ExpenseInDB.from_orm(db_expense)
    except Exception as e:
        logger.error(f"Error creating expense: {e}")
        session.rollback()  # Rollback on error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to create expense: {e}")

def update_expense(session: Session, expense_id: int, expense: ExpenseUpdate, current_user: User = Depends(get_current_user)) -> ExpenseInDB:
    db_expense = session.get(Expense, expense_id)
    if not db_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    if db_expense.user_id != current_user.id: # Check ownership
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this expense")

    expense_data = expense.dict(exclude_unset=True)
    for key, value in expense_data.items():
        setattr(db_expense, key, value)
    session.add(db_expense)
    session.commit()
    session.refresh(db_expense)
    return ExpenseInDB.from_orm(db_expense)

def delete_expense(session: Session, expense_id: int, current_user: User = Depends(get_current_user)):
    expense = session.get(Expense, expense_id)
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    if expense.user_id != current_user.id: # Check ownership
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this expense")
    session.delete(expense)
    session.commit()
    return {"message": "Expense deleted"}

def get_expenses_by_category(session: Session, category: str, current_user: User = Depends(get_current_user)) -> List[ExpenseInDB]:
    statement = select(Expense).where(and_(Expense.category == category, Expense.user_id == current_user.id))
    expenses = session.exec(statement).all()
    return [ExpenseInDB.from_orm(expense) for expense in expenses]