# SQL injection vulnerable
def search_products(search_term):
  query = f"SELECT * FROM products WHERE name LIKE '%{search_term}%'"    # pass user input as an executable code
  return query

# Safe version
def search_product(search_term, cursor):
  query = "SELECT * FROM products WHERE name LIKE ?"    # treats user input (search_term) as a data. "?" is a placeholder. It separates the query structure from the user input.
  cursor.execute(query, (search_term,))    # "," after search_term ensures that the input is a tuple.