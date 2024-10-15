from django.shortcuts import render
from dashboard.models import MobileBanking

# Create your views here.
def home(request):
    # Get all the data
    data=MobileBanking.objects.all()
    total_responses=data.count()
    mobile_banking_users=data.filter(UseMobileBankingApps='Yes').count()
    female_respondents=((data.filter(Gender='Female').count())/(total_responses))*100
    male_respondents=((data.filter(Gender='Male')).count()/(total_responses))*100
    if total_responses>0:
        adoption_rate=(mobile_banking_users/total_responses)*100
    else:
        adoption_rate=0
    context={'adoption_rate':adoption_rate,'total_responses':total_responses,'female_respondents':female_respondents,'male_respondents':male_respondents}
    return render(request,'dashboard/home.html',context)

def dashboard(request):
    return render(request,'dashboard/dashboard.html')
def modeling(request):
    return render(request,'dashbiard/modeling.html')
