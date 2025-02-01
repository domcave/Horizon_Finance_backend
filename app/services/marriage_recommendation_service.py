class MarriageRecommendation:
    def get_recommend(self, spouse_income, annual_income, number_of_kids, save_for_college, years_until_college=18, annual_return_rate=0.08):
        total_income = spouse_income + annual_income

        wedding_budget = total_income * 0.10

        monthly_college_savings = 0
        if save_for_college:
            college_savings_per_child = 200000
            future_value = number_of_kids * college_savings_per_child

            monthly_return_rate = annual_return_rate / 12
            months = years_until_college * 12
            monthly_college_savings = future_value * monthly_return_rate / ((1 + monthly_return_rate) ** months - 1)

        return {
            "wedding_budget": wedding_budget,
            "monthly_college_savings": monthly_college_savings
        }
