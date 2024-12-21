from typing import List, Dict, Any  # Import Dict and Any for delete response
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.config.database import get_session
from app.controllers import expense_controller
from app.schemas.expense import ExpenseCreate, ExpenseInDB, ExpenseUpdate
from app.auth.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/expenses",
    tags=["expenses"]  # Tags for Swagger documentation
)

@router.get(
    "/",
    response_model=List[ExpenseInDB],
    summary="List all expenses for the current user"
)
def read_expenses(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves all expenses belonging to the currently authenticated user.
    """
    return expense_controller.get_expenses(session, current_user)

@router.post(
    "/",
    response_model=ExpenseInDB,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new expense"
)
def create_expense(
    expense: ExpenseCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Creates a new expense for the currently authenticated user.
    """
    return expense_controller.create_expense(session, expense, current_user)

@router.put(
    "/{expense_id}",
    response_model=ExpenseInDB,
    summary="Update an existing expense"
)
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Updates an existing expense if it belongs to the currently authenticated user.
    """
    return expense_controller.update_expense(session, expense_id, expense, current_user)

@router.delete(
    "/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an expense"
)
def delete_expense(
    expense_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Deletes an expense if it belongs to the currently authenticated user.
    """
    expense_controller.delete_expense(session, expense_id, current_user)
    return  # Returning nothing as per HTTP 204 No Content

@router.get(
    "/category/{category}",
    response_model=List[ExpenseInDB],
    summary="List expenses by category"
)
def get_expense_by_category(
    category: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieves expenses of a specific category belonging to the currently authenticated user.
    """
    return expense_controller.get_expenses_by_category(session, category, current_user)

# ### New Endpoints for Bulk Update and Delete by Category ###

@router.put(
    "/category/{category}",
    response_model=List[ExpenseInDB],
    summary="Update all expenses in a specific category"
)
def update_expenses_by_category(
    category: str,
    expense_update: ExpenseUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Updates all expenses under a specific category for the currently authenticated user.
    """
    return expense_controller.update_expenses_by_category(
        session=session,
        category=category,
        expense_update=expense_update,
        current_user=current_user
    )

@router.delete(
    "/category/{category}",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Any],
    summary="Delete all expenses in a specific category"
)
def delete_expenses_by_category(
    category: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Deletes all expenses under a specific category for the currently authenticated user.
    """
    return expense_controller.delete_expenses_by_category(
        session=session,
        category=category,
        current_user=current_user
    )
