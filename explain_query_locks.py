import argparse

import psycopg2
from prettytable import PrettyTable

LOCK_CHECK_QUERY = """
    SELECT l.relation,
           c.relname,
           l.mode
    FROM pg_locks l
    JOIN pg_class c ON c.oid=l.relation
    JOIN pg_stat_activity a on l.pid = a.pid
    AND a.query NOT ILIKE '%pg_stat_activity%'
    ORDER BY l.relation ASC;
"""

RELATION_ID = 'Relation ID'
RELATION_NAME = 'Relation Name'
LOCK_TYPE = 'Lock Type'


def main(
        user: str,
        password: str,
        host: str,
        port: str,
        database: str,
        query: str,
):
    """Execute and rollback a query to see what locks it will take"""

    # Create a DB connection that will "stage" but not commit the DB change
    connection_for_schema_change = psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database,
    )
    connection_for_schema_change.autocommit = False
    schema_change_cursor = connection_for_schema_change.cursor()

    # Create a DB connection that will check what Locks are taken for "query"
    connection_for_lock_check = psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database,
    )
    lock_check_cursor = connection_for_lock_check.cursor()

    # Execute the query, but do not commit
    schema_change_cursor.execute(query)

    lock_check_cursor.execute(LOCK_CHECK_QUERY)

    results = lock_check_cursor.fetchall()

    connection_for_schema_change.rollback()

    results_table = PrettyTable()

    results_table.field_names = [RELATION_ID, RELATION_NAME, LOCK_TYPE]
    results_table.align[RELATION_ID] = 'l'
    results_table.align[RELATION_NAME] = 'l'
    results_table.align[LOCK_TYPE] = 'l'

    for relation_id, relation_name, lock_type in results:
        results_table.add_row([relation_id, relation_name, lock_type])

    print(results_table)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--query',
        required=True,
        help='A DDL statement to explain',
    )

    parser.add_argument(
        '--user',
        required=True,
        help='User for database connection',
    )

    parser.add_argument(
        '--password',
        required=True,
        help='Password for database connection',
    )

    parser.add_argument(
        '--host',
        default='localhost',
        help='Host for database connection',
    )

    parser.add_argument(
        '--port',
        default='5432',
        help='Port for database connection',
    )

    parser.add_argument(
        '--database',
        required=True,
        help='Database for database connection',
    )

    args = parser.parse_args()

    main(
        args.user,
        args.password,
        args.host,
        args.port,
        args.database,
        args.query,
    )
