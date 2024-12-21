# app/agents/agent.py

import os
import sys
import traceback
from dotenv import load_dotenv  # Import python-dotenv
from sqlmodel import Session, select
from app.config.database import get_session, engine
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import SystemMessage as LLMSystemMessage
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.controllers.expense_controller import (
    get_expenses,
    create_expense,
    update_expenses_by_category,
    delete_expenses_by_category,
    get_expenses_by_category
)
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
import arrow

import logging
from app.models.expense import Expense
from app.models.user import User

# Memory Imports
from langchain_core.messages import RemoveMessage
from langgraph.checkpoint.memory import MemorySaver
# Ensure IPython is installed

import contextvars  # Import contextvars

# Define a Context Variable for user_id
current_user_id: contextvars.ContextVar[Optional[int]] = contextvars.ContextVar("current_user_id", default=None)

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure GOOGLE_API_KEY is set
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    logger.error("GOOGLE_API_KEY environment variable is not set.")
    sys.exit(1)

# Optionally, set it in os.environ if required by ChatGoogleGenerativeAI
os.environ["GOOGLE_API_KEY"] = google_api_key

# Initialize LangChain LLM
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.3
    )
    logger.info("Initialized ChatGoogleGenerativeAI LLM.")
except Exception as e:
    logger.error(f"Failed to initialize ChatGoogleGenerativeAI LLM: {e}")
    logger.error(traceback.format_exc())
    sys.exit(1)

# Define Tool Functions
import dateparser  # Ensure dateparser is installed and imported


def tool_get_expenses(
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    description_keyword: Optional[str] = None
) -> str:
    """
    Retrieve expenses from the database, optionally filtered by category, date range,
    and description keyword, and calculate the total amount.

    Additionally, check if a specific or Categories description exists and inform the user accordingly.

    Args:
        category (Optional[str]): The category to filter expenses (e.g., 'Travel').
        start_date (Optional[str]): The start date for filtering expenses (e.g., '1 January').
        end_date (Optional[str]): The end date for filtering expenses (e.g., '25 January').
        description_keyword (Optional[str]): Keyword to filter expenses by description.

    Returns:
        str: A string containing the list of expenses and the total amount in plain text.
    """
    user_id = current_user_id.get()
    if not user_id:
        logger.error("User ID is not set in the context.")
        return "Error: User ID is missing."

    try:
        # Parse the date strings into datetime objects
        parsed_start_date = dateparser.parse(start_date) if start_date else None
        parsed_end_date = dateparser.parse(end_date) if end_date else None

        # Validate date parsing
        if start_date and not parsed_start_date:
            logger.error(f"Failed to parse start_date: {start_date}")
            return f"Error: Unable to parse the start date '{start_date}'. Please use a valid date format."

        if end_date and not parsed_end_date:
            logger.error(f"Failed to parse end_date: {end_date}")
            return f"Error: Unable to parse the end date '{end_date}'. Please use a valid date format."

        # Ensure start_date is not after end_date
        if parsed_start_date and parsed_end_date and parsed_start_date > parsed_end_date:
            logger.error("Start date cannot be after end date.")
            return "Error: Start date cannot be after end date."

        with Session(engine) as session:
            # Fetch the User object based on user_id
            current_user = session.get(User, user_id)
            if not current_user:
                logger.error(f"User with ID {user_id} not found.")
                return "Error: User not found."

            # Start building the query
            statement = select(Expense).where(Expense.user_id == user_id)
            filters = []

            # Apply category filter if provided
            if category:
                filters.append(Expense.category.ilike(f"%{category}%"))
                logger.debug(f"Applying category filter: {category}")
            # Apply description keyword filter if provided
            if description_keyword:
                filters.append(Expense.description.ilike(f"%{description_keyword}%"))
                logger.debug(f"Applying description keyword filter: {description_keyword}")
            # Apply date range filters if provided
            if parsed_start_date and parsed_end_date:
                filters.append(Expense.date.between(parsed_start_date, parsed_end_date))
                logger.debug(f"Applying date range filter: {parsed_start_date} to {parsed_end_date}")
            elif parsed_start_date:
                filters.append(Expense.date >= parsed_start_date)
                logger.debug(f"Applying start date filter: {parsed_start_date}")
            elif parsed_end_date:
                filters.append(Expense.date <= parsed_end_date)
                logger.debug(f"Applying end date filter: {parsed_end_date}")

            # Combine all filters
            if filters:
                statement = statement.where(*filters)

            # Execute the query and retrieve expenses
            expenses = session.exec(statement).all()
            logger.debug(f"Retrieved expenses with filters - Category: '{category}', Start Date: '{parsed_start_date}', End Date: '{parsed_end_date}': {expenses}")

            # Calculate total amount
            total_amount = sum(expense.amount for expense in expenses) if expenses else 0

            # Format expenses into a human-readable string
            if expenses:
                expenses_str = "\n".join([
                    f"ID: {expense.id} | Description: {expense.description} | "
                    f"Amount: ${expense.amount:.2f} | Category: {expense.category} | "
                    f"User ID: {expense.user_id} | Date: {expense.date.strftime('%Y-%m-%d') if expense.date else 'N/A'}"
                    for expense in expenses
                ])
                response = f"Here are your expenses for \"{category}\":\n{expenses_str}\n\nTotal: ${total_amount:.2f}"
            else:
                response = "No expenses found with the specified criteria."

        return response

    except Exception as e:
        logger.error(f"Error in tool_get_expenses: {e}")
        logger.error(traceback.format_exc())
        return f"Error retrieving expenses: {str(e)}"


