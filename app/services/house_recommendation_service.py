class HouseRecommendation:
    national_avg_30_yr_mortgage_rate = 0.0705
    national_avg_20_yr_mortgage_rate = 0.0686
    national_avg_15_yr_mortgage_rate = 0.0635
    national_avg_10_yr_mortgage_rate = 0.0628

    def get_recommendation(self, income, owned_house_price=0):
        max_mortgage = income * 4.5

        max_house_price = (max_mortgage * 0.8) + owned_house_price

        monthly_payment_30yr = (max_house_price * HouseRecommendation.national_avg_30_yr_mortgage_rate) / 12

        total_cost_30yr = monthly_payment_30yr * 12 * 30

        monthly_payment_20yr = (max_house_price * HouseRecommendation.national_avg_20_yr_mortgage_rate) / 12

        total_cost_20yr = monthly_payment_20yr * 12 * 20

        monthly_payment_15yr = (max_house_price * HouseRecommendation.national_avg_15_yr_mortgage_rate) / 12

        total_cost_15yr = monthly_payment_15yr * 12 * 15

        monthly_payment_10yr = (max_house_price * HouseRecommendation.national_avg_10_yr_mortgage_rate) / 12

        total_cost_10yr = monthly_payment_10yr * 12 * 10

        return {
            "max_house_price": max_house_price,
            "mortgages": {
                "30_year": {
                    "monthly_payment": monthly_payment_30yr,
                    "total_cost": total_cost_30yr,
                    "total_interest": total_cost_30yr - max_house_price,
                    "mortgage_rate": HouseRecommendation.national_avg_30_yr_mortgage_rate
                    },
                "20_year": {
                    "monthly_payment": monthly_payment_20yr,
                    "total_cost": total_cost_20yr,
                    "total_interest": total_cost_20yr - max_house_price,
                    "mortgage_rate": HouseRecommendation.national_avg_20_yr_mortgage_rate
                },
                "15_year": {
                    "monthly_payment": monthly_payment_15yr,
                    "total_cost": total_cost_15yr,
                    "total_interest": total_cost_15yr - max_house_price,
                    "mortgage_rate": HouseRecommendation.national_avg_15_yr_mortgage_rate
                },
                "10_year": {
                    "monthly_payment": monthly_payment_10yr,
                    "total_cost": total_cost_10yr,
                    "total_interest": total_cost_10yr - max_house_price,
                    "mortgage_rate": HouseRecommendation.national_avg_10_yr_mortgage_rate
                },
            }
        }