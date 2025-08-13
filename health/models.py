import datetime 
from django.db import models
from mongoengine import Document, EmbeddedDocument,ReferenceField,StringField, FloatField, DateTimeField, EmbeddedDocumentField, ObjectIdField,IntField, DictField,BooleanField, ListField, EmbeddedDocumentListField
from accounts.models import Account, UserProfile
from bson import ObjectId

# Create your models here.

class BodyParameters(Document):
    #user = ReferenceField(Account, required=True)
    user_id = IntField(required=True)
    dietician_id = IntField()
    stress_level = FloatField()
    # sleep_time = StringField()
    sleep_time = FloatField()
    sleep_quality = StringField()
    height = StringField()
    weight = FloatField()
    bmi = FloatField()
    # viseral_fats = StringField()
    viseral_fats = IntField()
    body_fat = FloatField()
    trunk_fat = FloatField()
    subcutaneous_fat = FloatField()
    muscle = FloatField()
    body_age = FloatField()
    waste_water = StringField()
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

   
    score = FloatField()  # Updated from StringField
    status = StringField()
    components = DictField()  # Updated from models.JSONField

    meta = {'collection': 'body_parameters'}
    



# ####################    BloodTestValues   #######################################
class ThyroidProfile(EmbeddedDocument):
    id =  ObjectIdField(default=lambda:  ObjectId(), primary_key=True)
    thyroid_t3 = FloatField()
    thyroid_t4 = FloatField()
    thyroid_tsh = FloatField()

class BloodTestValues(Document):
    user_id = IntField(required=True)
    dietician_id = IntField()
    date = DateTimeField(required=True)
    vitamin_d_25 = FloatField()
    thyroid_profile = EmbeddedDocumentField(ThyroidProfile)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'blood_test_values'}



# ####################    CompleteUrineExamination   #######################################
class PhysicalExamination(EmbeddedDocument):
    id =  ObjectIdField(default=lambda:  ObjectId(), primary_key=True)
    colour =  StringField()
    appearance =  StringField()

class ChemicalExamination(EmbeddedDocument):
    id =  ObjectIdField(default=lambda:  ObjectId(), primary_key=True)
    reaction_and_ph =  StringField()
    specific_gravity =  StringField()
    protein =  StringField()
    glucose =  StringField()
    blood =  StringField()
    ketones =  StringField()
    bilirubin =  StringField()
    leucocytes =  StringField()
    nitrites =  StringField()
    urobilinogen =  StringField()

class MicroscopicExamination(EmbeddedDocument):
    id =  ObjectIdField(default=lambda:  ObjectId(), primary_key=True)
    pus_cells =  StringField()
    epithelial_cells =  StringField()
    rbc =  StringField()
    casts =  StringField()
    crystals =  StringField()
    others =  StringField()

class CompleteUrineExamination(Document):
    user_id =IntField(required=True)
    dietician_id = IntField()
    physical_examination = EmbeddedDocumentField(PhysicalExamination)
    chemical_examination = EmbeddedDocumentField(ChemicalExamination)
    microscopic_examination =EmbeddedDocumentField(MicroscopicExamination)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'complete_urine_examination'}





# ####################    ErythrocyteSedimentationRate   #######################################
class Hemogram(EmbeddedDocument):
    id = ObjectIdField(default=lambda: ObjectId(), primary_key=True)
    hemoglobin = FloatField()
    pcv_hct = FloatField()
    total_rbc_count = FloatField()
    mcv = FloatField()
    mch = FloatField()
    mchc = FloatField()
    rdw_cv = FloatField()
    mpv = FloatField()
    total_wbc_count = FloatField()
    platelet_count = FloatField()
    neutrophils = FloatField()
    lymphocytes = FloatField()
    eosinophils = FloatField()
    monocytes = FloatField()
    basophils = FloatField()
    absolute_neutrophil_count = FloatField()
    absolute_lymphocyte_count = FloatField()
    absolute_eosinophil_count = FloatField()
    absolute_monocyte_count = FloatField()
    absolute_basophil_count = FloatField()
    neutrophil_lymphocyte_ratio = FloatField()

# Peripheral Blood Smear Embedded Document
class PeripheralBloodSmear(EmbeddedDocument):
    id = ObjectIdField(default=lambda: ObjectId(), primary_key=True)
    rbc = StringField()
    wbc = StringField()
    platelets = StringField()

