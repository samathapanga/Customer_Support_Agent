from langchain_core.tools import tool


# Mock customer data
CUSTOMERS = {
    "CUST001": {
        "name": "John Smith",
        "loan_type": "Personal Loan",
        "loan_amount": 500000,
        "loan_status": "Approved",
        "loan_balance": 325000
    },
    "CUST002": {
        "name": "Rahul Sharma",
        "loan_type": "Home Loan",
        "loan_amount": 3000000,
        "loan_status": "Under Review",
        "loan_balance": 2800000
    },
    "CUST003": {
        "name": "Priya Reddy",
        "loan_type": "Car Loan",
        "loan_amount": 800000,
        "loan_status": "Rejected",
        "loan_balance": 0
    }
}


@tool
def check_loan_status(customer_id: str) -> str:
    """
    Check the current loan status of a customer.
    """

    customer = CUSTOMERS.get(customer_id)

    if not customer:
        return f"Customer ID {customer_id} was not found."

    return (
        f"Customer {customer['name']} has a "
        f"{customer['loan_type']} with status: "
        f"{customer['loan_status']}."
    )


@tool
def get_customer_details(customer_id: str) -> str:
    """
    Get customer and loan details using the customer ID.
    """

    customer = CUSTOMERS.get(customer_id)

    if not customer:
        return f"Customer ID {customer_id} was not found."

    return (
        f"Name: {customer['name']}\n"
        f"Loan Type: {customer['loan_type']}\n"
        f"Loan Amount: ₹{customer['loan_amount']}\n"
        f"Loan Status: {customer['loan_status']}\n"
        f"Outstanding Balance: ₹{customer['loan_balance']}"
    )


@tool
def calculate_emi(
    loan_amount: float,
    annual_interest_rate: float,
    tenure_years: int
) -> str:
    """
    Calculate monthly EMI for a loan.
    """

    monthly_rate = annual_interest_rate / 12 / 100
    number_of_months = tenure_years * 12

    if monthly_rate == 0:
        emi = loan_amount / number_of_months
    else:
        emi = (
            loan_amount
            * monthly_rate
            * (1 + monthly_rate) ** number_of_months
            / ((1 + monthly_rate) ** number_of_months - 1)
        )

    return f"Monthly EMI: ₹{emi:,.2f}"


@tool
def get_loan_balance(customer_id: str) -> str:
    """
    Check the outstanding loan balance of a customer.
    """

    customer = CUSTOMERS.get(customer_id)

    if not customer:
        return f"Customer ID {customer_id} was not found."

    return (
        f"Customer {customer['name']} has an "
        f"outstanding loan balance of "
        f"₹{customer['loan_balance']:,}."
    )