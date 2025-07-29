from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import *
from datetime import datetime
from utils.health_score import calculate_health_score

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
        return Response({'message': 'Liver Function Test saved successfully.',
         "data": serializer.data}, status=status.HTTP_201_CREATED)
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
        return Response({'message': 'Medical History saved successfully.',
         "data": serializer.data}, status=status.HTTP_201_CREATED)
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
        return Response({"message": "Daily routine saved successfully.",
         "data": serializer.data}, status=status.HTTP_201_CREATED)
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
