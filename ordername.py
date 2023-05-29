from sqlalchemy import create_engine

# Create a database connection
engine = create_engine('sqlite:///PizzaOrders.db')

# Get a database connection
conn = engine.connect()

# Execute the SQL statement to alter the table
alter_statement = """
    ALTER TABLE PizzaOrders
    ADD COLUMN orderName TEXT;
"""
conn.execute(alter_statement)

# Close the database connection
conn.close()
