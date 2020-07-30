from .models import Users
from .forms import TransferForm
from django.contrib.auth.models import User
from django.views.generic.edit import FormView


class TransferView(FormView):
    
    form_class = TransferForm
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx['userlist'] = self.userlist()

        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx['userlist'] = self.userlist()

        amount = float(request.POST['amount'])
        sum_part = 0

        user_from = User.objects.get(id=request.POST['user_from'])
        
        # ищем сумму на счёте пользователя
        us = user_from.users_set.all()

        if us:
            acc_sum = us[0].account

            inn_to = Users.objects.filter(inn=request.POST['inn_to'])
            users_count = 0
            
            if inn_to and acc_sum >= amount:
                users_count = len(inn_to)
                sum_part = round(amount / users_count, 2)

                # со счёта донора списать всю сумму
                res_user = user_from.users_set.get()
                result_sum = float(res_user.account) - sum_part * users_count
                res_user.account = result_sum
                res_user.save()

                # на счёт каждого записать по части
                for i in inn_to:
                    result_sum = float(i.account) + sum_part
                    i.account = result_sum
                    i.save()

                ctx['op_result'] = [acc_sum, users_count, sum_part]
            else:
                ctx['op_result'] = 'перевод не выполнен'

        else:
            acc_sum = 0
            ctx['op_result'] = 'На счёте недостаточно средств'

        return self.render_to_response(ctx)

    def userlist(self):
        user_list = []

        for i in User.objects.all():
            cur_user = {}
            cur_user['id'] = i.id
            cur_user['username'] = i.username
            if i.users_set.all():
                tmp = i.users_set.get()
                cur_user['inn'] = tmp.inn
                cur_user['account'] = tmp.account
            user_list.append(cur_user)

        return user_list
