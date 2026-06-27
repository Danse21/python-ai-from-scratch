# SQL injection vulnerable
def search_products(search_term):
  query = f"SELECT * FROM products WHERE name LIKE '%{search_term}%'"
  return query

# Safe version
def search_product(search_term, cursor):
  query = "SELECT * FROM products WHERE name LIKE ?"
  cursor.execute(query, (search_term,))