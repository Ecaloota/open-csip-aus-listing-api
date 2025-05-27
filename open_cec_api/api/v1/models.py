from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class BaseV1(DeclarativeBase):
    pass


class SoftwareCommsClientModel_V1(BaseV1):
    __tablename__ = "software_comms_client"

    index = Column(Integer, primary_key=True, autoincrement=True)
    Communication_Device_Name__c = Column(String(255), nullable=True)  # TODO
    Communication_Manufacturer__c = Column(String(255), nullable=True)  # TODO
    Communication_Manufacturer_Name__c = Column(String(255), nullable=True)  # TODO
    Communication_Model_Name__c = Column(String(255), nullable=True)  # TODO


# class InverterCertificateDetailsModel_V1(BaseV1):
#     __tablename__ = "inverter_certificate_details"

#     index = Column(Integer, primary_key=True, autoincrement=True)
#     SalesforceInverterCertID = Column(String(255), nullable=False)
#     AS3100Tested = Column(Boolean, nullable=False)
#     AS4777Tested = Column(Boolean, nullable=False)
#     ApplicableStandardsOther = Column(String(255), nullable=True)  # TODO
#     ApplicableStandards = Column(String(255), nullable=False)  # TODO allowed standards
#     ApprovalDate = Column(String(255), nullable=False)  # TODO whenever date
#     ApprovingBody = Column(String(255), nullable=True)  # TODO
#     CECApprovedDate = Column(String(255), nullable=False)  # TODO whenever date
#     CECApproved = Column(Boolean, nullable=False)
#     CertificateNumber = Column(String(255), nullable=False)
#     BatteryCertifyingBody = Column(String(255), nullable=True)  # TODO
#     EquipmentCategory = Column(String(255), nullable=False)
#     ExpiryDate = Column(String(255), nullable=False)  # TODO whenever date
#     BrandName = Column(String(255), nullable=False)
#     TradingNames = Column(String(255), nullable=False)
#     AgreedtoTermsConditions = Column(Boolean, nullable=False)
#     ForTesting = Column(Boolean, nullable=False)

#     # Foreign keys to SoftwareCommsClientModel
#     Software_Communications_Client__c = Column(
#         String(255),
#         nullable=True,
#         ForeignKey="software_comms_client.index",
#     )
#     Software_Communications_Client_2__c = Column(
#         String(255),
#         nullable=True,
#         ForeignKey="software_comms_client.index",
#     )
#     Software_Communications_Client_3__c = Column(
#         String(255),
#         nullable=True,
#         ForeignKey="software_comms_client.index",
#     )
#     Software_Communications_Client_4__c = Column(
#         String(255),
#         nullable=True,
#         ForeignKey="software_comms_client.index",
#     )
#     Software_Communications_Client_5__c = Column(
#         String(255),
#         nullable=True,
#         ForeignKey="software_comms_client.index",
#     )
#     Software_Communications_Client_6__c = Column(
#         String(255),
#         nullable=True,
#         ForeignKey="software_comms_client.index",
#     )
#     Software_Communications_Client_7__c = Column(
#         String(255),
#         nullable=True,
#         ForeignKey="software_comms_client.index",
#     )
#     Software_Communications_Client_8__c = Column(
#         String(255),
#         nullable=True,
#         ForeignKey="software_comms_client.index",
#     )
#     Software_Communications_Client_9__c = Column(
#         String(255),
#         nullable=True,
#         ForeignKey="software_comms_client.index",
#     )
#     Software_Communications_Client_10__c = Column(
#         String(255),
#         nullable=True,
#         ForeignKey="software_comms_client.index",
#     )


# class InverterCertificateApplicationDetailsModel_V1(BaseV1):
#     __tablename__ = "inverter_certificate_application_details"

#     index = Column(Integer, primary_key=True, autoincrement=True)
#     Name = Column(String(255), nullable=False)


# class InverterCertificateApplicationModel_V1(BaseV1):
#     __tablename__ = "inverter_certificate_application"

#     index = Column(Integer, primary_key=True, autoincrement=True)
#     Details = Column(
#         String(255),
#         nullable=False,
#         ForeignKey="inverter_certificate_application_details.index",
#     )


# class InverterCertificateApplicationContactDetailsModel_V1(BaseV1):
#     __tablename__ = "inverter_certificate_application_contact_details"

#     index = Column(Integer, primary_key=True, autoincrement=True)
#     FirstName = Column(String(255), nullable=False)
#     LastName = Column(String(255), nullable=False)


