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
    __tablename__ = "keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[str] = mapped_column(String(50), nullable=False)  # hashed
    description: Mapped[str] = mapped_column(Text, nullable=False)


class EntityType(Base):
    __tablename__ = "entity_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )  # 'server', 'client'
    description: Mapped[str] = mapped_column(Text)

    # Relationships
    listings = relationship("Listing", back_populates="entity_type")


class DeviceClass(Base):
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
