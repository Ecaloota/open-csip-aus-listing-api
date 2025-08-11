from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class EntityType(Base):
    __tablename__ = "entity_types"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)  # 'server', 'client'
    description = Column(Text)

    # Relationships
    listings = relationship("Listing", back_populates="entity_type")


class DeviceClass(Base):
    __tablename__ = "device_classes"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)  # 'BESS', 'inverter', etc.
    description = Column(Text)
    requires_inverter = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.current_timestamp())

    # Relationships
    listing_device_classes = relationship(
        "ListingDeviceClass", back_populates="device_class"
    )
    device_class_attributes = relationship(
        "DeviceClassAttribute", back_populates="device_class"
    )


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True)
    entity_type_id = Column(Integer, ForeignKey("entity_types.id"), nullable=False)
    manufacturer = Column(String(255), nullable=False)
    model = Column(String(255), nullable=False)
    version = Column(String(100))
    csip_aus_version = Column(String(50), nullable=False)
    certification_body = Column(String(255))
    certification_date = Column(Date)
    certification_expiry = Column(Date)
    status = Column(String(50), default="active")  # 'active', 'suspended', 'expired'
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(
        DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp()
    )

    # Constraints
    __table_args__ = (UniqueConstraint("manufacturer", "model", "version"),)

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

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    device_class_id = Column(Integer, ForeignKey("device_classes.id"), nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.current_timestamp())

    # Constraints
    __table_args__ = (UniqueConstraint("listing_id", "device_class_id"),)

    # Relationships
    listing = relationship("Listing", back_populates="listing_device_classes")
    device_class = relationship("DeviceClass", back_populates="listing_device_classes")


class DeviceClassAttribute(Base):
    __tablename__ = "device_class_attributes"

    id = Column(Integer, primary_key=True)
    device_class_id = Column(Integer, ForeignKey("device_classes.id"), nullable=False)
    attribute_name = Column(String(100), nullable=False)
    attribute_type = Column(
        String(50), nullable=False
    )  # 'string', 'number', 'boolean', 'enum'
    is_required = Column(Boolean, default=False)
    enum_values = Column(ARRAY(Text))  # For enum types
    description = Column(Text)

    # Constraints
    __table_args__ = (UniqueConstraint("device_class_id", "attribute_name"),)

    # Relationships
    device_class = relationship("DeviceClass", back_populates="device_class_attributes")


class ListingDeviceClassAttribute(Base):
    __tablename__ = "listing_device_class_attributes"

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    device_class_id = Column(Integer, ForeignKey("device_classes.id"), nullable=False)
    attribute_name = Column(String(100), nullable=False)
    attribute_value = Column(Text)
    created_at = Column(DateTime, default=func.current_timestamp())

    # Constraints
    __table_args__ = (
        UniqueConstraint("listing_id", "device_class_id", "attribute_name"),
    )

    # Relationships
    listing = relationship("Listing", back_populates="listing_device_class_attributes")


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    certificate_data = Column(String)

    # Relationships
    listing = relationship("Listing", back_populates="certificates")