# class InverterCertificateApplicationContact_V1(BaseV1):
#     __tablename__ = "inverter_certificate_application_contact"

#     index = Column(Integer, primary_key=True, autoincrement=True)
#     Details = Column(
#         String(255),
#         nullable=False,
#         ForeignKey="inverter_certificate_application_contact_details.index",
#     )


# class InverterCertificateApplicationHolderAccountDetailsModel_V1(BaseV1):
#     __tablename__ = "inverter_certificate_application_holder_account_details"

#     index = Column(Integer, primary_key=True, autoincrement=True)
#     Name = Column(String(255), nullable=False)


# class InverterCertificateApplicationHolderAccount_V1(BaseV1):
#     __tablename__ = "inverter_certificate_application_holder_account"

#     index = Column(Integer, primary_key=True, autoincrement=True)
#     Details = Column(
#         String(255),
#         nullable=False,
#         ForeignKey="inverter_certificate_application_holder_account_details.index",
#     )


# class InverterCertificateModel_V1(BaseV1):
#     __tablename__ = "inverter_certificate"

#     index = Column(Integer, primary_key=True, autoincrement=True)
#     Details = Column(
#         String(255),
#         nullable=False,
#         ForeignKey="inverter_certificate_details.index",
#     )
#     Application = Column(
#         String(255),
#         nullable=False,
#         ForeignKey="inverter_certificate_application.index",
#     )
#     Contact = Column(
#         String(255),
#         nullable=False,
#         ForeignKey="inverter_certificate_application_contact.index",
#     )
#     ManufacturerCertificateHolderAccount = Column(
#         String(255),
#         nullable=False,
#         ForeignKey="inverter_certificate_application_holder_account.index",
#     )


# class InverterDetailsModel_V1(BaseV1):
#     __tablename__ = "inverter_details"

#     index = Column(Integer, primary_key=True, autoincrement=True)
#     Id = Column(String(255), nullable=False)
#     Model_Number__c = Column(String(255), nullable=False)
#     Series__c = Column(String(255), nullable=False)
#     Export_Control__c = Column(String(255), nullable=True)  # TODO
#     Generation_control__c = Column(String(255), nullable=True)  # TODO
#     Integrated_Battery_DC_Switch__c = Column(String(255), nullable=False)
#     Integrated_PV_DC_Switch__c = Column(String(255), nullable=False)
#     Internal_Battery__c = Column(Boolean, nullable=False)
#     CECLimitWithinInverterRange = Column(Boolean, nullable=False)
#     CECLimitWithinInverterRangeReason = Column(String(255), nullable=True)  # TODO
#     MultiInverterCombinationsTested = Column(Boolean, nullable=False)
#     Nominal_AC_Power_W__c = Column(Integer, nullable=False)
#     No_of_Phases__c = Column(Integer, nullable=False)
#     PQ_Mode_Cos_Power__c = Column(Boolean, nullable=False)
#     PQ_Mode_Fixed_P_Factor__c = Column(Boolean, nullable=False)
#     PQ_Mode_Rate_Limit__c = Column(String(255), nullable=True)  # TODO
#     PQ_Mode_Volt_Balance__c = Column(Boolean, nullable=False)
#     PQ_Mode_Volt_Watt__c = Column(Boolean, nullable=False)
#     PQ_Mode_Volt_Var__c = Column(Boolean, nullable=False)
#     Tested_to_IEC_62116__c = Column(Boolean, nullable=False)
#     Inverter_without_Nominal_230_400V_Output__c = Column(Boolean, nullable=False)
#     Test_Scenarios__c = Column(String(255), nullable=True)  # TODO
#     Power_rate_limits_compliant_with_4777_2__c = Column(Boolean, nullable=False)
#     Active_Anti_Island_Method__c = Column(String(255), nullable=False)
#     VDRT = Column(Boolean, nullable=False)
#     Internet_capability_via_LAN_WLAN_Wi_Fi = Column(String(255), nullable=False)
#     OnboardCommsPort = Column(String(255), nullable=False)
#     PV_Isolator_EESS__c = Column(String(255), nullable=True)  # TODO


# class InverterModel_V1(BaseV1):
#     __tablename__ = "inverter"

#     index = Column(Integer, primary_key=True, autoincrement=True)
#     InverterNumber = Column(String(255), nullable=False)
#     InverterCertificate = Column(
#         String(255),
#         nullable=False,
#         ForeignKey="inverter_certificate.index",
#     )
#     Details = Column(
#         String(255),
#         nullable=False,
#         ForeignKey="inverter_details.index",
#     )
