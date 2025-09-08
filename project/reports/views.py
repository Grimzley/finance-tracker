from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta

from reports.utils import get_monthly_summary

@login_required
def report_list_view(request):
    today = date.today()
    join_date = request.user.date_joined.date()
    month_data = []
    num_months = (today.year - join_date.year) * 12 + (today.month - join_date.month)
    if today.day < join_date.day:
        num_months -= 1
    for i in range(max(5, num_months)):
        first_day = (today.replace(day=1) - timedelta(days=30*i)).replace(day=1)
        summary = get_monthly_summary(request.user, first_day)
        month_data.append(summary)
    context = {
        'past': month_data
    }
    return render(request, 'report_list.html', context)
