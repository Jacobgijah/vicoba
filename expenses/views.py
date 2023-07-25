from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Category, Loan, Marital, Car, House
import json, datetime


def search_expenses(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText", "")
        expenses = (
            Loan.objects.filter(amount__starts_with=search_str, owner=request.user)
            | Loan.objects.filter(date__istarts_with=search_str, owner=request.user)
            | Loan.objects.filter(description__icontains=search_str, owner=request.user)
            | Loan.objects.filter(category__icontains=search_str, owner=request.user)
        )
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url="authentication/login")
def index(request):
    categories = Category.objects.all()
    expenses = Loan.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 4)
    page_no = request.GET.get("page")
    page_obj = Paginator.get_page(paginator, page_no)
    context = {
        "expenses": expenses,
        "page_obj": page_obj,
    }

    return render(request, "expenses/index.html", context)


def add_expense(request):
    categories = Category.objects.all()
    maritals = Marital.objects.all()
    cars = Car.objects.all()
    houses = House.objects.all()
    context = {
        "houses": houses,
        "cars": cars,
        "maritals": maritals,
        "categories": categories,
        "prof_choices": Loan.prof_choices,
        "values": request.POST,
    }
    if request.method == "GET":
        return render(request, "expenses/add_expense.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]
        for i in request.POST.lists():
            print(i)
        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "expenses/add_expense.html", context)

        description = request.POST["description"]
        date = request.POST["expense_date"]
        category = request.POST["category"]
        profession = request.POST.get("“profession”").replace("“", "").replace("”", "")
        marital = request.POST["marital"]
        house = request.POST["house"]
        car = request.POST["car"]
        age = request.POST["age"]
        income = request.POST["income"]
        experience = request.POST["experience"]

        print(profession)
        print(type(profession))
        print(len(profession))
        if not description:
            messages.error(request, "Description is required")
            return render(request, "expenses/add_expense.html", context)

        if not date:
            messages.error(request, "Date is required")
            return render(request, "expenses/add_expense.html", context)

        Loan.objects.create(
            owner=request.user,
            amount=amount,
            date=date,
            category=category,
            description=description,
            profession=profession,
            marital=marital,
            house=house,
            car=car,
            age=age,
            income=income,
            experience=experience,
        )
        messages.success(request, "Loan submitted successfully")

        return redirect("expenses")


def expense_edit(request, id):
    expense = Loan.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        "expense": expense,
        "values": expense,
        "categories": categories,
    }
    if request.method == "GET":
        return render(request, "expenses/edit-expense.html", context)

    if request.method == "POST":
        amount = request.POST["amount"]

        if not amount:
            messages.error(request, "Amount is required")
            return render(request, "expenses/edit-expense.html", context)

        description = request.POST["description"]
        date = request.POST["expense_date"]
        category = request.POST["category"]

        if not description:
            messages.error(request, "Description is required")
            return render(request, "expenses/edit-expense.html", context)

        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, "Loan updated successfully")

        return redirect("expenses")


def delete_expense(request, id):
    expense = Loan.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Loan Appication removed")
    return redirect("expenses")


# def search_expenses(request):
#     if request.method == "POST":
#         search_str = json.loads(request.body).get('searchText')
#         expenses = Expense.objects.filter(
#             amount__strat_with = search_str, owner = request.user) | Expense.objects.filter(
#             date__istrat_with = search_str, owner = request.user) | Expense.objects.filter(
#             description__icontains = search_str, owner = request.user) | Expense.objects.filter(
#             category__icontains = search_str, owner = request.user)
#         data = expenses.values()
#         return JsonResponse(list(data), safe=False)


def loan_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30 * 6)
    loans = Loan.objects.filter(
        owner=request.user, date__gte=six_months_ago, date__lte=todays_date
    )
    finalrep = {}

    def get_category(expense):
        return expense.category

    category_list = list(set(map(get_category, loans)))

    def get_loan_category_amount(category):
        amount = 0
        filtered_by_category = loans.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount

        return amount

    for x in loans:
        for y in category_list:
            finalrep[y] = get_loan_category_amount(y)

    return JsonResponse({"loan_category_data": finalrep}, safe=False)


def stats_view(request):
    return render(request, "expenses/stats.html")
