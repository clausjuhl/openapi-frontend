from datetime import datetime
import sqlalchemy


metadata = sqlalchemy.MetaData()


bookmarks = sqlalchemy.Table(
    "bookmarks",
    metadata,
    sqlalchemy.Column("pk", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.ForeignKey("users.openid"),
        index=True,
        nullable=False,
    ),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.DateTime,
        default=datetime.utcnow,
        nullable=False,
    ),
    sqlalchemy.Column("resource_id", sqlalchemy.String, nullable=False),
)


searches = sqlalchemy.Table(
    "searches",
    metadata,
    sqlalchemy.Column("pk", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "user_id",
        sqlalchemy.ForeignKey("users.openid"),
        index=True,
        nullable=False,
    ),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.DateTime,
        default=datetime.utcnow,
        nullable=False,
    ),
    sqlalchemy.Column(
        "updated_at",
        sqlalchemy.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    ),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("query_string", sqlalchemy.String, nullable=False),
)


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("pk", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "openid", sqlalchemy.String, index=True, nullable=False, unique=True
    ),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.DateTime,
        default=datetime.utcnow,
        nullable=False,
    ),
    sqlalchemy.Column(
        "updated_at",
        sqlalchemy.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    ),
    sqlalchemy.Column(
        "last_login",
        sqlalchemy.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    ),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column(
        "is_admin", sqlalchemy.Boolean, nullable=False, default=False
    ),
    sqlalchemy.Column(
        "is_employee", sqlalchemy.Boolean, nullable=False, default=False
    ),
    sqlalchemy.Column("email", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("email_verified", sqlalchemy.Boolean, nullable=False),
)
