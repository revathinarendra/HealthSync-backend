from django.urls import path
from . import views

urlpatterns = [
    path('body-parameters/', views.list_body_parameters),
    path('body-parameters/create/',views.create_body_parameters),
    path('body-parameters/<str:pk>/',views.update_body_parameters),
    path('body-parameters/delete/<str:pk>/', views.delete_body_parameters, name='delete_body_parameters'),
    path('body-parameters/byUser/<str:user_id>/', views.get_body_parameters_by_user, name='get_body_parameters_by_user'),



    path('blood-test/create/',views.create_blood_test_values),
    path('blood-test/',views.list_blood_test_values),
    path('blood-test/<str:pk>/',views.update_blood_test_values),
    path('blood-test/delete/<str:pk>/', views.delete_blood_test_values),


    path('CUE/create/',views.create_complete_urine_examination),
    path('CUE/',views.list_complete_urine_examinations),
    path('CUE/<str:pk>/',views.update_complete_urine_examination),
    path('CUE/delete/<str:pk>/', views.delete_complete_urine_examination),



    path('ESR/create/',views.create_Erythrocyte_sedimentation_rate),
    path('ESR/',views.list_Erythrocyte_sedimentation_rates),
    path('ESR/<str:pk>/',views.update_Erythrocyte_sedimentation_rate),
    path('ESR/delete/<str:pk>/', views.delete_Erythrocyte_sedimentation_rate),


    path('blood-urea/create/', views.create_blood_urea_nitrogen_test),
    path('blood-urea/', views.list_blood_urea_nitrogen_tests),
    path('blood-urea/<str:pk>/', views.update_blood_urea_nitrogen_test),
    path('blood-urea/delete/<str:pk>/', views.delete_blood_urea_nitrogen_test),


    path('lipid-profile/create/', views.create_lipid_profile),
    path('lipid-profile/', views.list_lipid_profiles),
    path('lipid-profile/<str:pk>/', views.update_lipid_profile),
    path('lipid-profile/delete/<str:pk>/', views.delete_lipid_profile),


    path('liver-function-test/create/', views.create_liver_function_test),
    path('liver-function-test/', views.list_liver_function_tests),
    path('liver-function-test/<str:pk>/', views.update_liver_function_test),
    path('liver-function-test/delete/<str:pk>/', views.delete_liver_function_test),


    path('medical-history/create/', views.create_medical_history),
    path('medical-history/', views.list_medical_histories),
    path('medical-history/<str:pk>/', views.update_medical_history),
    path('medical-history/delete/<str:pk>/', views.delete_medical_history),



    path('daily-routine/create/', views.create_daily_routine),
    path('daily-routine/', views.list_daily_routines),
    path('daily-routine/<str:pk>/', views.update_daily_routine),
    path('daily-routine/delete/<str:pk>/', views.delete_daily_routine),


    path('byUserId/<int:user_id>/', views.get_health_data_by_user),

#####category#######
    path('category/create/', views.category_create, name='category_create'),
    path('category/list/', views.category_list, name='category_list'),
    path('category/<str:pk>/', views.category_update, name='category_update'),
    path('category/delete/<str:pk>/', views.category_delete, name='category_delete'),
#####cart#######
    path('cart/create/', views.add_to_cart_create, name='create_cart'),
    path('cart/add-item/', views.add_item_to_cart, name='add_item_to_cart'),
    path('cart/remove-item/<str:item_id>/', views.remove_item_from_cart, name='remove_item_from_cart'),

########test#######
    path('test/create/', views.test_create, name='test_create'),
    path('test/list/', views.test_list, name='test_list'),
    path('test/<str:pk>/', views.test_update, name='test_update'),
    path('test/delete/<str:pk>/', views.test_delete, name='test_delete'),
    



]