def tool_create_expenses(amount: float, category: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new expense entry in the database.

    Args:
        amount (float): The monetary amount of the expense.
        category (str): The category for the expense.
        description (Optional[str]): An optional brief description of the expense.

    Returns:
        Dict[str, Any]: A dictionary containing the details of the created expense.
                        Returns an error message dictionary if an exception occurs.
    """
    user_id = current_user_id.get()
    if not user_id:
        logger.error("User ID is not set in the context.")
        return {"status": "error", "message": "User ID is missing."}

    try:
        # Add the current date to the expense data
        current_date = datetime.now()

        expense_data = ExpenseCreate(
            description=description,
            amount=amount,
            user_id=user_id,
            category=category,
            date=current_date  # Make sure to include the date field
        )

        with Session(engine) as session:
            db_expense = Expense(**expense_data.dict())  # Create an Expense instance
            session.add(db_expense)
            session.commit()
            session.refresh(db_expense)

        logger.info(f"Created expense: {db_expense}")
        return {
            "status": "success",
            "message": "Expense stored successfully.",
            "data": db_expense.dict()  # Return the created expense data
        }

    except Exception as e:
        logger.error(f"Error in tool_create_expenses: {e}")
        logger.error(traceback.format_exc())
        return {"status": "error", "message": str(e)}


def tool_update_expenses(
    category: str,
    description: Optional[str] = None,
    amount: Optional[float] = None,
    date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update all expenses under a specific category for the current user.

    Args:
        category (str): The category whose expenses need to be updated.
        description (Optional[str]): The new description for the expense.
        amount (Optional[float]): The new amount for the expense.
        date (Optional[str]): The new date for the expense.

    Returns:
        Dict[str, Any]: A dictionary containing the details of the updated expenses.
                        Returns an error message dictionary if an exception occurs.
    """
    user_id = current_user_id.get()
    if not user_id:
        logger.error("User ID is not set in the context.")
        return {"status": "error", "message": "User ID is missing."}

    try:
        if date:
            # Parse the provided date and adjust it as needed
            parsed_date = dateparser.parse(date)
            if not parsed_date:
                logger.error(f"Failed to parse date: {date}")
                return {"status": "error", "message": f"Unable to parse the date '{date}'."}
            # Format the date as needed, e.g., ISO format
            formatted_date = parsed_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            formatted_date = None

        # Initialize ExpenseUpdate without the 'id' field
        expense_update = ExpenseUpdate(
            description=description,
            amount=amount,
            category=category,
            date=formatted_date
        )

        with Session(engine) as session:
            # Fetch the User object based on user_id
            current_user = session.get(User, user_id)
            if not current_user:
                logger.error(f"User with ID {user_id} not found.")
                return {"status": "error", "message": "User not found."}

            updated_expenses = update_expenses_by_category(session, category, expense_update, current_user)
            logger.debug(f"Updated expenses in category '{category}': {updated_expenses}")

        return {
            "status": "success",
            "message": f"Updated {len(updated_expenses)} expenses in category '{category}'.",
            "data": [expense.dict() for expense in updated_expenses]
        }
    except HTTPException as he:
        logger.error(f"HTTP error in tool_update_expenses: {he.detail}")
        return {"status": "error", "message": he.detail}
    except Exception as e:
        logger.error(f"Error in tool_update_expenses: {e}")
        logger.error(traceback.format_exc())
        return {"status": "error", "message": str(e)}


def tool_delete_expenses(category: str) -> Dict[str, Any]:
    """
    Delete all expenses belonging to a specific category.

    Args:
        category (str): The category name whose expenses need to be deleted.

    Returns:
        Dict[str, Any]: A dictionary confirming the deletion of expenses in the specified category.
                        Returns an error message dictionary if an exception occurs.
    """
    user_id = current_user_id.get()
    if not user_id:
        logger.error("User ID is not set in the context.")
        return {"status": "error", "message": "User ID is missing."}

    try:
        with Session(engine) as session:
            # Fetch the User object based on user_id
            current_user = session.get(User, user_id)
            if not current_user:
                logger.error(f"User with ID {user_id} not found.")
                return {"status": "error", "message": "User not found."}

            deletion_result = delete_expenses_by_category(session, category, current_user)
            logger.debug(f"Deletion result for category '{category}': {deletion_result}")

        return {
            "status": "success",
            "message": deletion_result["message"]
        }
    except HTTPException as he:
        logger.error(f"HTTP error in tool_delete_expenses: {he.detail}")
        return {"status": "error", "message": he.detail}
    except Exception as e:
        logger.error(f"Error in tool_delete_expenses: {e}")
        logger.error(traceback.format_exc())
        return {"status": "error", "message": str(e)}


# Define Tools List Directly Without Using LangChain's Tool Class
tools = [
    tool_get_expenses,
    tool_create_expenses,
    tool_update_expenses,
    tool_delete_expenses
]

logger.info(f"Defined {len(tools)} tools.")

# Bind Tools to the LLM
try:
    llm_with_tools = llm.bind_tools(tools)
    logger.info("Bound tools to the LLM.")
except Exception as e:
    logger.error(f"Failed to bind tools to the LLM: {e}")
    logger.error(traceback.format_exc())
    sys.exit(1)

# Define System Message
sys_msg = LLMSystemMessage(content="""
You are a financial assistant that helps users manage their expenses. Your capabilities include:

1. **Create Expense:** Add a new expense with description, amount, and category. The user ID is retrieved from the human message parameter.
2. **View Expenses:** Retrieve and display all expenses, optionally filtered by category and/or date range.
3. **Update Expense:** Modify an expense's category, amount, user ID, or date using the category as a reference.
   - **Two-Step Update Process:** 
     1. **Verification:** First, verify the existence of the expense in the specified category using the **View Expenses** capability.
     2. **Update Execution:** 
        - **Important Instructions:** 
          - Before updating an expense, you **must** retrieve all necessary details (such as `description`, `id`, `date`, `user_id`, and `category`) from the retrieved expense.
          - **Pass the `description`, `id`, `date`, `category`, and `user_id` along with the new `amount` as arguments to the `tool_update_expenses`.** Failing to pass all required fields will result in a validation error.
          - The `amount` should always be updated with the new value provided by the user.

**User ID Extraction:**
You are an assistant that extracts the `user_id` from a message structure. 
Given a message formatted as follows:
[HumanMessage(content='yes', additional_kwargs={}, response_metadata={}, user_id=<USER_ID>)]
or similar variations, please extract and return only the `user_id` as an integer, regardless of its value.

**Guidelines:**
- **Clarity:** Provide clear and concise responses.
- **Confirmation:** Confirm actions taken (e.g., "Expense added successfully.").
- **Formatting:** Present data in a readable format.
- **Graceful Handling:** Manage invalid requests gracefully (e.g., "No expenses found for category 'Travel'.").
- **Partial Updates:** When updating, only modify fields specified by the user, leaving other fields unchanged.
- **Date Handling:** Allow users to specify date ranges in natural language (e.g., "from 1 January to 25 January").
- **Implicit Intent Detection:** Identify and handle indirect mentions of expenses, such as purchases, costs, budgeting, or saving.
- **Two-Step Update Process:** When an update is requested, first verify the existence of the expense using the **View Expenses** capability before performing the update.

**Examples:**
1. **User:** Create an expense for groceries costing $50.
   **Assistant:** Expense for groceries costing $50 has been added successfully.

2. **User:** Show me all my Travel expenses.
   **Assistant:** Here are your expenses for "Travel":
   - ID: 3 | Description: Flight to NYC | Amount: $200.00 | Category: Travel | User ID: 1 | Date: 2024-11-15
   - ID: 4 | Description: Taxi from airport | Amount: $50.00 | Category: Travel | User ID: 1 | Date: 2024-11-15

     Total: $250.00

3. **User:** Show me all my expenses from January 1, 2024, to January 31, 2024.
   **Assistant:** Here are your expenses from 2024-01-01 to 2024-01-31:
   - ID: 1 | Description: Groceries | Amount: $50.00 | Category: Food | User ID: 1 | Date: 2024-01-05
   - ID: 2 | Description: Utilities | Amount: $100.00 | Category: Bills | User ID: 1 | Date: 2024-01-10

     Total: $150.00

4. **User:** Update all Travel expenses to $200.
   **Assistant:** Updated all expenses in the "Travel" category to $200 successfully.

5. **User:** Delete all expenses related to Travel.
   **Assistant:** All expenses in the "Travel" category have been deleted successfully.

6. When a user provides an input like "I just bought a new bike for $900," recognize the implicit intent to create an expense.
   If the user confirms ("Yes"), extract the following details using its intelligence:
   - **Description:** Use contextual keywords to derive a meaningful description (e.g., "New bike").
   - **Amount:** Parse and extract the numerical value from the user's input (e.g., "$900").
   - **Category:** Based on the description or context, automatically infer an appropriate category (e.g., "Transportation").
   Proceed to create the expense with the extracted details and confirm the action.

7. **User:** My latest gadget cost me around $300.
   **Assistant:** Noted! Should I log this gadget expense for you?

8. **User:** I need to keep track of my spending this month.
   **Assistant:** Sure! Would you like to review your current expenses or add a new one?

9. **User:** Managed to spend less on dining out this week.
   **Assistant:** Congratulations on saving! Do you want to update your expense records accordingly?

10. **User:** I spent $200 on concert tickets.
    **Assistant:** Would you like me to add this concert tickets expense to your records?

11. **User:** What is the cost of my shoes?
    **Assistant:** Here are your expenses for "Shoes":
    - ID: 5 | Description: Running Shoes | Amount: $120.00 | Category: Shoes | User ID: 2 | Date: 2024-12-01

      Total: $120.00.

12. **User:** What is the total of all my expenses?
    **Assistant:** Your total expenses amount to $720.00.

13. **User:** What is the total cost of my Food and Travel categories?
    **Assistant:** Here are the total costs for your specified categories:
    - Food: $150.00
    - Travel: $250.00

      Combined Total: $400.00

14. **User:** Update my shoes expense from $300 to $400.
    **Assistant:** Found the following expenses for "shoes":
    - ID: 4 | Description: White shoes | Amount: $300.00 | Category: Shoes | User ID: 1 | Date: 2024-12-05

      Updating the amount to $400.00.

      Expense updated successfully.
""")


# Define Assistant Node
from langgraph.graph import MessagesState
from typing import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages, AnyMessage


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    summary: str


def assistant(state: State) -> State:
    """
    The main assistant function that processes incoming messages,
    invokes the LLM with the bound tools, and returns the updated state.

    Args:
        state (State): The current state containing messages and summary.

    Returns:
        State: The updated state with new messages.
    """
    # Get summary if it exists
    summary = state.get("summary", "")

    # If there is summary, then we add it
    if summary:
        # Add summary to system message
        system_message = f"Summary of conversation earlier: {summary}\n\n{sys_msg.content}"

        # Append summary to any newer messages
        messages = [SystemMessage(content=system_message)] + state["messages"]
    else:
        messages = [sys_msg] + state["messages"]

    response = llm_with_tools.invoke(messages)
    return {"messages": response}


# Memory Functions
def summarize_conversation(state: State):
    """
    Summarizes the conversation when it exceeds a certain length to maintain context.

    Args:
        state (State): The current state containing messages and summary.

    Returns:
        Dict[str, Any]: Updated state with the new summary and pruned messages.
    """
    # First, we get any existing summary
    summary = state.get("summary", "")

    # Create our summarization prompt
    if summary:
        # A summary already exists
        summary_message = (
            f"This is summary of the conversation to date: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )
    else:
        summary_message = "Create a summary of the conversation above:"

    # Add prompt to our history
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = llm_with_tools.invoke(messages)

    # Delete all but the 2 most recent messages
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary": response.content, "messages": delete_messages}


def should_continue(state: State):
    """
    Determines whether the conversation should continue or be summarized.

    Args:
        state (State): The current state containing messages and summary.

    Returns:
        str: The next node to execute ("summarize_conversation" or END).
    """
    messages = state["messages"]

    # If there are more than six messages, then we summarize the conversation
    if len(messages) > 6:
        return "summarize_conversation"

    # Otherwise we can just end
    return END


# Define the unified LangGraph Agent with Memory
builder = StateGraph(State)

# Add Nodes
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_node("summarize_conversation", summarize_conversation)

# Define Edges
# Start with the assistant node
builder.add_edge(START, "assistant")

# Assistant can trigger tool usage
builder.add_conditional_edges("assistant", tools_condition)

# After tools, loop back to assistant
builder.add_edge("tools", "assistant")

# After assistant, decide whether to summarize or continue
builder.add_conditional_edges("assistant", should_continue)

builder.add_edge("summarize_conversation", END)

# Compile the graph with a MemorySaver to persist state
memory = MemorySaver()
try:
    compiled_graph = builder.compile(checkpointer=memory)
    logger.info("Compiled the unified LangGraph agent with memory.")
except Exception as e:
    logger.error(f"Failed to compile the unified LangGraph agent: {e}")
    logger.error(traceback.format_exc())
    sys.exit(1)
