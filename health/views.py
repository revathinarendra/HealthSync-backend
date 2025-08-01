from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import *
from datetime import datetime
from utils.health_score import calculate_health_score
from mongoengine.errors import DoesNotExist as RefDoesNotExist

# from .models import BodyParameters, BloodTestValues
from .serializers import BodyParametersSerializer, BloodTestValuesSerializer,CompleteUrineExaminationSerializer, ErythrocyteSedimentationRateSerializer, BloodUreaNitrogenTestSerializer,LipidProfileSerializer,LiverFunctionTestSerializer,MedicalHistorySerializer,DailyRoutineSerializer

# #################Body parameters############
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_body_parameters(request):
    serializer = BodyParametersSerializer(data=request.data)
    if serializer.is_valid():
        body_param = serializer.save()

        # Prepare input for health score calculation
        body_data = {
            'height': body_param.height,
            'weight': body_param.weight,
            'BMI': body_param.bmi,
            'body_fat': body_param.body_fat,
            'muscle': body_param.muscle,
            'viseral_fats': body_param.viseral_fats,
            'sleep_time': body_param.sleep_time,
            'sleep_quality': body_param.sleep_quality,
            'stress_level': body_param.stress_level,
            'body_age': body_param.body_age,
            'waste_water': body_param.waste_water,
        }

        result = calculate_health_score(body_data)
        print(result)
        # Update model instance with score data
       
        if 'error' not in result:
            body_param.score = result['score']  # float
            body_param.status = result['status']  # string
        else:
            body_param.score = 0.0
            body_param.status = 'Error'
        # components = result.get('components', {})
        # body_param.components = components
        body_param.save()

        return Response({
            'message': 'Body parameters saved successfully.',
            'data': BodyParametersSerializer(body_param).data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_body_parameters(request):
    body_params = BodyParameters.objects.all()
    serializer = BodyParametersSerializer(body_params, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_body_parameters_by_user(request, user_id):
    print("Called with user_id:", user_id)
    body_params = BodyParameters.objects.filter(user_id=user_id)
    print("Queryset count:", body_params.count())
    serializer = BodyParametersSerializer(body_params, many=True)
    return Response(serializer.data, status=200)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_body_parameters(request, pk):
    try:
        body_param = BodyParameters.objects.get(pk=pk)
    except BodyParameters.DoesNotExist:
        return Response({'error': 'Body Parameters not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BodyParametersSerializer(body_param, data=request.data, partial=True)
    if serializer.is_valid():
        body_param.updated_at = datetime.utcnow()
        serializer.save()
        return Response({
        'message': 'Body Parameters updated successfully.',
        'data': BodyParametersSerializer(body_param).data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_body_parameters(request, pk):
    try:
        body_param = BodyParameters.objects.get(pk=pk)
        body_param.delete()
        return Response({'message': 'Body Parameters deleted successfully.'}, status=status.HTTP_200_OK)
    except BodyParameters.DoesNotExist:
        return Response({'error': 'Body Parameters not found'}, status=status.HTTP_404_NOT_FOUND)





# ################Blood test##################


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_blood_test_values(request):
    serializer = BloodTestValuesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Blood Test values saved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_blood_test_values(request):
    blood_tests= BloodTestValues.objects.all()
    serializer= BloodTestValuesSerializer(blood_tests, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_blood_test_values(request,pk):
    try:
        blood_test= BloodTestValues.objects.get(pk=pk)
    except BloodTestValues.DoesNotExist:
        return Response({'error': 'Blood Test Values not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = BloodTestValuesSerializer(blood_test, data=request.data, partial=True)
    if serializer.is_valid():
        blood_test.updated_at = datetime.utcnow()
        serializer.save()
        return Response({'message': 'Blood Test Values updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_blood_test_values(request, pk):
    try:
        blood_test= BloodTestValues.objects.get(pk=pk)
        blood_test.delete()
        return Response({'message': 'Blood test deleted successfully.'}, status=status.HTTP_200_OK)
    except BloodTestValues.DoesNotExist:
        return Response({'error': 'Blood test not found'}, status=status.HTTP_404_NOT_FOUND)



# ####################### cue ##################
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_complete_urine_examination(request):
    serializer = CompleteUrineExaminationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"CUE saved successfully.",
         "data": serializer.data},status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_complete_urine_examinations(request):
    cue= CompleteUrineExamination.objects.all()
    serializer= CompleteUrineExaminationSerializer(cue, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_complete_urine_examination(request,pk):
    try:
        cue= CompleteUrineExamination.objects.get(pk=pk)
    except CompleteUrineExamination.DoesNotExist:
        return Response({'error': 'CUE not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = CompleteUrineExaminationSerializer(cue, data=request.data, partial=True)
    if serializer.is_valid():
        cue.updated_at = datetime.utcnow()
        serializer.save()
        return Response({'message': 'CUE updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_complete_urine_examination(request, pk):
    try:
        cue= CompleteUrineExamination.objects.get(pk=pk)
        cue.delete()
        return Response({'message': 'CUE deleted successfully.'}, status=status.HTTP_200_OK)
    except CompleteUrineExamination.DoesNotExist:
        return Response({'error': 'CUE not found'}, status=status.HTTP_404_NOT_FOUND)


# ####################### ESR ##################
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_Erythrocyte_sedimentation_rate(request):
    serializer = ErythrocyteSedimentationRateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"ESR saved successfully.",
         "data": serializer.data},status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_Erythrocyte_sedimentation_rates(request):
    esr= ErythrocyteSedimentationRate.objects.all()
    serializer= ErythrocyteSedimentationRateSerializer(esr, many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_Erythrocyte_sedimentation_rate(request,pk):
    try:
        esr= ErythrocyteSedimentationRate.objects.get(pk=pk)
    except ErythrocyteSedimentationRate.DoesNotExist:
        return Response({'error': 'ESR not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ErythrocyteSedimentationRateSerializer(esr, data=request.data, partial=True)
    if serializer.is_valid():
        esr.updated_at = datetime.utcnow()
        serializer.save()
        return Response({'message': 'ESr updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_Erythrocyte_sedimentation_rate(request, pk):
    try:
        esr= ErythrocyteSedimentationRate.objects.get(pk=pk)
        esr.delete()
        return Response({'message': 'ESR deleted successfully.'}, status=status.HTTP_200_OK)
    except ErythrocyteSedimentationRate.DoesNotExist:
        return Response({'error': 'ESR not found'}, status=status.HTTP_404_NOT_FOUND)


# ######################## BloodUreaNitrogenTest    ###########
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_blood_urea_nitrogen_test(request):
    serializer = BloodUreaNitrogenTestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Blood Urea Nitrogen Test saved successfully.",
         "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_blood_urea_nitrogen_tests(request):
    tests = BloodUreaNitrogenTest.objects.all()
    serializer = BloodUreaNitrogenTestSerializer(tests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_blood_urea_nitrogen_test(request, pk):
    try:
        test = BloodUreaNitrogenTest.objects.get(pk=pk)
    except BloodUreaNitrogenTest.DoesNotExist:
        return Response({'error': 'Blood Urea Nitrogen Test not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BloodUreaNitrogenTestSerializer(test, data=request.data, partial=True)
    if serializer.is_valid():
        test.updated_at = datetime.utcnow()
        serializer.save()
        return Response({'message': 'Blood Urea Nitrogen Test updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_blood_urea_nitrogen_test(request, pk):
    try:
        test = BloodUreaNitrogenTest.objects.get(pk=pk)
        test.delete()
        return Response({'message': 'Blood Urea Nitrogen Test deleted successfully.'}, status=status.HTTP_200_OK)
    except BloodUreaNitrogenTest.DoesNotExist:
        return Response({'error': 'Blood Urea Nitrogen Test not found'}, status=status.HTTP_404_NOT_FOUND)



# ######################## LipidProfile    ###########
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_lipid_profile(request):
    serializer = LipidProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Lipid Profile saved successfully.',
         "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_lipid_profiles(request):
    data = LipidProfile.objects.all()
    serializer = LipidProfileSerializer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_lipid_profile(request, pk):
    try:
        obj = LipidProfile.objects.get(pk=pk)
    except LipidProfile.DoesNotExist:
        return Response({'error': 'Lipid Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = LipidProfileSerializer(obj, data=request.data, partial=True)
    if serializer.is_valid():
        obj.updated_at = datetime.utcnow()
        serializer.save()
        return Response({'message': 'Lipid Profile updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_lipid_profile(request, pk):
    try:
        obj= LipidProfile.objects.get(pk=pk)
        obj.delete()
        return Response({'message': 'Lipid Profile deleted successfully.'}, status=status.HTTP_200_OK)
    except LipidProfile.DoesNotExist:
        return Response({'error': 'Lipid Profile not found'}, status=status.HTTP_404_NOT_FOUND)


# ######################## LiverFunctionTest    ###########
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_liver_function_test(request):
    serializer = LiverFunctionTestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Liver Function Test saved successfully.',"data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_liver_function_tests(request):
    data = LiverFunctionTest.objects.all()
    serializer = LiverFunctionTestSerializer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_liver_function_test(request, pk):
    try:
        obj = LiverFunctionTest.objects.get(pk=pk)
    except LiverFunctionTest.DoesNotExist:
        return Response({'error': 'Liver Function Test not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = LiverFunctionTestSerializer(obj, data=request.data, partial=True)
    if serializer.is_valid():
        obj.updated_at = datetime.utcnow()
        serializer.save()
        return Response({'message': 'Liver Function Test updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_liver_function_test(request, pk):
    try:
        obj= LiverFunctionTest.objects.get(pk=pk)
        obj.delete()
        return Response({'message': 'Liver Function Test deleted successfully.'}, status=status.HTTP_200_OK)
    except LiverFunctionTest.DoesNotExist:
        return Response({'error': 'Liver Function Test not found'}, status=status.HTTP_404_NOT_FOUND)


# ######################## MedicalHistory    ###########
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_medical_history(request):
    serializer = MedicalHistorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Medical History saved successfully.',"data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_medical_histories(request):
    data = MedicalHistory.objects.all()
    serializer = MedicalHistorySerializer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_medical_history(request, pk):
    try:
        obj = MedicalHistory.objects.get(pk=pk)
    except MedicalHistory.DoesNotExist:
        return Response({'error': 'Medical History not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MedicalHistorySerializer(obj, data=request.data, partial=True)
    if serializer.is_valid():
        obj.updated_at = datetime.utcnow()
        serializer.save()
        return Response({'message': 'Medical History updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_medical_history(request, pk):
    try:
        obj= MedicalHistory.objects.get(pk=pk)
        obj.delete()
        return Response({'message': 'Medical History deleted successfully.'}, status=status.HTTP_200_OK)
    except MedicalHistory.DoesNotExist:
        return Response({'error': 'Medical History Test not found'}, status=status.HTTP_404_NOT_FOUND)




# ####################    DailyRoutine   #######################################
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_daily_routine(request):
    serializer = DailyRoutineSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Daily routine saved successfully.","data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_daily_routines(request):
    routines = DailyRoutine.objects.all()
    serializer = DailyRoutineSerializer(routines, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_daily_routine(request, pk):
    try:
        obj = DailyRoutine.objects.get(pk=pk)
    except DailyRoutine.DoesNotExist:
        return Response({'error': 'Daily routine not found'}, status=status.HTTP_404_NOT_FOUND)
    
    obj.updated_at = datetime.utcnow()
    serializer = DailyRoutineSerializer(obj, data=request.data, partial=True)
    if serializer.is_valid():
        obj.updated_at = datetime.utcnow()
        serializer.save()
        return Response({'message': 'Daily routine updated successfully.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_daily_routine(request, pk):
    try:
        obj= DailyRoutine.objects.get(pk=pk)
        obj.delete()
        return Response({'message': 'Daily routine deleted successfully.'}, status=status.HTTP_200_OK)
    except DailyRoutine.DoesNotExist:
        return Response({'error': 'Daily routine Test not found'}, status=status.HTTP_404_NOT_FOUND)




MODEL_SERIALIZER_MAPPING = {
    'body_parameters': (BodyParameters, BodyParametersSerializer),
    'blood_test': (BloodTestValues, BloodTestValuesSerializer),
    'urine_examination': (CompleteUrineExamination, CompleteUrineExaminationSerializer),
    'esr': (ErythrocyteSedimentationRate, ErythrocyteSedimentationRateSerializer),
    'bun_test': (BloodUreaNitrogenTest, BloodUreaNitrogenTestSerializer),
    'lipid_profile': (LipidProfile, LipidProfileSerializer),
    'liver_function': (LiverFunctionTest, LiverFunctionTestSerializer),
    'medical_history': (MedicalHistory, MedicalHistorySerializer),
    'daily_routine': (DailyRoutine, DailyRoutineSerializer),
}


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_health_data_by_user(request, user_id):
    model_type = request.GET.get('type')

    if not model_type:
        return Response({'success': False, 'message': 'Query parameter "type" is required.'}, status=status.HTTP_400_BAD_REQUEST)

    model_info = MODEL_SERIALIZER_MAPPING.get(model_type)
    if not model_info:
        return Response({'success': False, 'message': f'Invalid type: {model_type}'}, status=status.HTTP_400_BAD_REQUEST)

    model_class, serializer_class = model_info

    try:
        records = model_class.objects.filter(user_id=int(user_id)).order_by('-created_at')
        serializer = serializer_class(records, many=True)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'success': False, 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    






    
##################test#######################
from .serializers import TestSerializer
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated]) 
def test_create(request):
    serializer = TestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated]) 
def test_list(request):
    tests = Test.objects.all()
    serializer = TestSerializer(tests, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def test_update(request, pk):
    try:
        test = Test.objects.get(id=pk)
    except Test.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TestSerializer(test, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def test_delete(request, pk):
    try:
        test = Test.objects.get(id=pk)
    except Test.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    test.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


###############category#######################
from .serializers import CategorySerializer
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated]) 
def category_create(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def category_update(request, pk):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(category, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def category_delete(request, pk):
    try:
        category = Category.objects.get(id=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


#####################cart#######################
from .serializers import CartSerializer

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_to_cart_create(request):
    serializer = CartSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()#either updates or creates a new cart
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# # ######## CART VIEW ######


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_item_to_cart(request):
    user_id = request.data.get('user_id', request.user.id)  # Use authenticated user ID if not provided
    test_id = request.data.get('test_id')
    quantity = request.data.get('quantity', 1)
    if not test_id:
        return Response({"detail": "Test ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not isinstance(quantity, int) or quantity<=0:
        return Response({"detail": "Quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        test_obj= Test.objects.get(id=test_id)
    except Test.DoesNotExist:
        return Response({"detail": "Test not found."}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        cart= Cart.objects(user_id=user_id).first()
    except Exception as e:
        return Response({"detail": f"Error retrieving or creating cart: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Remove any broken references in cart before processing
    valid_items = []
    for item in cart.items:
        try:
            _ = item.test.id  # Triggers dereference
            valid_items.append(item)
        except RefDoesNotExist:
            continue
    cart.items = valid_items

    # Check if item already in cart
    cart_item_found = None
    for item in cart.items:
        try:
            if str(item.test.id) == str(test_id):  # Safely compare ObjectId and str
                cart_item_found = item
                break
        except RefDoesNotExist:
            continue
        except Exception as e:
            return Response({"detail": f"Error reading cart item test reference: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if cart_item_found:
        item.quantity+= quantity

    else:
        try:
            new_cart_item = CartItem(
                test=test_obj,
                testName=test_obj.testName,
                parameterCount=test_obj.parametersCovered_count,
                quantity=quantity,
            )
        except AttributeError:
            return Response({"detail": "Missing required fields in test object."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        cart.items.append(new_cart_item)

    try:
        cart.save()  # Will trigger `clean()` safely now
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"detail": "Error saving cart."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_to_cart_list(request):
    carts=Cart.objects.filter(user_id=request.user.id)
    serializer= CartSerializer(carts, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_to_cart_update(request, pk):
    try:
        # Ensure only the authenticated user's cart can be updated
        cart = Cart.objects.get(id=pk, user_id=request.user.id)
    except Cart.DoesNotExist:
        return Response({"detail": "Cart not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CartSerializer(cart, data=request.data, partial=True)
    if serializer.is_valid():
        # Ensure user_id cannot be changed during update
        if 'user_id' in serializer.validated_data and serializer.validated_data['user_id'] != request.user.id:
            return Response({"detail": "Cannot change user_id of a cart."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save() # Cart's clean method should update totals
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated]) # Authentication restored
def add_to_cart_delete(request,pk):
    try:
        cart=Cart.objects.get(user_id=request.user.id)
    except Cart.DoesNotExist:
        return Response({"detail": "Cart not found or you don't have permission."}, status=status.HTTP_404_NOT_FOUND)
    
    cart.delete()
    return Response({"detail": "Cart deleted successfully."}, status=status.HTTP_204_NO_CONTENT)





@api_view(['POST']) # Using POST for state change, or DELETE if you pass item_id in URL
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated]) # Authentication restored
def remove_item_from_cart(request):
    """
    Removes a specified Test from the authenticated user's cart, or decreases its quantity.
    Expected request.data: {"test_id": "test_mongo_object_id", "quantity": 1 (optional)}
    If quantity is not provided, removes entire item.
    User ID is inferred from the authenticated user.
    """
    user_id = request.user.id # Get user ID from authenticated user

    test_id_to_remove = request.data.get('test_id')
    quantity_to_remove = request.data.get('quantity') # Optional: if not provided, remove all

    if not test_id_to_remove:
        return Response({"detail": "test_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    if quantity_to_remove is not None and (not isinstance(quantity_to_remove, int) or quantity_to_remove <= 0):
        return Response({"detail": "Quantity to remove must be a positive integer or omitted."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Get the user's cart
        cart = Cart.objects.get(user_id=user_id)
    except Cart.DoesNotExist:
        return Response({"detail": "Cart not found for this user."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e: # Catch potential errors if test_id is not a valid ObjectId for filtering
        return Response({"detail": f"Error retrieving cart: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Find the cart item to remove/update
    item_index_to_remove = -1
    for i, item in enumerate(cart.items):
        if str(item.test.id) == test_id_to_remove: # Convert ObjectId to string for comparison
            item_index_to_remove = i
            break

    if item_index_to_remove == -1:
        return Response({"detail": "Test not found in cart."}, status=status.HTTP_404_NOT_FOUND)

    cart_item = cart.items[item_index_to_remove]

    if quantity_to_remove is not None and quantity_to_remove > 0 and cart_item.quantity > quantity_to_remove:
        # Decrease quantity
        cart_item.quantity -= quantity_to_remove
    else:
        # Remove the entire item
        cart.items.pop(item_index_to_remove)

    try:
        cart.save() # This will trigger the clean() method to recalculate totals
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"detail": f"Error saving cart: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




