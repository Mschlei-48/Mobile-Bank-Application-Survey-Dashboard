from django.db import models

# Create your models here.

class MobileBanking(models.Model):
    Age=models.IntegerField()
    Gender=models.CharField(max_length=500)
    Occupation=models.CharField(max_length=500)
    UseMobileBankingApps=models.CharField(max_length=500)
    HowLongBeenUsingMobileBankingApplications=models.CharField(max_length=500)
    UsingBankingAppsMakesFinancialManagementMoreEfficient=models.CharField(max_length=500)
    BankingAppsProvideFinancialAdviceThatIFindUseful=models.CharField(max_length=500)
    ItIsImportantThatAIBankingAppsAreAvailableInMyNativeLanguage=models.CharField(max_length=500)
    IWouldBeMoreLikelyToUseAIEnabledMobileBankingIfItInteractedInACulturallyAppropriateManner=models.CharField(max_length=500)
    AIFeaturesSuchAsChatbotsAndAutomatedAlertsInMobileBankingAreEasyToUse=models.CharField(max_length=500)
    SeamlessIntegrationOfAIIntoMobileBankingAppsMakesMeMoreLikelyToUseThem=models.CharField(max_length=500)
    MyCulturalBackgroundInfluencesMyTrustAndUseOfAIEnabledMobileBanking=models.CharField(max_length=500)
    IPreferAIFeaturesThatAreSensitiveToMyCulture=models.CharField(max_length=500)
    ITrustTheSecurityMeasuresInAIEnabledMobileBankingApps=models.CharField(max_length=500)
    PersonalizedServiceInAIEnabledMobileBankingIncreaseMySatisfaction=models.CharField(max_length=500)
    AIEnabledMobileBankingAppearsIntelligentEnoughToHandleComplexTransactions=models.CharField(max_length=500)
    IFeelComfortableInteractingWithAIAsThoughItWereAHumanBankingAssistant=models.CharField(max_length=500)
    PleaseProvideAnyAdditionalCommentsOrSuggestionsRegardingAIEnabledMobileBanking=models.CharField(max_length=5000)

    def __str__(self):
        # return self.name
        # Creating names for the rows
        return f"{self.Gender} - {self.Occupation}"