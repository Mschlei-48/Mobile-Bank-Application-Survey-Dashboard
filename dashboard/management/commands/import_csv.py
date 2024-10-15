# dashboard/management/commands/import_csv.py
import pandas as pd
from django.core.management.base import BaseCommand
from dashboard.models import MobileBanking

class Command(BaseCommand):
    help = "Import data from Excel file into SQLite database"

    def handle(self, *args, **kwargs):
        # Load the Excel file using pandas
        df = pd.read_excel('C:/Users/Student/Desktop/Mobile-Banking-Django-App/Mobile-Baking-Data-Cleaned.xlsx')

        # Iterate over the rows and create Banking objects
        for _, row in df.iterrows():
            print(row)
            MobileBanking.objects.create(
                Age=row['Age'],
                Gender=row['Gender'],
                Occupation=row['Occupation'],
                UseMobileBankingApps=row['UseMobileBankingApps'],
                HowLongBeenUsingMobileBankingApplications=row['HowLongBeenUsingMobileBankingApplications'],
                UsingBankingAppsMakesFinancialManagementMoreEfficient=row['UsingBankingAppsMakesFinancialManagementMoreEfficient'],
                BankingAppsProvideFinancialAdviceThatIFindUseful=row['BankingAppsProvideFinancialAdviceThatIFindUseful'],
                ItIsImportantThatAIBankingAppsAreAvailableInMyNativeLanguage=row['ItIsImportantThatAIBankingAppsAreAvailableInMyNativeLanguage'],
                IWouldBeMoreLikelyToUseAIEnabledMobileBankingIfItInteractedInACulturallyAppropriateManner=row['IWouldBeMoreLikelyToUseAIEnabledMobileBankingIfItInteractedInACulturallyAppropriateManner'],
                AIFeaturesSuchAsChatbotsAndAutomatedAlertsInMobileBankingAreEasyToUse=row['AIFeaturesSuchAsChatbotsAndAutomatedAlertsInMobileBankingAreEasyToUse'],
                SeamlessIntegrationOfAIIntoMobileBankingAppsMakesMeMoreLikelyToUseThem=row['SeamlessIntegrationOfAIIntoMobileBankingAppsMakesMeMoreLikelyToUseThem'],
                MyCulturalBackgroundInfluencesMyTrustAndUseOfAIEnabledMobileBanking=row['MyCulturalBackgroundInfluencesMyTrustAndUseOfAIEnabledMobileBanking'],
                IPreferAIFeaturesThatAreSensitiveToMyCulture=row['IPreferAIFeaturesThatAreSensitiveToMyCulture'],
                ITrustTheSecurityMeasuresInAIEnabledMobileBankingApps=row['ITrustTheSecurityMeasuresInAIEnabledMobileBankingApps'],
                PersonalizedServiceInAIEnabledMobileBankingIncreaseMySatisfaction=row['PersonalizedServiceInAIEnabledMobileBankingIncreaseMySatisfaction'],
                AIEnabledMobileBankingAppearsIntelligentEnoughToHandleComplexTransactions=row['AIEnabledMobileBankingAppearsIntelligentEnoughToHandleComplexTransactions'],
                IFeelComfortableInteractingWithAIAsThoughItWereAHumanBankingAssistant=row['IFeelComfortableInteractingWithAIAsThoughItWereAHumanBankingAssistant'],
                PleaseProvideAnyAdditionalCommentsOrSuggestionsRegardingAIEnabledMobileBanking=row['PleaseProvideAnyAdditionalCommentsOrSuggestionsRegardingAIEnabledMobileBanking'],
            )

        self.stdout.write(self.style.SUCCESS("Data imported successfully!"))
