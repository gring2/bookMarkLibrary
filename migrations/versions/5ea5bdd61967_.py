"""empty message

Revision ID: 5ea5bdd61967
Revises: ad42ec6ad206
Create Date: 2019-05-12 14:27:02.426693

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5ea5bdd61967'
down_revision = 'ad42ec6ad206'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookmarks', sa.Column('user_id', sa.Integer(), nullable=True))

    connection = op.get_bind()

    result = connection.execute("""
        UPDATE bookmarks SET user_id=(SELECT user_id from categories WHERE bookmarks.parent_id = categories.id)

    """)

    op.drop_table('categories')
    op.alter_column('bookmark_tag_rel', 'tags',
               existing_type=mysql.CHAR(length=32),
               nullable=True)
    op.create_foreign_key(None, 'bookmarks', 'user', ['user_id'], ['id'])
    op.drop_column('bookmarks', 'parent_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookmarks', sa.Column('parent_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'bookmarks', type_='foreignkey')
    op.drop_column('bookmarks', 'user_id')
    op.alter_column('bookmark_tag_rel', 'tags',
               existing_type=mysql.CHAR(length=32),
               nullable=False)
    op.create_table('categories',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('parent_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('created_at', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('updated_at', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('deleted_at', mysql.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='categories_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
