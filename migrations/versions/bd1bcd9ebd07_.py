"""empty message

Revision ID: bd1bcd9ebd07
Revises: 
Create Date: 2021-08-14 13:01:44.001166

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd1bcd9ebd07'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('surname', sa.String(length=120), nullable=True),
    sa.Column('room', sa.Integer(), nullable=True),
    sa.Column('chat_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('chat_id')
    )
    op.create_index(op.f('ix_student_name'), 'student', ['name'], unique=False)
    op.create_index(op.f('ix_student_surname'), 'student', ['surname'], unique=False)
    op.create_table('problems',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_problems_text'), 'problems', ['text'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_problems_text'), table_name='problems')
    op.drop_table('problems')
    op.drop_index(op.f('ix_student_surname'), table_name='student')
    op.drop_index(op.f('ix_student_name'), table_name='student')
    op.drop_table('student')
    # ### end Alembic commands ###
