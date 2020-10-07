import datetime

from django.contrib import admin
from django.utils import timezone
from django.contrib.admin import SimpleListFilter
from django.contrib.admin import DateFieldListFilter
from django.db.models import Sum
from django.contrib.auth import get_user_model

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from rangefilter.filter import DateRangeFilter

from location.models import Branches
from finance.models  import Sales, Expense_Types, Expense_Methods, \
                            Banks, Expenses, Bank_Status
from adminApiModel.utils import FilterBranchStaffDropDown, \
                                FilterBranchStaffBankDropDown, \
                                BranchFilter, \
                                BankFilter, \
                                ExpenseTypeFilter, \
                                TotalsumAdmin, HistoryFilterBranchStaffBankDropDown


class SalesResource(resources.ModelResource):
    branch = fields.Field(
        column_name='branch',
        attribute='branch',
        widget=ForeignKeyWidget(Branches, 'location'))
    class Meta:
        model = Sales
        fields = (
            'date',
            'branch',
            'short_or_over',
            'gross_sales',
            'cash_on_caja',
            'cash_for_deposit',
        )
        export_order = ('date', 'branch')


@admin.register(Sales)
class CustomSaleAdmin(TotalsumAdmin, HistoryFilterBranchStaffBankDropDown):
    change_list_template = "admin/utils/change_list.html"
    totalsum_list = ('gross_sales','cash_on_caja', 'short_or_over', 'caja_minus_deposit', 'cash_for_deposit')
    resource_class = SalesResource
    list_per_page = 10
    ordering = ['-date', 'branch']
    list_display = ['date', 'branch', 'short_or_over', 'cash_on_caja', 'gross_sales', 'cash_for_deposit', 'caja_minus_deposit', 'remark', 'num_trxn', 'num_cstmr', 'OR_nums', 'num_rcpt', 'total_disc', 'petty_cash', 'bank', 'was_deposited', 'is_valid', 'file', 'retailer']
    list_filter = ['is_valid',
                    BranchFilter,
                   ('date', DateRangeFilter),
                   ('date', DateFieldListFilter),
    ]


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        user = request.user
        disabled_fields = set()  # type: Set[str]

        if not user.is_superuser:
            disabled_fields |= {
                'manager',
                'short_or_over',
            }

        if not user.roles.is_manager:
            disabled_fields |= {
                'retailer',
            }

            if not user.roles.sale_change_deposit:
                disabled_fields |= {
                    'was_deposited',
                }

            if not (user.roles.is_assistant and user.roles.sale_can_validate):
                disabled_fields |= {
                    'is_valid',
                }


        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


    def get_queryset(self, request):
        user = request.user
        if user.is_superuser:
            return super().get_queryset(request)
        elif user.roles.is_manager:
            return super().get_queryset(request
                   ).filter(manager=user)
        elif user.roles.is_assistant:
            days = user.roles.sale_days
            branches = user.roles.sale_branches.all()
            if days and branches:
                return super().get_queryset(request
                       ).filter(manager=user.roles.manager
                       ).filter(date__gte=timezone.now() - datetime.timedelta(days=days)
                       ).filter(branch__in=branches)
            else:
                raise RuntimeError("User is assistant but roles improperly configured")
        elif user.roles.is_retailer:
            days = user.roles.days
            if days:
                return super().get_queryset(request
                       ).filter(manager=user.roles.manager
                       ).filter(date__gte=timezone.now() - datetime.timedelta(days=days)
                       ).filter(branch__in=user.roles.branches.all())
            else:
                return super().get_queryset(request
                       ).filter(manager=user.roles.manager
                       ).filter(date__gte=timezone.now() - datetime.timedelta(days=1)
                       ).filter(branch__in=user.roles.branches.all())

        # elif user.roles.is_retailer:
        #     return super().get_queryset(request
        #            ).filter(manager=user.roles.manager
        #            ).filter(date__gte=timezone.now() - datetime.timedelta(days=1)
        #            ).filter(branch__in=user.roles.branches.all())


    def save_model(self, request, obj, form, change):
        if request.user.roles.is_manager:
            obj.manager = request.user
            obj.retailer = request.user
        elif request.user.roles.is_retailer or request.user.roles.is_assistant:
            obj.manager = request.user.roles.manager
            obj.retailer = request.user
        super().save_model(request, obj, form, change)


    def save_related(self, request, form, formsets, change):
        try:
            bank_status = form.instance.bank_status
        except Sales.bank_status.RelatedObjectDoesNotExist:
            bank_status = None

        if (not bank_status) and form.instance.was_deposited:
            if request.user.is_superuser:
                manager = request.user
            elif request.user.roles.is_manager:
                manager = request.user
            else:
                manager = request.user.roles.manager
            Bank_Status(manager=manager,
                        bank=form.instance.bank,
                        date=datetime.datetime.combine(form.instance.date, datetime.datetime.now().time()),
                        sale_report=form.instance,
                        deposit=form.instance.cash_for_deposit,
                ).save()
        elif bank_status:
            bank_status.deposit = form.instance.cash_for_deposit
            bank_status.bank = form.instance.bank
            bank_status.save()