# ESR Master Document
class ErythrocyteSedimentationRate(Document):
    user_id = IntField(required=True)
    dietician_id = IntField()
    hemogram = EmbeddedDocumentField(Hemogram)
    peripheral_blood_smear = EmbeddedDocumentField(PeripheralBloodSmear)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'erythrocyte_sedimentation_rate'}



# ####################    BloodUreaNitrogenTest   #######################################
class BloodUreaNitrogen(EmbeddedDocument):
    id = ObjectIdField(default=lambda: ObjectId(), primary_key=True)
    urea = FloatField()

class CalciumSerum(EmbeddedDocument):
    id = ObjectIdField(default=lambda: ObjectId(), primary_key=True)
    calcium = FloatField()

class CreatinineSerum(EmbeddedDocument):
    id = ObjectIdField(default=lambda: ObjectId(), primary_key=True)
    creatinine = FloatField()

class GlycosylatedHemoglobin(EmbeddedDocument):
    id = ObjectIdField(default=lambda: ObjectId(), primary_key=True)
    glycosylated_hemoglobin = FloatField()
    estimated_average_glucose = FloatField()

class VitaminB12(EmbeddedDocument):
    id = ObjectIdField(default=lambda: ObjectId(), primary_key=True)
    vitamin_b12 = FloatField()

class ElectrolytesSerum(EmbeddedDocument):
    id = ObjectIdField(default=lambda: ObjectId(), primary_key=True)
    sodium = FloatField()
    potassium = FloatField()
    chloride = FloatField()

class Ferritin(EmbeddedDocument):
    id = ObjectIdField(default=lambda: ObjectId(), primary_key=True)
    ferritin = FloatField()

class IronWithTIBC(EmbeddedDocument):
    id = ObjectIdField(default=lambda: ObjectId(), primary_key=True)
    iron = FloatField()
    tibc = FloatField()

class BloodUreaNitrogenTest(Document):
    user_id = IntField(required=True)
    dietician_id = IntField()
    blood_urea_nitrogen =EmbeddedDocumentField(BloodUreaNitrogen)
    calcium_serum = EmbeddedDocumentField(CalciumSerum)
    creatinine_serum = EmbeddedDocumentField(CreatinineSerum)
    glycosylated_hemoglobin = EmbeddedDocumentField(GlycosylatedHemoglobin)
    vitamin_b12 = EmbeddedDocumentField(VitaminB12)
    electrolytes_serum = EmbeddedDocumentField(ElectrolytesSerum)
    ferritin = EmbeddedDocumentField(Ferritin)
    iron_with_tibc = EmbeddedDocumentField(IronWithTIBC)

    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'blood_urea_nitrogen_test'}


# ####################    LipidProfile   #######################################
class LipidProfile(Document):
    user_id = IntField(required=True)
    dietician_id = IntField()
    total_cholesterol = FloatField()
    hdl_cholesterol = FloatField()
    vldl_cholesterol = FloatField()
    ldl_cholesterol = FloatField()
    triglycerides = FloatField()
    chol_hdl_ratio = FloatField()
    ldl_hdl_ratio = FloatField()

    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'lipid_profile'}



# ####################    LiverFunctionTest   #######################################
class PhosphorusSerum(EmbeddedDocument):
    id = ObjectIdField(default=lambda: ObjectId(), primary_key=True)
    phosphorus = FloatField()

class TransferrinSaturation(EmbeddedDocument):
    id = ObjectIdField(default=lambda: ObjectId(), primary_key=True)
    transferrin_saturation_index = FloatField()

class LiverFunctionTest(Document):
    user_id = IntField(required=True)
    dietician_id = IntField()
    total_bilirubin = FloatField()
    direct_bilirubin = FloatField()
    indirect_bilirubin = FloatField()
    alt = FloatField()
    ast = FloatField()
    alp = FloatField()
    gamma_gt = FloatField()
    total_protein = FloatField()
    albumin = FloatField()
    globulin = FloatField()
    a_g_ratio = FloatField()
    ast_alt_ratio = FloatField()

    phosphorus_serum = EmbeddedDocumentField(PhosphorusSerum)
    transferrin_saturation = EmbeddedDocumentField(TransferrinSaturation)

    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'liver_function_test'}



