def format_currency(amount):
    amount = float(amount)
    return f"{amount:,.0f}".replace(",", ".")
