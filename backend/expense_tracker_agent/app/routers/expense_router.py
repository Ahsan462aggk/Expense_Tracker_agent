from typing import List # Import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.config.database import get_session
from app.controllers import expense_controller
from app.schemas.expense import ExpenseCreate, ExpenseInDB, ExpenseUpdate
from app.auth.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/expenses", tags=["expenses"]) # Add prefix and tags

@router.get("/", response_model=List[ExpenseInDB], summary="List all expenses for the current user") # Add summary
def read_expenses(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """Retrieves all expenses belonging to the currently authenticated user."""
    return expense_controller.get_expenses(session, current_user)

@router.post("/", response_model=ExpenseInDB, status_code=status.HTTP_201_CREATED, summary="Create a new expense") # Add summary
def create_expense(expense: ExpenseCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """Creates a new expense for the currently authenticated user."""
    return expense_controller.create_expense(session, expense, current_user)

@router.put("/{expense_id}", response_model=ExpenseInDB, summary="Update an existing expense") # Add summary
def update_expense(expense_id: int, expense: ExpenseUpdate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """Updates an existing expense if it belongs to the currently authenticated user."""
    return expense_controller.update_expense(session, expense_id, expense, current_user)

@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an expense") # Add summary and correct status code
def delete_expense(expense_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """Deletes an expense if it belongs to the currently authenticated user."""
    expense_controller.delete_expense(session, expense_id, current_user) # Don't return anything on delete
    return

@router.get("/category/{category}", response_model=List[ExpenseInDB], summary="List expenses by category") # Add summary
def get_expense_by_category(category: str, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """Retrieves expenses of a specific category belonging to the currently authenticated user."""
    return expense_controller.get_expenses_by_category(session, category, current_user)