# manager
# bank
# date
# sale_report
# expense_report
# deposit
# withdraw
# update
# remark
# check
# online
# image


class BaseExpensePurchaseSubAdmin(admin.ModelAdmin):


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        user = request.user
        disabled_fields = set()  # type: Set[str]

        if not user.is_superuser:
            disabled_fields |= {
                'manager',
            }


        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


    def save_model(self, request, obj, form, change):
        if request.user.roles.is_manager:
            obj.manager = request.user
        else:
            obj.manager = request.user.roles.manager
        super().save_model(request, obj, form, change)


    def get_queryset(self, request):
        user = request.user
        if user.is_superuser:
            return super().get_queryset(request)
        elif user.roles.is_manager:
            return super().get_queryset(request
                   ).filter(manager=user)
        elif user.roles.is_assistant:
            return super().get_queryset(request
                   ).filter(manager=user.roles.manager)


@admin.register(Expense_Types)
class CustomExpenseTypeAdmin(BaseExpensePurchaseSubAdmin):
    pass


@admin.register(Expense_Methods)
class CustomExpenseMethodAdmin(BaseExpensePurchaseSubAdmin):
    pass


@admin.register(Banks)
class CustomBankAdmin(BaseExpensePurchaseSubAdmin):
    pass


class ExpensesResource(resources.ModelResource):
    branch = fields.Field(
        column_name='branch',
        attribute='branch',
        widget=ForeignKeyWidget(Branches, 'location'))
    type_of_expense = fields.Field(
        column_name='Type of Expense',
        attribute='type_of_expense',
        widget=ForeignKeyWidget(Expense_Types, 'name'))
    method_of_payment = fields.Field(
        column_name='Method of Payment',
        attribute='method_of_payment',
        widget=ForeignKeyWidget(Expense_Methods, 'name'))
    bank = fields.Field(
        column_name='Bank',
        attribute='bank',
        widget=ForeignKeyWidget(Banks, 'name'))
    class Meta:
        model = Expenses
        fields = (
            'date',
            'branch',
            'amount',
            'type_of_expense',
            'method_of_payment',
            'bank',
        )
        export_order = ('date', 'branch')


