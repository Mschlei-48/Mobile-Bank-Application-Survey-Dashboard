from django.shortcuts import render
from dashboard.models import MobileBanking
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import pandas as pd
from textblob import TextBlob
from sklearn.feature_extraction.text import CountVectorizer


# Create your views here.
def home(request):
    # Get all the data
    data=MobileBanking.objects.all()
    # Change the object data to a dataframe
    # df = pd.DataFrame(list(data))

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

    # Gender plot Distribution
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

    # Add count labels above the bars
    for index, value in enumerate(sorted_gender_counts.values()):
        fig_gender.add_annotation(
            x=list(sorted_gender_counts.keys())[index],
            y=value,
            text=str(value),
            showarrow=False,
            font=dict(size=12),
            yshift=5  # Adjusts the position of the text label
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

    # Create the bar plot using Plotly Express
    fig_duration = px.bar(
        x=list(sorted_duration_distribution.keys()), 
        y=list(sorted_duration_distribution.values()), 
        title="Duration of Mobile Banking Use", 
        width=450,
        labels={'x': 'Duration', 'y': 'Count'}
    )

    # Add count labels above the bars
    for index, value in enumerate(sorted_duration_distribution.values()):
        fig_duration.add_annotation(
            x=list(sorted_duration_distribution.keys())[index],
            y=value,
            text=str(value),
            showarrow=False,
            font=dict(size=12),
            yshift=5  # Adjusts the position of the text label
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
        yaxis_title="Count",
        xaxis_tickangle=-45  # Rotate x-axis labels for better visibility
    )

    # Add count labels on top of the bars for 'Uses Mobile Banking'
    for index, value in enumerate(sorted_yes_counts):
        if value > 0:  # Check if there is a bar
            y_position = value + 5  # Positioning above the bar with a fixed offset
            fig_occupation_usage.add_annotation(
                x=sorted_occupations[index],
                y=y_position,
                text=str(value),
                showarrow=False,
                font=dict(size=10),
                yshift=5  # Adjust this value as needed
            )

    # Add count labels on top of the bars for 'Doesn't Use Mobile Banking'
    for index, value in enumerate(sorted_no_counts):
        if value > 0:  # Check if there is a bar
            y_position = sorted_yes_counts[index] + value + 5  # Position above the stacked bar
            fig_occupation_usage.add_annotation(
                x=sorted_occupations[index],
                y=y_position,
                text=str(value),
                showarrow=False,
                font=dict(size=10),
                yshift=5  # Adjust this value as needed
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

    # Create a list to hold annotations for each age group
    all_annotations = {}

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
            visible=(age_group == '18-25'),  # Show only the first age group initially
            marker_color='#4169E1'  # Color for the bars
        ))

        # Create annotations for this age group
        annotations = []
        for index, value in enumerate(sorted_fm_counts.values()):
            if value > 0:  # Only add annotations for bars with counts
                annotations.append(
                    dict(
                        x=list(sorted_fm_counts.keys())[index],
                        y=value + 0.5,  # Adjust the position above the bar
                        text=str(value),
                        showarrow=False,
                        font=dict(size=10),
                        yshift=5
                    )
                )
        
        # Store annotations for the current age group
        all_annotations[age_group] = annotations

    # Set the initial annotations for the first age group
    fig_fm_efficiency.update_layout(
        annotations=all_annotations['18-25']  # Set initial annotations for the first visible group
    )

    # Add dropdown buttons for age groups
    fig_fm_efficiency.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        args=[{'visible': [age_group == '18-25' for age_group in age_groups]},
                            {'annotations': all_annotations['18-25']}],
                        label="18-25",
                        method="update"
                    ),
                    dict(
                        args=[{'visible': [age_group == '26-35' for age_group in age_groups]},
                            {'annotations': all_annotations['26-35']}],
                        label="26-35",
                        method="update"
                    ),
                    dict(
                        args=[{'visible': [age_group == '36-45' for age_group in age_groups]},
                            {'annotations': all_annotations['36-45']}],
                        label="36-45",
                        method="update"
                    ),
                    dict(
                        args=[{'visible': [age_group == '46-55' for age_group in age_groups]},
                            {'annotations': all_annotations['46-55']}],
                        label="46-55",
                        method="update"
                    ),
                    dict(
                        args=[{'visible': [age_group == '55+' for age_group in age_groups]},
                            {'annotations': all_annotations['55+']}],
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

    # Create a list to hold annotations for each age group
    all_annotations = {}

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
            visible=(age_group == '18-24'),  # Show only the first age group initially
            marker_color='#4169E1'
        ))

        # Create annotations for this age group
        annotations = []
        for index, value in enumerate(sorted_fa_counts.values()):
            if value > 0:  # Only add annotations for bars with counts
                annotations.append(
                    dict(
                        x=list(sorted_fa_counts.keys())[index],
                        y=value + 0.5,  # Adjust the position above the bar
                        text=str(value),
                        showarrow=False,
                        font=dict(size=10),
                        yshift=5
                    )
                )
        
        # Store annotations for the current age group
        all_annotations[age_group] = annotations

    # Set the initial annotations for the first age group
    fig_fa_advice.update_layout(
        annotations=all_annotations['18-24']  # Set initial annotations for the first visible group
    )

    # Add dropdown buttons for age groups
    fig_fa_advice.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        args=[{'visible': [age_group == '18-24' for age_group in age_groups]},
                            {'annotations': all_annotations['18-24']}],
                        label="18-24",
                        method="update"
                    ),
                    dict(
                        args=[{'visible': [age_group == '25-34' for age_group in age_groups]},
                            {'annotations': all_annotations['25-34']}],
                        label="25-34",
                        method="update"
                    ),
                    dict(
                        args=[{'visible': [age_group == '35-44' for age_group in age_groups]},
                            {'annotations': all_annotations['35-44']}],
                        label="35-44",
                        method="update"
                    ),
                    dict(
                        args=[{'visible': [age_group == '45+' for age_group in age_groups]},
                            {'annotations': all_annotations['45+']}],
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



    # Importance of AI in Native Language and Cultural Appropriateness (Bar Plot)
    native_language_responses = data.values_list('ItIsImportantThatAIBankingAppsAreAvailableInMyNativeLanguage', flat=True)
    nl_counts = Counter(native_language_responses)

    cultural_appropriateness_responses = data.values_list(
        'IWouldBeMoreLikelyToUseAIEnabledMobileBankingIfItInteractedInACulturallyAppropriateManner', flat=True
    )
    ca_counts = Counter(cultural_appropriateness_responses)

    response_categories = list(set(native_language_responses) | set(cultural_appropriateness_responses))

    nl_values = [nl_counts.get(category, 0) for category in response_categories]
    ca_values = [ca_counts.get(category, 0) for category in response_categories]

    fig_stacked_bar = go.Figure()

    fig_stacked_bar.add_trace(go.Bar(
        x=response_categories,
        y=nl_values,
        name="Importance of Native Language",
        marker_color='#4169E1'
    ))


    fig_stacked_bar.add_trace(go.Bar(
        x=response_categories,
        y=ca_values,
        name="Cultural Appropriateness",
        marker_color='#FF4500'
    ))

    fig_stacked_bar.update_layout(
        barmode='stack',
        title="Perception of AI in Native Language and Cultural Appropriateness",
        xaxis_title="Response",
        yaxis_title="Count",
        width=930
    )
    plot_stacked_bar_html = fig_stacked_bar.to_html(full_html=False)



    # Heatmap
    df = pd.DataFrame(list(data.values()))
    fig_facet = px.box(
        df,
        x='Age',
        y='PersonalizedServiceInAIEnabledMobileBankingIncreaseMySatisfaction',
        color='Gender',
        title="Satisfaction by Age and Gender",
        width=930,
        labels={
            'Age': 'Age of Respondents',  # Custom label for x-axis
            'PersonalizedServiceInAIEnabledMobileBankingIncreaseMySatisfaction': 'Satisfaction Level',  # Custom label for y-axis
            'Gender': 'Respondent Gender'  # Custom label for color grouping
        }
    )

    # Convert the figure to HTML for rendering in the template
    plot_facet_html = fig_facet.to_html(full_html=False)


    # Bubble Plot
    fig_violin = px.violin(
        df,
        x='Gender',
        y='IFeelComfortableInteractingWithAIAsThoughItWereAHumanBankingAssistant',
        box=True,
        title="Comfort with AI by Gender",
        width=930,
        labels={
            'Gender':'Gender',
            'IFeelComfortableInteractingWithAIAsThoughItWereAHumanBankingAssistant':'Comfortable Interacting With AI'
        }
    )

    plot_violin_html = fig_violin.to_html(full_html=False)

    # BAR GRAPH 
    df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 18, 30, 45, 60, 100], labels=['<18', '18-30', '30-45', '45-60', '>60'])

    # Count occurrences of usability responses per AgeGroup and Gender
    df_grouped = df.groupby(['AgeGroup', 'Gender']).size().reset_index(name='Count')

    # Create the bar plot
    fig_bar = px.bar(
        df_grouped,
        x='AgeGroup',
        y='Count',
        color='Gender',
        title="AI Usability by Age Group and Gender",
        barmode='group',
        width=950,
        labels={'Count': 'Number of Users'}
    )

    # Convert the figure to HTML for rendering in the template
    new_plot_bar_html = fig_bar.to_html(full_html=False)


    # Sentiment Analysis plots
    def get_sentiment(text):
        analysis = TextBlob(text)
        if analysis.sentiment.polarity > 0:
            return 'Positive'
        elif analysis.sentiment.polarity == 0:
            return 'Neutral'
        else:
            return 'Negative'

    # Apply sentiment analysis to each comment
    df['Sentiment'] = df['PleaseProvideAnyAdditionalCommentsOrSuggestionsRegardingAIEnabledMobileBanking'].apply(get_sentiment)

    # Count the occurrences of each sentiment
    sentiment_counts = df['Sentiment'].value_counts()

    # Create a doughnut plot
    fig_sentiment_doughnut = px.pie(
        values=sentiment_counts.values,  # Y-axis values (the counts)
        names=sentiment_counts.index,    # X-axis values (the sentiment labels)
        title="Comments Sentiments",
        hole=0.4,  # This creates the doughnut effect
        width=450
    )

    # Convert the plot to HTML for embedding in Django template
    plot_sentiment_doughnut_html = fig_sentiment_doughnut.to_html(full_html=False)


    # Common words
    vectorizer = CountVectorizer(stop_words='english', max_features=10)
    comment_vectors = vectorizer.fit_transform(df['PleaseProvideAnyAdditionalCommentsOrSuggestionsRegardingAIEnabledMobileBanking'])
    keywords = vectorizer.get_feature_names_out()
    counts = comment_vectors.toarray().sum(axis=0)
    df_keywords = pd.DataFrame({'Keyword': keywords, 'Count': counts})
    df_keywords = df_keywords.sort_values(by='Count', ascending=False)
    fig_keywords = px.bar(
        df_keywords,
        x='Keyword',
        y='Count',
        title="Top Words in  Comments",
        text='Count',  # Show the count on top of each bar
        width=450
    )
    fig_keywords.update_layout(
        xaxis_title="Keywords",
        yaxis_title="Count",
    )

    plot_keywords_html = fig_keywords.to_html(full_html=False)


    # Text Length
    df['CommentLength'] = df['PleaseProvideAnyAdditionalCommentsOrSuggestionsRegardingAIEnabledMobileBanking'].apply(lambda x: len(x.split()))
    fig_histogram = px.histogram(df, x='CommentLength', title="Distribution of Comment Lengths", nbins=20,width=450)
    new_plot_histogram_html = fig_histogram.to_html(full_html=False)

    # Bigrams
    vectorizer = CountVectorizer(ngram_range=(2, 2), stop_words='english', max_features=10)
    bigram_vectors = vectorizer.fit_transform(df['PleaseProvideAnyAdditionalCommentsOrSuggestionsRegardingAIEnabledMobileBanking'])
    bigrams = vectorizer.get_feature_names_out()
    bigram_counts = bigram_vectors.toarray().sum(axis=0)

    # Create a DataFrame to hold bigrams and counts, and sort by count
    df_bigrams = pd.DataFrame({'Bigram': bigrams, 'Count': bigram_counts}).sort_values(by='Count', ascending=False)

