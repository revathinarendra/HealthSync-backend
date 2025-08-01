from rest_framework_mongoengine import serializers
# from .models import BodyParameters, BloodTestValues,ThyroidProfile,
from .models import *


# #################Body parameters############
class BodyParametersSerializer(serializers.DocumentSerializer):
    class Meta:
        model = BodyParameters
        fields = '__all__'
        # read_only_fields = ['score', 'status', 'components']



# ################Blood test##################
class ThyroidProfileSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = ThyroidProfile
        fields='__all__'

class BloodTestValuesSerializer(serializers.DocumentSerializer):
    thyroid_profile = ThyroidProfileSerializer(required=False)
    class Meta:
        model= BloodTestValues
        fields='__all__'



# ####################### cue ##################
class PhysicalExaminationSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = PhysicalExamination
        fields='__all__'
class ChemicalExaminationSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = ChemicalExamination
        fields='__all__'
class MicroscopicExaminationSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = MicroscopicExamination
        fields='__all__'

class CompleteUrineExaminationSerializer(serializers.DocumentSerializer):
    physical_examination = PhysicalExaminationSerializer(required=False)
    chemical_examination = ChemicalExaminationSerializer(required=False)
    microscopic_examination = MicroscopicExaminationSerializer(required=False)
    class Meta:
        model= CompleteUrineExamination
        fields='__all__'



# ####################### ESR ##################
class HemogramSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Hemogram
        fields='__all__'
class PeripheralBloodSmearSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = PeripheralBloodSmear
        fields='__all__'

class ErythrocyteSedimentationRateSerializer(serializers.DocumentSerializer):
    hemogram = HemogramSerializer(required=False)
    peripheral_blood_smear = PeripheralBloodSmearSerializer(required=False)
    class Meta:
        model= ErythrocyteSedimentationRate
        fields='__all__'




# ######################## BloodUreaNitrogenTest    ###########

class BloodUreaNitrogenSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = BloodUreaNitrogen
        fields = '__all__'

class CalciumSerumSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = CalciumSerum
        fields = '__all__'

class CreatinineSerumSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = CreatinineSerum
        fields = '__all__'

class GlycosylatedHemoglobinSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = GlycosylatedHemoglobin
        fields = '__all__'

class VitaminB12Serializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = VitaminB12
        fields = '__all__'

class ElectrolytesSerumSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = ElectrolytesSerum
        fields = '__all__'

class FerritinSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Ferritin
        fields = '__all__'

class IronWithTIBCSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = IronWithTIBC
        fields = '__all__'

class BloodUreaNitrogenTestSerializer(serializers.DocumentSerializer):
    blood_urea_nitrogen = BloodUreaNitrogenSerializer(required=False)
    calcium_serum = CalciumSerumSerializer(required=False)
    creatinine_serum = CreatinineSerumSerializer(required=False)
    glycosylated_hemoglobin = GlycosylatedHemoglobinSerializer(required=False)
    vitamin_b12 = VitaminB12Serializer(required=False)
    electrolytes_serum = ElectrolytesSerumSerializer(required=False)
    ferritin = FerritinSerializer(required=False)
    iron_with_tibc = IronWithTIBCSerializer(required=False)

    class Meta:
        model = BloodUreaNitrogenTest
        fields = '__all__'



# ######################## LipidProfile    ###########
class LipidProfileSerializer(serializers.DocumentSerializer):
    class Meta:
        model = LipidProfile
        fields = '__all__'



# ######################## LiverFunctionTest    ###########
class PhosphorusSerumSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = PhosphorusSerum
        fields = '__all__'


class TransferrinSaturationSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = TransferrinSaturation
        fields = '__all__'


class LiverFunctionTestSerializer(serializers.DocumentSerializer):
    phosphorus_serum = PhosphorusSerumSerializer(required=False)
    transferrin_saturation = TransferrinSaturationSerializer(required=False)

    class Meta:
        model = LiverFunctionTest
        fields = '__all__'




# ######################## MedicalHistory    ###########
class MedicalHistorySerializer(serializers.DocumentSerializer):
    class Meta:
        model = MedicalHistory
        fields = '__all__'


# ####################    DailyRoutine   #######################################
class DailyRoutineSerializer(serializers.DocumentSerializer):
    class Meta:
        model = DailyRoutine
        fields = '__all__'




# -------------------------
# Category Serializer
# -------------------------
class CategorySerializer(serializers.DocumentSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# -------------------------
# Parameter (Embedded)
# -------------------------
class ParameterSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = Parameter
        fields = '__all__'


# -------------------------
# FAQ (Embedded)
# -------------------------
class FAQSerializer(serializers.EmbeddedDocumentSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


# -------------------------
# Test Serializer
# -------------------------
class TestSerializer(serializers.DocumentSerializer):
    parametersCovered_list = ParameterSerializer(required=False)
    faqs = FAQSerializer(required=False,many=True)
    #category = CategorySerializer()

    class Meta:
        model = Test
        fields = '__all__'


# -------------------------
# CartItem (Embedded)
# -------------------------
class CartItemSerializer(serializers.EmbeddedDocumentSerializer):

    class Meta:
        model = CartItem
        fields = '__all__'


# -------------------------
# Cart Serializer
# -------------------------
class CartSerializer(serializers.DocumentSerializer):
    items = CartItemSerializer(required=False)

    class Meta:
        model = Cart
        fields = '__all__'

class AppointmentSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class PaymentSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Payment
        fields = '__all__'