# ####################    MedicalHistory   #######################################
class MedicalHistory(Document):
    user_id = IntField(required=True)
    dietician_id = IntField()
    alcohol_smoking = StringField()
    food_allergies = StringField()
    any_other_health_concerns = StringField()
    special_mentions = StringField()
    current_medication = StringField()
    father_side_medical_details = StringField()
    mother_side_medical_details = StringField()

    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'medical_history'}



# ####################    DailyRoutine   #######################################
class DailyRoutine(Document):
    user_id = IntField(required=True)
    dietician_id = IntField()
    water_intake = FloatField()
    sleep_time = StringField()
    sleep_quality = StringField()
    wakeup_time = StringField()
    morning_beverages = StringField()
    breakfast_time = StringField()
    breakfast_type = StringField()
    mid_morning_snacks = StringField()
    lunch_time = StringField()
    lunch_type = StringField()
    evening_snacks = StringField()
    dinner_time = StringField()
    dinner_type = StringField()
    mid_night_snacks = StringField()
    digestion_info = StringField()
    frequency_of_eat_out = StringField()

    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'daily_routine'}


    
# -------------------------
# Category Model
# -------------------------
class Category(Document):
    name = StringField(required=True, unique=True)
    meta = {'collection': 'categories'}


# -------------------------
# Parameter (Embedded inside Test)
# -------------------------
class Parameter(EmbeddedDocument):
    name = StringField(required=True)


# -------------------------
# FAQ (Embedded inside Test)
# -------------------------
class FAQ(EmbeddedDocument):
    question = StringField()
    answer = StringField()


# -------------------------
# Test Model
# -------------------------

class Test(Document):
    testName = StringField(required=True)
    testCode = StringField
    price = FloatField(required=True)
    specialInstruction = StringField(default='No special preparation required')
    reportFrequency = StringField(default='Daily')
    sampleReportLink = StringField()
    homeCollectionAvailable = BooleanField(default=True)
    labVisitAvailable = BooleanField(default=True)
    applicableForHomeCollectionOnly = BooleanField(default=True)

    overview = StringField()
    purpose = StringField()
    whatItMeasures = StringField()
    preparations = StringField()
    resultInterpretation = StringField()

    parametersCovered_count = IntField(default=0) 
    #parametersCovered_list = EmbeddedDocumentField(Parameter)
    parametersCovered_list = ListField(EmbeddedDocumentField(Parameter))


    faqs = ListField(EmbeddedDocumentField(FAQ))

    category = ReferenceField(Category, required=False)

    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'tests'}


# -------------------------
# CartItem (Embedded inside AddToCart)
# -------------------------
class CartItem(EmbeddedDocument):
    test = ReferenceField(Test, required=True)
    testName = StringField()
    parameterCount = IntField()
    quantity = IntField(default=1)
    price = FloatField(required=True)


# -------------------------
# Cart Model
# -------------------------
class Cart(Document):
    user_id = IntField(required=True)
    items = ListField(EmbeddedDocumentField(CartItem))

    subTotal = FloatField(default=0)
    total = FloatField(default=0)
    netPayableAmount = FloatField(default=0)

    created_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'add_to_cart'}

    def clean(self):
        """Auto-calculate totals before saving"""
        try:
            self.subTotal = sum(item.test.price * item.quantity for item in self.items)
            self.total = self.subTotal
            self.netPayableAmount = self.total  # Can apply discounts/coupons later
        except Exception as e:
            raise ValueError(f"Error calculating totals: {str(e)}")


# -------------------------
# Appointment Model
# -------------------------
class Appointment(Document):
    user_id = IntField(required=True)
    dietician_id = IntField(required=True)
    appointment_date = DateTimeField
    appointment_time = StringField
    mode = StringField(choices=["Online", "In-person"])
    status = StringField(choices=["Scheduled", "Completed", "Cancelled", "Rescheduled"], default="Scheduled")
    notes = StringField()

    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'appointment'}


# -------------------------
# Payment Model
# -------------------------

class Payment(Document):
    user_id = IntField(required=True)
    test_booking_id = StringField(required=True)
    amount = FloatField(required=True)
    payment_method = StringField(choices=["UPI", "Card", "Cash", "NetBanking"])
    status = StringField(choices=["Paid", "Pending", "Failed"], default="Pending")
    transaction_id = StringField()

    timestamp = DateTimeField(default=datetime.datetime.utcnow)

    meta = {'collection': 'payment'}