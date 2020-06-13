#!/usr/bin/python3
# -*- coding: utf-8 -*-

def spending():
    try:
        logging.info("Getting MTD Spending")
        # Retreive current spend for this month
        client = boto3.client('ce', region_name='us-east-1')
        today = datetime.now()
        tomorrow = (datetime.today() + timedelta(days=1))
        firstdayofmonth = datetime.today().replace(day=1).strftime('%Y-%m-%d')
        lastdayofmonth = today.replace(day = calendar.monthrange(today.year, today.month)[1]).strftime('%Y-%m-%d')
        lastdayofnextmonth = tomorrow.replace(day = calendar.monthrange(tomorrow.year, tomorrow.month)[1]).strftime('%Y-%m-%d')
        mtd_cost = client.get_cost_and_usage(
            TimePeriod={
                'Start': firstdayofmonth,
                'End': today.strftime('%Y-%m-%d')
            },
            Granularity='MONTHLY',
            Metrics=[
                'AmortizedCost',
            ]
            )

        for r in mtd_cost['ResultsByTime']:
            usd = r['Total']['AmortizedCost']['Amount']
            usd = round(float(usd), 2)
        logging.info("MTD Spend: %s", usd)
        
        forecast_cost = client.get_cost_forecast(
            TimePeriod={
                'Start': tomorrow.strftime('%Y-%m-%d'),
                'End': lastdayofmonth if today.strftime('%Y-%m-%d') > lastdayofmonth else lastdayofnextmonth
            },
            Metric='UNBLENDED_COST',
            Granularity='MONTHLY',
            PredictionIntervalLevel=99)

        f_usd = forecast_cost['Total']['Amount']
        f_usd = round(float(f_usd), 2)
        logging.info("Forecasted Spend: %s", f_usd)

        return [usd, f_usd]
    except Exception as e:
        logging.error("Failed to get spending with error: %s", e)
