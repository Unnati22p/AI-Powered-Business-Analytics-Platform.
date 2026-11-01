
import sqlite3
import pandas as pd

def create_database(df):

    conn = sqlite3.connect(":memory:")

    df.to_sql(
        "business_data",
        conn,
        if_exists="replace",
        index=False
    )

    return conn


def execute_query(df, query):

    conn = create_database(df)

    try:
        query_upper = query.strip().upper()

        # Allow only read-only SELECT queries
        if not query_upper.startswith("SELECT"):
            return None, "Only SELECT queries are allowed."

        result = pd.read_sql_query(query, conn)

        return result, None

    except Exception as e:
        return None, str(e)

    finally:
        conn.close()
