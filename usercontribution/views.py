from django.shortcuts import render
from .models import Source, UserContribution
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json, datetime

def search_contribution(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText', '')
        contribution = UserContribution.objects.filter(amount__starts_with = search_str, owner = request.user) | UserContribution.objects.filter(
                    date__istarts_with = search_str, owner = request.user) | UserContribution.objects.filter(
                    description__icontains = search_str, owner = request.user) | UserContribution.objects.filter(
                    category__icontains = search_str, owner = request.user)
        data = contribution.values()
        return JsonResponse(list(data), safe = False)

@login_required(login_url='authentication/login')
def index(request):
    source = Source.objects.all()
    contribution = UserContribution.objects.filter(owner=request.user)
    paginator = Paginator(contribution, 4)
    page_no = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_no)
    context = {
        'contribution': contribution,
        'page_obj': page_obj,
    }
    
    return render(request, 'contribution/index.html', context)

# def add_expense(request):
#     categories = Category.objects.all()
#     context = {
#             'categories': categories,
#             'values': request.POST
#         }
#     if request.method == "GET":
#         return render(request, 'expenses/add_expense.html', context)

#     if request.method == "POST":
#         amount = request.POST['amount']
        
#         if not amount:
#             messages.error(request, 'Amount is required')
#             return render(request, 'expenses/add_expense.html', context)
    
#         description = request.POST['description']
#         date = request.POST['expense_date']
#         category = request.POST['category']
        
#         if not description:
#             messages.error(request, 'Description is required')
#             return render(request, 'expenses/add_expense.html', context)
        
#         if not date:
#             messages.error(request, 'Date is required')
#             return render(request, 'expenses/add_expense.html', context)
        
#         Expense.objects.create(owner=request.user, amount=amount, date=date, category=category, description=description)
#         messages.success(request, 'UserContribution submitted successfully')
        
#         return redirect('contribution')

# def contribution_source_summary(request):
#     todays_date = datetime.date.today()
#     six_months_ago = todays_date - datetime.timedelta(days=30*6)
#     contributions = UserContribution.objects.filter(owner=request.user,
#                                 date__gte=six_months_ago, date__lte=todays_date)
#     finalrep = {}
    
#     def get_source(contribution):
#         return contribution.source
    
#     source_list = list(set(map(get_source, contributions)))
    
#     def get_contribution_source_amount(source):
#         amount = 0
#         filtered_by_source = contributions.filter(source=source)
        
#         for item in filtered_by_source:
#             amount += item.amount
        
#         return amount
    
#     for x in contributions:
#         for y in source_list:
#             finalrep[y] = get_contribution_source_amount(y)
    
#     return JsonResponse({'contribution_source_data': finalrep}, safe=False)

# def stats_view(request):
#      return render(request, 'contribution/cstats.html')

# creating an endpoint
def contribution_source_summary(request):
    try:    
        todays_date = datetime.date.today()
        six_months_ago = todays_date - datetime.timedelta(days=30*6)
        #query users contributions
        contributions = UserContribution.objects.filter(owner=request.user,
                                                        date__gte=six_months_ago, date__lte=todays_date)    
        #construct a final representation of the data
        final_rep = {}
        
        #get all source of user's contribution from the database
        #take a contribution and return a source of that contribution
        def get_source(contribution):
            return contribution.source
        #contributions list base upon source
        contribution_list = list(set(map(get_source, contributions)))
        
        def get_contribution_amount(source):
            amount = 0
            filtered_by_source = contributions.filter(source=source)
            
            for item in filtered_by_source:
                amount += item.amount
                    
            return amount
        
        for x in contributions:
            for y in contribution_list:
                final_rep[y] = get_contribution_amount(y)
        
        
        return JsonResponse({'contribution_source_data': final_rep}, safe=False)
    except Exception as e:
        # Log the error or handle it appropriately
        print("Error in contribution_source_summary:", str(e))
        return JsonResponse({'error': 'An error occurred'}, status=500)

def cstats_view(request):
    return render(request, 'contribution/cstats.html') 