# Create the bar plot
    fig_bigrams = px.bar(
        df_bigrams,
        x='Bigram',
        y='Count',
        title="Top Bigrams in Comments",
        text='Count',  # Show the count on top of the bars
        width=450,
        labels={'Bigram': "Bigrams", 'Count': 'Count'}  # Correctly label the axes
    )

    # Update the layout for axis labels and add numbers on top of bars
    fig_bigrams.update_layout(
        xaxis_title="Bigrams",
        yaxis_title="Count",
    )

    # Convert the plot to HTML for rendering in Django
    plot_bigrams_html = fig_bigrams.to_html(full_html=False)

    context={'adoption_rate':adoption_rate,'total_responses':total_responses,
    'female_respondents':female_respondents,'male_respondents':male_respondents,
    'plot_age_html':plot_age_html,'plot_occupation_html':plot_occupation_html,
    'plot_gender_html':plot_gender_html,'plot_usage_age_html':plot_usage_age_html,
    'plot_duration_html':plot_duration_html,'plot_occupation_usage_html':plot_occupation_usage_html,
    'plot_fm_efficiency_html':plot_fm_efficiency_html,'plot_fa_advice_html':plot_fa_advice_html,
    'plot_facet_html':plot_facet_html,'plot_violin_html':plot_violin_html,
    'new_plot_bar_html':new_plot_bar_html,'plot_sentiment_doughnut_html':plot_sentiment_doughnut_html,
    'plot_keywords_html':plot_keywords_html,'new_plot_histogram_html':new_plot_histogram_html,
    'plot_bigrams_html':plot_bigrams_html 
    }
    return render(request,'dashboard/home.html',context)

def dashboard(request):
    return render(request,'dashboard/dashboard.html')
def modeling(request):
    return render(request,'dashbiard/modeling.html')
