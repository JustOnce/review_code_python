from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User

from .serializers import TransferSerializer
from .models import Users


class TransferViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TransferSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(True)

        amount = float(request.POST['amount'])
        sum_part = 0

        user_from = User.objects.get(id=request.data['user_from'])

        # ищем сумму на счёте пользователя
        us = user_from.users_set.all()

        if us:
            acc_sum = us[0].account

            inn_to = Users.objects.filter(inn=request.data['inn_to'])
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

                return Response(serializer.data)
            else:
                return Response('перевод не выполнен')
        else:
            acc_sum = 0
            return Response('На счёте недостаточно средств')
