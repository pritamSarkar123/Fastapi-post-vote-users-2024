from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

from ..database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(500), nullable=False)
    content = Column(String(1000), nullable=False)
    published = Column(Boolean, nullable=False, server_default="TRUE")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        Integer, ForeignKey(column="users.id", ondelete="CASCADE"), nullable=False
    )  # fk name to_from_fk

    # autofetch ability, no db related stuff, just sql alchemy stuff
    owner = relationship(
        "User"
    )  # will not be reflected by alembis, as it is handled by sqlalchemy , not db property
