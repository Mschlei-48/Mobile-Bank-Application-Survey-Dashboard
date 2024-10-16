from django.shortcuts import render
from dashboard.models import MobileBanking
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter


# Create your views here.
def home(request):
    # Get all the data
    data=MobileBanking.objects.all()
    total_responses=data.count()
    mobile_banking_users=data.filter(UseMobileBankingApps='Yes').count()
    female_respondents=(data.filter(Gender='Female').count())
    male_respondents=(data.filter(Gender='Male')).count()
    if total_responses>0:
        adoption_rate=(mobile_banking_users/total_responses)*100
    else:
        adoption_rate=0
    
    # Get the ages, gender and occupations from the data
    ages=[entry.Age for entry in data]
    genders=[entry.Gender for entry in data]
    occupations=[entry.Occupation for entry in data]
    # Make plot for ages
    fig_age=px.violin(y=ages,title="Age Distribution",box=True,points=False,labels={'y':'Age'},width=450)
    plot_age_html=fig_age.to_html(full_html=False)

    # Plot for occupations
    occupation_counts = {occupation: occupations.count(occupation) for occupation in set(occupations)}

    # Create a doughnut chart by adding the 'hole' parameter
    fig_occupation = px.pie(
        values=list(occupation_counts.values()), 
        names=list(occupation_counts.keys()), 
        title="Occupation Distribution", 
        width=450, 
        hole=0.5  # This creates a doughnut chart by specifying the size of the hole (0.5 is typical for a doughnut chart)
    )

    # Convert the figure to HTML for rendering in the template
    plot_occupation_html = fig_occupation.to_html(full_html=False)

    # Gender plot
    gender_counts = {gender: genders.count(gender) for gender in set(genders)}

    # Sort the gender_counts dictionary by count in descending order
    sorted_gender_counts = dict(sorted(gender_counts.items(), key=lambda item: item[1], reverse=True))

    # Create the bar plot using the sorted data
    fig_gender = px.bar(
        x=list(sorted_gender_counts.keys()), 
        y=list(sorted_gender_counts.values()), 
        title="Gender Distribution", 
        labels={'x': 'Gender', 'y': 'Count'},
        color_discrete_sequence=['#4169E1', 'pink']
    )

    # Convert the figure to HTML for rendering in the template
    plot_gender_html = fig_gender.to_html(full_html=False)


    # Usage By Age Plot
    # Mobile Banking Usage by Age (Line Plot)
    age_usage_counts = list(data.filter(UseMobileBankingApps='Yes').values_list('Age', flat=True))
    age_all_counts = list(data.values_list('Age', flat=True))

    # Create a dictionary to count the number of users who said "Yes" to mobile banking for each age
    age_usage_distribution = {age: age_usage_counts.count(age) for age in set(age_all_counts)}

    # Now create the line plot using Plotly Express
    fig_usage_age = px.line(
        x=list(age_usage_distribution.keys()), 
        y=list(age_usage_distribution.values()), 
        title="Mobile Banking Usage by Age", 
        labels={'x': 'Age', 'y': 'Usage Count'},
        markers=True,
        width=450
    )

    # Convert plot to HTML for rendering in your Django template
    plot_usage_age_html = fig_usage_age.to_html(full_html=False)


    # Duration of mobile banking usage plot
    # Duration of Mobile Banking Use (Bar Plot)
    duration_counts = list(data.values_list('HowLongBeenUsingMobileBankingApplications', flat=True))

    # Create a dictionary to count the occurrences of each duration
    duration_distribution = {duration: duration_counts.count(duration) for duration in set(duration_counts)}

    # Sort the distribution by values (counts) in descending order
    sorted_duration_distribution = dict(sorted(duration_distribution.items(), key=lambda item: item[1], reverse=True))

    # Now create the bar plot using Plotly Express
    fig_duration = px.bar(
        x=list(sorted_duration_distribution.keys()), 
        y=list(sorted_duration_distribution.values()), 
        title="Duration of Mobile Banking Use", 
        width=450,
        labels={'x': 'Duration', 'y': 'Count'}
    )

    # Convert plot to HTML for rendering in your Django template
    plot_duration_html = fig_duration.to_html(full_html=False)


    # Banking Usage by Occupation Plot
    occupations = list(data.values_list('Occupation', flat=True))
    usage_yes = list(data.filter(UseMobileBankingApps='Yes').values_list('Occupation', flat=True))
    usage_no = list(data.filter(UseMobileBankingApps='No').values_list('Occupation', flat=True))

    # Calculate counts for both 'Yes' and 'No' mobile banking users
    occupation_distribution_yes = {occupation: usage_yes.count(occupation) for occupation in set(occupations)}
    occupation_distribution_no = {occupation: usage_no.count(occupation) for occupation in set(occupations)}

    # Calculate the total count for each occupation (for sorting)
    total_counts = {occupation: (occupation_distribution_yes.get(occupation, 0) + occupation_distribution_no.get(occupation, 0)) 
                    for occupation in set(occupations)}

    # Sort occupations by total count in descending order
    sorted_occupations = sorted(total_counts.keys(), key=lambda occ: total_counts[occ], reverse=True)

    # Prepare sorted values for plotting
    sorted_yes_counts = [occupation_distribution_yes.get(occ, 0) for occ in sorted_occupations]
    sorted_no_counts = [occupation_distribution_no.get(occ, 0) for occ in sorted_occupations]

    # Create the figure and add traces for stacked bar plot
    fig_occupation_usage = go.Figure()

    fig_occupation_usage.add_trace(go.Bar(
        x=sorted_occupations,
        y=sorted_yes_counts,
        name="Uses Mobile Banking",
        marker_color='#4169E1'
    ))

    fig_occupation_usage.add_trace(go.Bar(
        x=sorted_occupations,
        y=sorted_no_counts,
        name="Doesn't Use Mobile Banking",
        marker_color='red'
    ))

    # Update layout for the stacked bar plot
    fig_occupation_usage.update_layout(
        barmode='stack',
        title="Mobile Banking Usage by Occupation",
        xaxis_title="Occupation",
        yaxis_title="Count"
    )

    # Convert plot to HTML for rendering
    plot_occupation_usage_html = fig_occupation_usage.to_html(full_html=False)


    # Efficiency of AI Plots
    # Sample data (replace with your actual data)
    age_groups = ['18-25', '26-35', '36-45', '46-55', '55+']

    # Create a function to filter data by age
    def filter_data_by_age(data, age_group):
        if age_group == '18-25':
            return data.filter(Age__gte=18, Age__lte=25).values_list('UsingBankingAppsMakesFinancialManagementMoreEfficient', flat=True)
        elif age_group == '26-35':
            return data.filter(Age__gte=26, Age__lte=35).values_list('UsingBankingAppsMakesFinancialManagementMoreEfficient', flat=True)
        elif age_group == '36-45':
            return data.filter(Age__gte=36, Age__lte=45).values_list('UsingBankingAppsMakesFinancialManagementMoreEfficient', flat=True)
        elif age_group == '46-55':
            return data.filter(Age__gte=46, Age__lte=55).values_list('UsingBankingAppsMakesFinancialManagementMoreEfficient', flat=True)
        elif age_group == '55+':
            return data.filter(Age__gte=56).values_list('UsingBankingAppsMakesFinancialManagementMoreEfficient', flat=True)

    # Initialize figure
    fig_fm_efficiency = go.Figure()

    # Add traces for each age group
    for age_group in age_groups:
        financial_management_responses = filter_data_by_age(data, age_group)
        
        # Convert queryset to list for counting
        financial_management_responses_list = list(financial_management_responses)
        
        # Count responses
        fm_counts = {response: financial_management_responses_list.count(response) for response in set(financial_management_responses_list)}

        # Sort counts in descending order
        sorted_fm_counts = dict(sorted(fm_counts.items(), key=lambda item: item[1], reverse=True))

        # Add a bar trace for this age group
        fig_fm_efficiency.add_trace(go.Bar(
            x=list(sorted_fm_counts.keys()),
            y=list(sorted_fm_counts.values()),
            name=age_group,
            visible=(age_group == '18-25'),
            marker_color='#4169E1'  # Show only the first age group initially
        ))

    # Add dropdown buttons for age groups
    fig_fm_efficiency.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        args=[{'visible': [age_group == '18-25' for age_group in age_groups]}],
                        label="18-25",
                        method="update"
                    ),
                    dict(
                        args=[{'visible': [age_group == '26-35' for age_group in age_groups]}],
                        label="26-35",
                        method="update"
                    ),
                    dict(
                        args=[{'visible': [age_group == '36-45' for age_group in age_groups]}],
                        label="36-45",
                        method="update"
                    ),
                    dict(
                        args=[{'visible': [age_group == '46-55' for age_group in age_groups]}],
                        label="46-55",
                        method="update"
                    ),
                    dict(
                        args=[{'visible': [age_group == '55+' for age_group in age_groups]}],
                        label="55+",
                        method="update"
                    ),
                ],
                direction="down",
                showactive=True,
            ),
        ],
        title="Perception of AI in Financial Management Efficiency",
        xaxis_title="Response",
        yaxis_title="Count",
        width=930
    )

    # Convert to HTML for rendering in Django
    plot_fm_efficiency_html = fig_fm_efficiency.to_html(full_html=False)


    # Perception of AI in Providing Financial Advice (Bar Plot)
    age_groups = ['18-24', '25-34', '35-44', '45+']

    # Create a function to filter data by age
    def filter_data_by_age(data, age_group):
        if age_group == '18-24':
            return data.filter(Age__gte=18, Age__lte=24).values_list('BankingAppsProvideFinancialAdviceThatIFindUseful', flat=True)
        elif age_group == '25-34':
            return data.filter(Age__gte=25, Age__lte=34).values_list('BankingAppsProvideFinancialAdviceThatIFindUseful', flat=True)
        elif age_group == '35-44':
            return data.filter(Age__gte=35, Age__lte=44).values_list('BankingAppsProvideFinancialAdviceThatIFindUseful', flat=True)
        elif age_group == '45+':
            return data.filter(Age__gte=45).values_list('BankingAppsProvideFinancialAdviceThatIFindUseful', flat=True)

    # Initialize figure
    fig_fa_advice = go.Figure()

    # Add traces for each age group
    for age_group in age_groups:
        financial_advice_responses = filter_data_by_age(data, age_group)

        # Convert queryset to list for counting
        financial_advice_responses_list = list(financial_advice_responses)

        # Count responses
        fa_counts = {response: financial_advice_responses_list.count(response) for response in set(financial_advice_responses_list)}

        # Sort counts in descending order
        sorted_fa_counts = dict(sorted(fa_counts.items(), key=lambda item: item[1], reverse=True))

        # Add a bar trace for this age group
        fig_fa_advice.add_trace(go.Bar(
            x=list(sorted_fa_counts.keys()),
            y=list(sorted_fa_counts.values()),
            name=age_group,
            visible=(age_group == '18-24'),  # Show only the first age group initially,
            marker_color='#4169E1'
        ))

    # Add dropdown buttons for age groups
    fig_fa_advice.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        args=[{'visible': [age_group == '18-24' for age_group in age_groups]}],
                        label="18-24",
                        method="update"
                    ),
                    dict(
                        args=[{'visible': [age_group == '25-34' for age_group in age_groups]}],
                        label="25-34",
                        method="update"
                    ),
                    dict(
                        args=[{'visible': [age_group == '35-44' for age_group in age_groups]}],
                        label="35-44",
                        method="update"
                    ),
                    dict(
                        args=[{'visible': [age_group == '45+' for age_group in age_groups]}],
                        label="45+",
                        method="update"
                    ),
                ],
                direction="down",
                showactive=True,
            ),
        ],
        title="Perception of AI in Providing Financial Advice",
        xaxis_title="Response",
        yaxis_title="Count",
        width=930
    )

    # Convert to HTML for rendering in Django
    plot_fa_advice_html = fig_fa_advice.to_html(full_html=False)



    # Importance of AI in Native Language (Bar Plot)
    native_language_responses = data.values_list('ItIsImportantThatAIBankingAppsAreAvailableInMyNativeLanguage', flat=True)

    # Count occurrences of each unique response
    nl_counts = Counter(native_language_responses)

    # Create the bar plot
    fig_nl_importance = px.bar(
        x=list(nl_counts.keys()), 
        y=list(nl_counts.values()), 
        title="Importance of AI in Native Language", 
        labels={'x': 'Response', 'y': 'Count'},
        color_discrete_sequence=['#4169E1'],
        width=450
    )

    # Convert the figure to HTML
    plot_nl_importance_html = fig_nl_importance.to_html(full_html=False)



    # Cultural Appropriateness and Mobile Banking (Bar Plot)
    cultural_appropriateness_responses = data.values_list(
        'IWouldBeMoreLikelyToUseAIEnabledMobileBankingIfItInteractedInACulturallyAppropriateManner', 
        flat=True
    )
