# Constants for the state and county tax rates
STATE_TAX_RATE = 0.05
COUNTY_TAX_RATE = 0.025

# Main function
def main():
    try:
        # Get the amount of the purchase from the user
        purchase_amount = float(input("Enter the purchase amount: "))

        # Calculate the state and county tax
        state_tax = calculate_state_tax(purchase_amount)
        county_tax = calculate_county_tax(purchase_amount)

        # Display results
        show_sale(purchase_amount, state_tax, county_tax)

    except ValueError:
        print("Invalid input. Please enter a numeric value.")

# Function to calculate the state tax
def calculate_state_tax(purchase):
    return purchase * STATE_TAX_RATE

# Function to calculate the county tax
def calculate_county_tax(purchase):
    return purchase * COUNTY_TAX_RATE

# Function to display formatted sale details
def show_sale(purchase, state_tax, county_tax):
    total_tax = state_tax + county_tax
    total_sale = purchase + total_tax

    print("\nSales Summary:")
    print(f"Purchase amount: ${purchase:,.2f}")
    print(f"State tax:       ${state_tax:,.2f}")
    print(f"County tax:      ${county_tax:,.2f}")
    print(f"Total tax:       ${total_tax:,.2f}")
    print(f"Total sale:      ${total_sale:,.2f}")

# Run the program
if __name__ == "__main__":
    main()
