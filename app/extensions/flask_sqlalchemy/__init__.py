# encoding: utf-8
#
#  Project: py-ispyb
#  https://github.com/ispyb/py-ispyb
#
#  This file is part of py-ispyb software.
#
#  py-ispyb is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  py-ispyb is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with MXCuBE. If not, see <http://www.gnu.org/licenses/>.


__license__ = "LGPLv3+"


import sqlite3
from sqlalchemy import engine, MetaData

from flask_sqlalchemy import SQLAlchemy as BaseSQLAlchemy


def set_sqlite_pragma(dbapi_connection, connection_record):
    # pylint: disable=unused-argument
    """
    SQLite supports FOREIGN KEY syntax when emitting CREATE statements for
    tables, however by default these constraints have no effect on the
    operation of the table.

    http://docs.sqlalchemy.org/en/latest/dialects/sqlite.html#foreign-key-support
    """
    if not isinstance(dbapi_connection, sqlite3.Connection):
        return
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class AlembicDatabaseMigrationConfig(object):
    """
    Helper config holder that provides missing functions of Flask-Alembic
    package since we use custom invoke tasks instead.
    """

    def __init__(self, database, directory="migrations", **kwargs):
        self.db = database  # pylint: disable=invalid-name
        self.directory = directory
        self.configure_args = kwargs


class SQLAlchemy(BaseSQLAlchemy):
    """
    Customized Flask-SQLAlchemy adapter with enabled autocommit, constraints
    auto-naming conventions and ForeignKey constraints for SQLite.
    """

    def __init__(self, *args, **kwargs):
        if "session_options" not in kwargs:
            kwargs["session_options"] = {}
        kwargs["session_options"]["autocommit"] = True
        # Configure Constraint Naming Conventions:
        # http://docs.sqlalchemy.org/en/latest/core/constraints.html#constraint-naming-conventions
        kwargs["metadata"] = MetaData(
            naming_convention={
                "pk": "pk_%(table_name)s",
                "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
                "ix": "ix_%(table_name)s_%(column_0_name)s",
                "uq": "uq_%(table_name)s_%(column_0_name)s",
                "ck": "ck_%(table_name)s_%(constraint_name)s",
            }
        )
        super(SQLAlchemy, self).__init__(*args, **kwargs)

    def init_app(self, app):
        super(SQLAlchemy, self).init_app(app)

        database_uri = app.config["SQLALCHEMY_DATABASE_URI"]
        assert database_uri, "SQLALCHEMY_DATABASE_URI must be configured!"
        if database_uri.startswith("sqlite:"):
            self.event.listens_for(engine.Engine, "connect")(set_sqlite_pragma)

        app.extensions["migrate"] = AlembicDatabaseMigrationConfig(
            self, compare_type=True
        )