# Use Counter to count occurrences of each response
    ca_counts = Counter(cultural_appropriateness_responses)

    # Prepare data for plotting
    x_responses = list(ca_counts.keys())
    y_counts = list(ca_counts.values())

    # Create the bar plot
    fig_ca_mobile_banking = px.bar(
        x=x_responses, 
        y=y_counts, 
        title="Cultural Appropriateness and Mobile Banking", 
        labels={'x': 'Response', 'y': 'Count'},
        color_discrete_sequence=['#4169E1'],
        width=450
    )

    # Convert to HTML for embedding
    plot_ca_mobile_banking_html = fig_ca_mobile_banking.to_html(full_html=False)




    context={'adoption_rate':adoption_rate,'total_responses':total_responses,
    'female_respondents':female_respondents,'male_respondents':male_respondents,
    'plot_age_html':plot_age_html,'plot_occupation_html':plot_occupation_html,
    'plot_gender_html':plot_gender_html,'plot_usage_age_html':plot_usage_age_html,
    'plot_duration_html':plot_duration_html,'plot_occupation_usage_html':plot_occupation_usage_html,
    'plot_fm_efficiency_html':plot_fm_efficiency_html,'plot_fa_advice_html':plot_fa_advice_html,
    'plot_nl_importance_html':plot_nl_importance_html,'plot_ca_mobile_banking_html':plot_ca_mobile_banking_html}
    return render(request,'dashboard/home.html',context)

def dashboard(request):
    return render(request,'dashboard/dashboard.html')
def modeling(request):
    return render(request,'dashbiard/modeling.html')
