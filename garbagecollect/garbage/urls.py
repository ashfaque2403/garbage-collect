from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.LoginView,name='login'),
    path('register/',views.register_view,name='register'),
    path('logout/',views.logout_view,name='logout'),
    path('thanks/',views.thanks,name='add-thanks'),
    # path('addgarbagecollector/',views.AddGarbageCollector,name='add-garbage-collector'),
    path('viewcomplaint/',views.ViewComplaint,name='view-complaint'),
    path('addingdriver/', views.adddriver, name='add-driver-user'),
    path('addgarbagecollector/', views.addgarbagecollector, name='add-garbage-collector'),
    path('addcomplaint/',views.AddComplaint,name='add-complaint'),
    path('complete',views.CompleteCustomerProfile,name='complete'),
    path('addcompanyadmin/',views.AddCompanyAdmin,name='add-company-admin'),
    path('removeadmin/',views.RemoveAdmin,name='remove-admin'),
    path('removeadminbutton/<int:id>',views.delete_data,name='remove-admin-button'),
    path('driverlist/',views.DriverList,name='driver-list'),
    path('removedriver/<int:id>',views.RemoveDriver,name='remove-driver'),
    path('garbagelist/',views.CollectorList,name='garbage-collector'),
    path('removegarbagelist/<int:id>',views.RemoveCollectorList,name='remove-garbage-collector'),
    path('reply/', views.ViewReplyComplaint, name='view-reply-complaint'),
    path('reply_complaint/<int:complaint_id>/', views.reply_complaint, name='reply_complaint'),
    path('payment/create/', views.PaymentReportCreateView, name='payment_report_create'),
    path('customers/',views.CustomerDetails,name='customer-details'),
    path('garbage/collected/',views.GarbageReport,name='garbage-report'),
    path('payment/collected/view/',views.ViewPayment,name='payment-report-view'),
    path('customer/payment/collected/view/',views.CustomerViewPayment,name='payment-customer-view'),
    path('garbage/collected/view/',views.ViewGarbage,name='garbage-report-view'),
    

]