@admin.register(Expenses)
class CustomExpenseAdmin(TotalsumAdmin):
    change_list_template = "admin/utils/change_list.html"
    totalsum_list = ('amount',)
    resource_class = ExpensesResource
    ordering = ['-date', 'branch']
    list_display = ['date', 'branch', 'is_paid', 'amount', 'type_of_expense', 'method_of_payment', 'bank', 'remark', 'is_valid', 'bill_stmt', 'prf_pay', 'attch_doc', 'doc_desc']
    list_filter = ['is_valid',
                   BranchFilter,
                   ExpenseTypeFilter,
                   ('date', DateRangeFilter),
                   ('date', DateFieldListFilter),
    ]


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        user = request.user
        disabled_fields = set()  # type: Set[str]

        if not user.is_superuser:
            disabled_fields |= {
                'manager',
            }

        if not user.roles.is_manager:
            disabled_fields |= {
                'retailer',
            }
            if not (user.roles.is_assistant and user.roles.expense_can_validate):
                disabled_fields |= {
                    'is_valid',
                }


        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


    def save_model(self, request, obj, form, change):
        if request.user.roles.is_manager:
            obj.manager = request.user
        else:
            obj.manager = request.user.roles.manager
            obj.retailer = request.user
        super().save_model(request, obj, form, change)


    def get_queryset(self, request):
        user = request.user
        if user.is_superuser:
            return super().get_queryset(request)
        elif user.roles.is_manager:
            return super().get_queryset(request
                   ).filter(manager=user)
        elif user.roles.is_assistant:
            days = user.roles.expense_days
            branches = user.roles.expense_branches.all()
            if days and branches:
                return super().get_queryset(request
                       ).filter(manager=user.roles.manager
                       ).filter(date__gte=timezone.now() - datetime.timedelta(days=days)
                       ).filter(branch__in=branches)
            else:
                raise RuntimeError("User is assistant but roles improperly configured")
        elif user.roles.is_retailer:
            days = user.roles.days
            if days:
                return super().get_queryset(request
                       ).filter(manager=user.roles.manager
                       ).filter(date__gte=timezone.now() - datetime.timedelta(days=days)
                       ).filter(branch__in=user.roles.branches.all())
            else:
                return super().get_queryset(request
                       ).filter(manager=user.roles.manager
                       ).filter(date__gte=timezone.now() - datetime.timedelta(days=1)
                       ).filter(branch__in=user.roles.branches.all())


    def save_related(self, request, form, formsets, change):
        try:
            bank_status = form.instance.bank_status
        except Expenses.bank_status.RelatedObjectDoesNotExist:
            bank_status = None

        if (not bank_status) and form.instance.is_valid and form.instance.bank:
            if request.user.is_superuser:
                manager = request.user
            elif request.user.roles.is_manager:
                manager = request.user
            else:
                manager = request.user.roles.manager
            Bank_Status(manager=manager,
                        bank=form.instance.bank,
                        date=datetime.datetime.combine(form.instance.date, datetime.datetime.now().time()),
                        expense_report=form.instance,
                        withdraw=form.instance.amount,
                ).save()
        elif bank_status:
            bank_status.withdraw = form.instance.amount
            bank_status.bank = form.instance.bank
            bank_status.save()


    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "staff" or db_field.name == "retailer":
            if request.user.is_superuser:
                kwargs["queryset"] = \
                    get_user_model().objects.all()
            elif request.user.roles.is_manager:
                kwargs["queryset"] = \
                    get_user_model().objects.filter(
                        roles__manager=request.user)
            else:
                kwargs["queryset"] = \
                    get_user_model().objects.filter(
                        roles__manager=request.user.roles.manager)


        elif db_field.name == "branch":
            if request.user.is_superuser:
                kwargs["queryset"] = \
                    Branches.objects.all()
            elif request.user.roles.is_manager:
                kwargs["queryset"] = request.user.branches.filter(is_open=True)
            else:
                kwargs["queryset"] = request.user.roles.branches.filter(is_open=True)


        elif db_field.name == "type_of_expense":
            if request.user.is_superuser:
                kwargs["queryset"] = \
                    Expense_Types.objects.all()
            elif request.user.roles.is_manager:
                kwargs["queryset"] = request.user.expense_types.filter(is_active=True)
            else:
                kwargs["queryset"] = request.user.roles.manager.expense_types.filter(is_active=True)


        elif db_field.name == "method_of_payment":
            if request.user.is_superuser:
                kwargs["queryset"] = \
                    Expense_Methods.objects.all()
            elif request.user.roles.is_manager:
                kwargs["queryset"] = request.user.expense_methods.filter(is_active=True)
            else:
                kwargs["queryset"] = request.user.roles.manager.expense_methods.filter(is_active=True)


        elif db_field.name == "bank":
            if request.user.is_superuser:
                kwargs["queryset"] = \
                    Banks.objects.all()
            elif request.user.roles.is_manager:
                kwargs["queryset"] = request.user.banks.filter(is_active=True)
            else:
                kwargs["queryset"] = request.user.roles.manager.banks.filter(is_active=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Bank_Status)
class CustomBankStatusAdmin(TotalsumAdmin):
    change_list_template = "admin/finance/change_list_bank_status.html"
    totalsum_list = ('deposit', 'withdraw')
    ordering = ['bank', '-date']
    # ordering = ['-date', 'bank']
    list_display = ['date', 'bank', 'total', 'update', 'error', 'deposit', 'withdraw', 'remark']
    list_filter = [BankFilter,
                   ('date', DateRangeFilter),
                   ('date', DateFieldListFilter),
    ]
    list_per_page = 10
    readonly_fields = ('deposit', 'withdraw', 'total', 'error')
    fields = ('deposit', 'withdraw', 'total', 'date', 'update', 'error', 'remark', 'check', 'online', 'image')


    def get_queryset(self, request):
        user = request.user
        if user.roles.is_manager:
            return user.bank_statuses


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        user = request.user
        disabled_fields = set()  # type: Set[str]

        if not user.is_superuser:
            disabled_fields |= {
                'manager',
                'sale_report',
                'expense_report',
                'bank',
                'deposit',
                'withdraw',
            }



        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form

    def get_total(self, request):
        user = request.user
        if user.roles.is_manager:
            banks = user.banks
            m_bank_status = user.bank_statuses
        else:
            banks = user.roles.manager.banks
            m_bank_status = user.roles.manager.bank_statuses
        total = 0
        for b in banks.all():
            filtered_bank_status =  m_bank_status.filter(bank=b)
            if filtered_bank_status:
                latest = filtered_bank_status.order_by('-date').first()
                if latest.update:
                    total += latest.update
                else:
                    total += latest.total()
        return str(total)

    def changelist_view(self, request, extra_context=None):
        my_context = {
            'total': self.get_total(request),
        }
        return super(CustomBankStatusAdmin, self).changelist_view(request,
            extra_context=my_context)