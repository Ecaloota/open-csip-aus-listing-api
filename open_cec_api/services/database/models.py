from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY  # postgres specific for ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Key(Base):
    """
    Stores access keys
    """

    __tablename__ = "keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[str] = mapped_column(String(50), nullable=False)  # hashed
    description: Mapped[str] = mapped_column(Text, nullable=False)


class EntityType(Base):
    """
    Defines categories of entities (e.g. server or client). Each entity type has a unique
    name and description. One entity type can be associated with many listings. A listing
    must reference exactly one entity type (e.g. a listing can only be one of server or client)
    """

    __tablename__ = "entity_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )  # 'server', 'client'
    description: Mapped[str] = mapped_column(Text)

    # Relationships
    listings = relationship("Listing", back_populates="entity_type")


class DeviceClass(Base):
    """
    Represents a category of devices such as a BESS or inverter. A device class can be linked
    to many listings through a join table and can define many attributes that describe the
    properties of the class.
    """

    __tablename__ = "device_classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True
    )  # 'BESS', 'inverter', etc.
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.current_timestamp()
    )

    # Relationships
    listing_device_classes = relationship(
        "ListingDeviceClass", back_populates="device_class"
    )
    device_class_attributes = relationship(
        "DeviceClassAttribute", back_populates="device_class"
    )


class Listing(Base):
    """Represents a specific product offered by a manufacturer, unique by
    manufacturer-model pair. Each listing:

    * Belongs to one entity type
    * Can be associated with multiple device classes
    * Can store attribute values specific to its device classes
    * Can have multiple certificates
    """

    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("entity_types.id"), nullable=False
    )
    manufacturer: Mapped[str] = mapped_column(String(255), nullable=False)
    model: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), default="active"
    )  # 'active', 'suspended', 'expired'
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.current_timestamp()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )

    # Constraints
    __table_args__ = (UniqueConstraint("manufacturer", "model"),)

    # Relationships
    entity_type = relationship("EntityType", back_populates="listings")
    listing_device_classes = relationship(
        "ListingDeviceClass", back_populates="listing", cascade="all, delete-orphan"
    )
    listing_device_class_attributes = relationship(
        "ListingDeviceClassAttribute",
        back_populates="listing",
        cascade="all, delete-orphan",
    )
    certificates = relationship(
        "Certificate", back_populates="listing", cascade="all, delete-orphan"
    )


class ListingDeviceClass(Base):
    """A join table that links listings and device classes. It models a many-to-many
    relationship: a listing can belong to multiple device classes and a device class can
    apply to multiple listings. Each listing-device class pair is unique."""

    __tablename__ = "listing_device_classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    listing_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("listings.id"), nullable=False
    )
    device_class_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("device_classes.id"), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.current_timestamp()
    )

    # Constraints
    __table_args__ = (UniqueConstraint("listing_id", "device_class_id"),)

    # Relationships
    listing = relationship("Listing", back_populates="listing_device_classes")
    device_class = relationship("DeviceClass", back_populates="listing_device_classes")


class DeviceClassAttribute(Base):
    """Defines attribute schemas for a device class. Each record specifies an attribute name
    and type, and optional description. A device class can have many attributes"""

    __tablename__ = "device_class_attributes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_class_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("device_classes.id"), nullable=False
    )
    attribute_name: Mapped[str] = mapped_column(String(100), nullable=False)
    attribute_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # 'string', 'number', 'boolean', 'enum'
    description: Mapped[str] = mapped_column(Text, nullable=True)

    # Constraints
    __table_args__ = (UniqueConstraint("device_class_id", "attribute_name"),)

    # Relationships
    device_class = relationship("DeviceClass", back_populates="device_class_attributes")


class ListingDeviceClassAttribute(Base):
    """Stores attribute values for a lisitng within a device class. It links a listing
    and device class to an attribute name and value. Each listing-device class-attribute
    combination is unqiue. This model instantiates the attribute definitions from DeviceClassAttribute."""

    __tablename__ = "listing_device_class_attributes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    listing_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("listings.id"), nullable=False
    )
    device_class_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("device_classes.id"), nullable=False
    )
    attribute_name: Mapped[str] = mapped_column(String(100), nullable=False)
    attribute_value: Mapped[str] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=func.current_timestamp()
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint("listing_id", "device_class_id", "attribute_name"),
    )

    # Relationships
    listing = relationship("Listing", back_populates="listing_device_class_attributes")


class Certificate(Base):
    """Represents certifications associated with a listing. Each certificate records details
    associated with the certification event, such as the expiry date and certifying body.
    A listing can have multiple certificates, and a certificate belongs to exactly one listing"""

    __tablename__ = "certificates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    listing_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("listings.id"), nullable=False
    )
    expiry: Mapped[Date] = mapped_column(Date, nullable=False)
    certification_date: Mapped[Date] = mapped_column(Date, nullable=False)
    certifying_body: Mapped[str] = mapped_column(String(100), nullable=False)

    test_profiles: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)

    # Relationships
    listing = relationship("Listing", back_populates="certificates")
