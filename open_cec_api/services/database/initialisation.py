"""Perform database initialization tasks, if requested."""

from datetime import date

from sqlalchemy.orm import Session

from open_cec_api.services.database.models import (
    Certificate,
    DeviceClass,
    DeviceClassAttribute,
    EntityType,
    Key,
    Listing,
    ListingDeviceClass,
    ListingDeviceClassAttribute,
)
from open_cec_api.settings import settings


def init_db(session: Session) -> None:
    """
    Populate the database with example data.

    Returns a dictionary containing the created objects for reference.
    """
    created_objects = {}

    # Create dummy Key
    keys = [Key(value=settings.api_key_hash, description="dummy key")]

    for k in keys:
        session.add(k)
    session.flush()

    # Create Entity Types
    entity_types = [
        EntityType(name="client", description="Client-side devices and systems"),
        EntityType(name="server", description="Server-side devices and systems"),
    ]

    for et in entity_types:
        session.add(et)
    session.flush()  # Get IDs without committing

    created_objects["entity_types"] = {et.name: et for et in entity_types}

    # Create Device Classes
    device_classes = [
        DeviceClass(name="bess", description="Battery Energy Storage System"),
        DeviceClass(
            name="inverter", description="Power inverter for DC to AC conversion"
        ),
    ]

    for dc in device_classes:
        session.add(dc)
    session.flush()

    created_objects["device_classes"] = {dc.name: dc for dc in device_classes}

    # Create Device Class Attributes
    bess_attributes = [
        DeviceClassAttribute(
            device_class_id=created_objects["device_classes"]["bess"].id,  # type: ignore
            attribute_name="max_power",
            attribute_type="number",
            description="Maximum power output in kW",
        ),
        DeviceClassAttribute(
            device_class_id=created_objects["device_classes"]["bess"].id,  # type: ignore
            attribute_name="capacity",
            attribute_type="number",
            description="Energy storage capacity in kWh",
        ),
        DeviceClassAttribute(
            device_class_id=created_objects["device_classes"]["bess"].id,  # type: ignore
            attribute_name="chemistry",
            attribute_type="enum",
            description="Battery chemistry type (LiFePO4, NMC, etc.)",
        ),
        DeviceClassAttribute(
            device_class_id=created_objects["device_classes"]["bess"].id,  # type: ignore
            attribute_name="round_trip_efficiency",
            attribute_type="number",
            description="Round trip efficiency as percentage",
        ),
        DeviceClassAttribute(
            device_class_id=created_objects["device_classes"]["bess"].id,  # type: ignore
            attribute_name="cycle_life",
            attribute_type="number",
            description="Expected number of charge/discharge cycles",
        ),
    ]

    inverter_attributes = [
        DeviceClassAttribute(
            device_class_id=created_objects["device_classes"]["inverter"].id,  # type: ignore
            attribute_name="max_power",
            attribute_type="number",
            description="Maximum power output in kW",
        ),
        DeviceClassAttribute(
            device_class_id=created_objects["device_classes"]["inverter"].id,  # type: ignore
            attribute_name="efficiency",
            attribute_type="number",
            description="Power conversion efficiency as percentage",
        ),
        DeviceClassAttribute(
            device_class_id=created_objects["device_classes"]["inverter"].id,  # type: ignore
            attribute_name="input_voltage_range",
            attribute_type="string",
            description="DC input voltage range (e.g., '200-800V')",
        ),
        DeviceClassAttribute(
            device_class_id=created_objects["device_classes"]["inverter"].id,  # type: ignore
            attribute_name="output_voltage",
            attribute_type="string",
            description="AC output voltage (e.g., '240V', '480V')",
        ),
        DeviceClassAttribute(
            device_class_id=created_objects["device_classes"]["inverter"].id,  # type: ignore
            attribute_name="topology",
            attribute_type="enum",
            description="Inverter topology (string, central, micro, power optimizer)",
        ),
        DeviceClassAttribute(
            device_class_id=created_objects["device_classes"]["inverter"].id,  # type: ignore
            attribute_name="grid_tie",
            attribute_type="boolean",
            description="Whether the inverter can connect to the grid",
        ),
    ]

    all_attributes = bess_attributes + inverter_attributes
    for attr in all_attributes:
        session.add(attr)
    session.flush()

    created_objects["device_class_attributes"] = {
        "bess": bess_attributes,
        "inverter": inverter_attributes,
    }

    # Create Sample Listings
    listings = [
        # BESS Listings
        Listing(
            entity_type_id=created_objects["entity_types"]["client"].id,  # type: ignore
            manufacturer="Tesla",
            model="Powerwall 2",
            status="active",
        ),
        Listing(
            entity_type_id=created_objects["entity_types"]["server"].id,  # type: ignore
            manufacturer="LG Chem",
            model="RESU 10H",
            status="active",
        ),
        Listing(
            entity_type_id=created_objects["entity_types"]["client"].id,  # type: ignore
            manufacturer="Sonnen",
            model="ecoLinx",
            status="active",
        ),
        # Inverter Listings
        Listing(
            entity_type_id=created_objects["entity_types"]["client"].id,  # type: ignore
            manufacturer="SolarEdge",
            model="SE7600H-US",
            status="active",
        ),
        Listing(
            entity_type_id=created_objects["entity_types"]["server"].id,  # type: ignore
            manufacturer="Enphase",
            model="IQ7PLUS-72-2-US",
            status="active",
        ),
        Listing(
            entity_type_id=created_objects["entity_types"]["client"].id,  # type: ignore
            manufacturer="Fronius",
            model="Primo 8.2-1",
            status="active",
        ),
        # Hybrid BESS + Inverter system
        Listing(
            entity_type_id=created_objects["entity_types"]["client"].id,  # type: ignore
            manufacturer="Enphase",
            model="IQ Battery 5P",
            status="active",
        ),
    ]

    for listing in listings:
        session.add(listing)
    session.flush()

    created_objects["listings"] = listings

    # Create Listing-Device Class relationships
    listing_device_classes = [
        # BESS listings (first 3)
        ListingDeviceClass(
            listing_id=listings[0].id,
            device_class_id=created_objects["device_classes"]["bess"].id,  # type: ignore
        ),
        ListingDeviceClass(
            listing_id=listings[1].id,
            device_class_id=created_objects["device_classes"]["bess"].id,  # type: ignore
        ),
        ListingDeviceClass(
            listing_id=listings[2].id,
            device_class_id=created_objects["device_classes"]["bess"].id,  # type: ignore
        ),
        # Inverter listings (next 3)
        ListingDeviceClass(
            listing_id=listings[3].id,
            device_class_id=created_objects["device_classes"]["inverter"].id,  # type: ignore
        ),
        ListingDeviceClass(
            listing_id=listings[4].id,
            device_class_id=created_objects["device_classes"]["inverter"].id,  # type: ignore
        ),
        ListingDeviceClass(
            listing_id=listings[5].id,
            device_class_id=created_objects["device_classes"]["inverter"].id,  # type: ignore
        ),
        # Hybrid system (last listing) - both BESS and inverter
        ListingDeviceClass(
            listing_id=listings[6].id,
            device_class_id=created_objects["device_classes"]["bess"].id,  # type: ignore
        ),
        ListingDeviceClass(
            listing_id=listings[6].id,
            device_class_id=created_objects["device_classes"]["inverter"].id,  # type: ignore
        ),
    ]

    for ldc in listing_device_classes:
        session.add(ldc)
    session.flush()

    created_objects["listing_device_classes"] = listing_device_classes

    # Create Listing Device Class Attributes with sample values
    bess_device_class_id = created_objects["device_classes"]["bess"].id  # type: ignore
    inverter_device_class_id = created_objects["device_classes"]["inverter"].id  # type: ignore

    listing_attributes = [
        # Tesla Powerwall 2 attributes
        ListingDeviceClassAttribute(
            listing_id=listings[0].id,
            device_class_id=bess_device_class_id,
            attribute_name="max_power",
            attribute_value="5.0",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[0].id,
            device_class_id=bess_device_class_id,
            attribute_name="capacity",
            attribute_value="13.5",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[0].id,
            device_class_id=bess_device_class_id,
            attribute_name="chemistry",
            attribute_value="NMC",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[0].id,
            device_class_id=bess_device_class_id,
            attribute_name="round_trip_efficiency",
            attribute_value="90",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[0].id,
            device_class_id=bess_device_class_id,
            attribute_name="cycle_life",
            attribute_value="5000",
        ),
        # LG Chem RESU 10H attributes
        ListingDeviceClassAttribute(
            listing_id=listings[1].id,
            device_class_id=bess_device_class_id,
            attribute_name="max_power",
            attribute_value="5.0",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[1].id,
            device_class_id=bess_device_class_id,
            attribute_name="capacity",
            attribute_value="9.8",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[1].id,
            device_class_id=bess_device_class_id,
            attribute_name="chemistry",
            attribute_value="NMC",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[1].id,
            device_class_id=bess_device_class_id,
            attribute_name="round_trip_efficiency",
            attribute_value="95",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[1].id,
            device_class_id=bess_device_class_id,
            attribute_name="cycle_life",
            attribute_value="6000",
        ),
        # Sonnen ecoLinx attributes
        ListingDeviceClassAttribute(
            listing_id=listings[2].id,
            device_class_id=bess_device_class_id,
            attribute_name="max_power",
            attribute_value="12.0",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[2].id,
            device_class_id=bess_device_class_id,
            attribute_name="capacity",
            attribute_value="20.0",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[2].id,
            device_class_id=bess_device_class_id,
            attribute_name="chemistry",
            attribute_value="LiFePO4",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[2].id,
            device_class_id=bess_device_class_id,
            attribute_name="round_trip_efficiency",
            attribute_value="93",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[2].id,
            device_class_id=bess_device_class_id,
            attribute_name="cycle_life",
            attribute_value="10000",
        ),
        # SolarEdge SE7600H-US attributes
        ListingDeviceClassAttribute(
            listing_id=listings[3].id,
            device_class_id=inverter_device_class_id,
            attribute_name="max_power",
            attribute_value="7.6",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[3].id,
            device_class_id=inverter_device_class_id,
            attribute_name="efficiency",
            attribute_value="97.6",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[3].id,
            device_class_id=inverter_device_class_id,
            attribute_name="input_voltage_range",
            attribute_value="200-1000V",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[3].id,
            device_class_id=inverter_device_class_id,
            attribute_name="output_voltage",
            attribute_value="240V",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[3].id,
            device_class_id=inverter_device_class_id,
            attribute_name="topology",
            attribute_value="power optimizer",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[3].id,
            device_class_id=inverter_device_class_id,
            attribute_name="grid_tie",
            attribute_value="true",
        ),
        # Enphase IQ7PLUS attributes
        ListingDeviceClassAttribute(
            listing_id=listings[4].id,
            device_class_id=inverter_device_class_id,
            attribute_name="max_power",
            attribute_value="0.295",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[4].id,
            device_class_id=inverter_device_class_id,
            attribute_name="efficiency",
            attribute_value="97.0",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[4].id,
            device_class_id=inverter_device_class_id,
            attribute_name="input_voltage_range",
            attribute_value="16-48V",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[4].id,
            device_class_id=inverter_device_class_id,
            attribute_name="output_voltage",
            attribute_value="240V",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[4].id,
            device_class_id=inverter_device_class_id,
            attribute_name="topology",
            attribute_value="micro",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[4].id,
            device_class_id=inverter_device_class_id,
            attribute_name="grid_tie",
            attribute_value="true",
        ),
        # Fronius Primo attributes
        ListingDeviceClassAttribute(
            listing_id=listings[5].id,
            device_class_id=inverter_device_class_id,
            attribute_name="max_power",
            attribute_value="8.2",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[5].id,
            device_class_id=inverter_device_class_id,
            attribute_name="efficiency",
            attribute_value="98.0",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[5].id,
            device_class_id=inverter_device_class_id,
            attribute_name="input_voltage_range",
            attribute_value="150-1000V",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[5].id,
            device_class_id=inverter_device_class_id,
            attribute_name="output_voltage",
            attribute_value="240V",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[5].id,
            device_class_id=inverter_device_class_id,
            attribute_name="topology",
            attribute_value="string",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[5].id,
            device_class_id=inverter_device_class_id,
            attribute_name="grid_tie",
            attribute_value="true",
        ),
        # Enphase IQ Battery 5P - BESS attributes
        ListingDeviceClassAttribute(
            listing_id=listings[6].id,
            device_class_id=bess_device_class_id,
            attribute_name="max_power",
            attribute_value="5.0",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[6].id,
            device_class_id=bess_device_class_id,
            attribute_name="capacity",
            attribute_value="5.0",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[6].id,
            device_class_id=bess_device_class_id,
            attribute_name="chemistry",
            attribute_value="LiFePO4",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[6].id,
            device_class_id=bess_device_class_id,
            attribute_name="round_trip_efficiency",
            attribute_value="89",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[6].id,
            device_class_id=bess_device_class_id,
            attribute_name="cycle_life",
            attribute_value="6000",
        ),
        # Enphase IQ Battery 5P - Inverter attributes
        ListingDeviceClassAttribute(
            listing_id=listings[6].id,
            device_class_id=inverter_device_class_id,
            attribute_name="max_power",
            attribute_value="5.0",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[6].id,
            device_class_id=inverter_device_class_id,
            attribute_name="efficiency",
            attribute_value="96.0",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[6].id,
            device_class_id=inverter_device_class_id,
            attribute_name="input_voltage_range",
            attribute_value="200-480V",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[6].id,
            device_class_id=inverter_device_class_id,
            attribute_name="output_voltage",
            attribute_value="240V",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[6].id,
            device_class_id=inverter_device_class_id,
            attribute_name="topology",
            attribute_value="micro",
        ),
        ListingDeviceClassAttribute(
            listing_id=listings[6].id,
            device_class_id=inverter_device_class_id,
            attribute_name="grid_tie",
            attribute_value="true",
        ),
    ]

    for attr in listing_attributes:
        session.add(attr)
    session.flush()

    created_objects["listing_device_class_attributes"] = listing_attributes

    # Create some sample certificates
    certificates = [
        Certificate(
            listing_id=listings[0].id,
            expiry=date(2025, 12, 31),
            certification_date=date(2023, 1, 15),
            certifying_body="UL",
            test_profiles=["UL1973", "UL9540", "IEEE1547"],
        ),
        Certificate(
            listing_id=listings[3].id,
            expiry=date(2026, 6, 30),
            certification_date=date(2023, 3, 20),
            certifying_body="UL",
            test_profiles=["UL1741", "IEEE1547", "FCC Part 15"],
        ),
        Certificate(
            listing_id=listings[1].id,
            expiry=date(2025, 9, 15),
            certification_date=date(2022, 12, 10),
            certifying_body="IEC",
            test_profiles=["IEC62619", "IEC61000"],
        ),
    ]

    for cert in certificates:
        session.add(cert)
    session.flush()

    created_objects["certificates"] = certificates

    # Commit all changes
    session.commit()
