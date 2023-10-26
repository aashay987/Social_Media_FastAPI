"""add values to posts,users,votes

Revision ID: 4d7f658a5ca4
Revises: c4e7c3edf4e5
Create Date: 2023-10-21 17:53:06.259359

"""
from typing import Sequence, Union

from alembic import op

import sqlalchemy as sa

#from ..env import Base

# revision identifiers, used by Alembic.
revision: str = '4d7f658a5ca4'
down_revision: Union[str, None] = 'c4e7c3edf4e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



# pass in tuple with tables we want to reflect, otherwise whole database will get reflected

def upgrade() -> None:
    table_name = 'users'  # Replace this with your actual table name
    table = sa.Table(table_name, sa.MetaData(), autoload_with=op.get_bind())

    # Define the data to be inserted (list of dictionaries)
    data_to_insert = [
        {
            'name': 'admin', 
            'email': 'admin@gmail.com',
            'password': 'default'    
        }
        # Add more dictionaries as needed
    ]

    # Perform bulk insert
    op.bulk_insert(table, data_to_insert)

def downgrade():
    # For downgrades, you might want to delete the inserted data
    table_name = 'users'  # Replace this with your actual table name
    op.execute(f"DELETE FROM {table_name}")

