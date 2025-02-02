class RetirementRecommendation:
    def calculate_retirement(self, age, savings, annual_income, target_amount, annual_return_rate=0.07, withdrawal_rate=0.04):
        required_retirement_savings = annual_income / withdrawal_rate

        years_until_retirement = 0
        future_value_savings = savings
        while future_value_savings < required_retirement_savings:
            future_value_savings = future_value_savings * (1 + annual_return_rate) + annual_income
            years_until_retirement += 1

        retirement_age = age + years_until_retirement

        months_until_retirement = years_until_retirement * 12
        monthly_return_rate = annual_return_rate / 12
        future_value_contributions = required_retirement_savings - future_value_savings
        if future_value_contributions > 0:
            monthly_investment = future_value_contributions / (((1 + monthly_return_rate) ** months_until_retirement - 1) / monthly_return_rate * (1 + monthly_return_rate))
        else:
            monthly_investment = 0

        return {
            "suggested_retirement_age": retirement_age,
            "years_until_retirement": years_until_retirement,
            "total_retirement_savings": future_value_savings,
            "required_retirement_savings": required_retirement_savings,
            "suggested_monthly_investment": monthly_investment,
            "target_amount": target_amount
        }