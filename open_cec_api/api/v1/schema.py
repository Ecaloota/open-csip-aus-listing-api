from typing import Any

from pydantic import BaseModel


class SoftwareCommsClient(BaseModel):
    Communication_Device_Name__c: str | None  # TODO ??
    Communication_Manufacturer__c: str | None  # TODO ??
    Communication_Manufacturer_Name__c: str | None  # TODO ??
    Communication_Model_Name__c: str | None  # TODO ??


class InverterCertificateDetails(BaseModel):
    SalesforceInverterCertID: str
    AS3100Tested: bool
    AS4777Tested: bool
    ApplicableStandardsOther: Any | None  # TODO ??
    ApplicableStandards: list[str]  # TODO allowed standards
    ApprovalDate: str  # TODO whenever date
    ApprovingBody: str | None  # TODO ??
    CECApprovedDate: str  # TODO whenever date
    CECApproved: bool
    CertificateNumber: str
    BatteryCertifyingBody: str | None  # TODO ??
    EquipmentCategory: str
    ExpiryDate: str  # TODO whenever date
    BrandName: str
    TradingNames: str
    AgreedtoTermsConditions: bool
    ForTesting: bool
    Software_Communications_Client__c: SoftwareCommsClient
    Software_Communications_Client_2__c: SoftwareCommsClient
    Software_Communications_Client_3__c: SoftwareCommsClient
    Software_Communications_Client_4__c: SoftwareCommsClient
    Software_Communications_Client_5__c: SoftwareCommsClient
    Software_Communications_Client_6__c: SoftwareCommsClient
    Software_Communications_Client_7__c: SoftwareCommsClient
    Software_Communications_Client_8__c: SoftwareCommsClient
    Software_Communications_Client_9__c: SoftwareCommsClient
    Software_Communications_Client_10__c: SoftwareCommsClient


class InverterCertificateApplicationDetails(BaseModel):
    Name: str


class InverterCertificateApplication(BaseModel):
    Details: InverterCertificateApplicationDetails


class InverterCertificateApplicationContactDetails(BaseModel):
    FirstName: str
    LastName: str


class InverterCertificateApplicationContact(BaseModel):
    Details: InverterCertificateApplicationContactDetails


class InverterCertificateApplicationHolderAccountDetails(BaseModel):
    Name: str


class InverterCertificateApplicationHolderAccount(BaseModel):
    Details: InverterCertificateApplicationHolderAccountDetails


class InverterCertificate(BaseModel):
    Details: InverterCertificateDetails
    Application: InverterCertificateApplication
    Contact: InverterCertificateApplicationContact
    ManufacturerCertificateHolderAccount: InverterCertificateApplicationHolderAccount


class InverterDetails(BaseModel):
    Id: str
    Model_Number__c: str
    Series__c: str
    Export_Control__c: Any | None  # TODO ??
    Generation_control__c: Any | None  # TODO ??
    Integrated_Battery_DC_Switch__c: str
    Integrated_PV_DC_Switch__c: str
    Internal_Battery__c: bool
    CECLimitWithinInverterRange: bool
    CECLimitWithinInverterRangeReason: Any | None  # TODO ??
    MultiInverterCombinationsTested: bool
    Nominal_AC_Power_W__c: int
    No_of_Phases__c: int
    PQ_Mode_Cos_Power__c: bool
    PQ_Mode_Fixed_P_Factor__c: bool
    PQ_Mode_Rate_Limit__c: Any | None  # TODO ??
    PQ_Mode_Volt_Balance__c: bool
    PQ_Mode_Volt_Watt__c: bool
    PQ_Mode_Volt_Var__c: bool
    Tested_to_IEC_62116__c: bool
    Inverter_without_Nominal_230_400V_Output__c: bool
    Test_Scenarios__c: Any | None  # TODO ??
    Power_rate_limits_compliant_with_4777_2__c: bool
    Active_Anti_Island_Method__c: str
    VDRT: bool
    Internet_capability_via_LAN_WLAN_Wi_Fi: str
    OnboardCommsPort: str
    PV_Isolator_EESS__c: Any | None  # TODO ??


class Inverter(BaseModel):
    InverterNumber: str
    Details: InverterDetails
    Certificate: InverterCertificate


class InverterList(BaseModel):
    inverters: list[Inverter]
