from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.db import transaction, models
from .serializers import TransferSerializer
from .models import Users


class TransferViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TransferSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)  # context
        serializer.is_valid(True)
        data = serializer.data
        amount = data['amount']
        with transaction.atomic():
            user_from = User.objects.prefetch_related('users_set').filter(id=data['user_from']).first()

            # ищем сумму на счёте пользователя
            us = user_from.users_set.all().first()

            if us:
                acc_sum = us.account

                inn_to = Users.objects.filter(inn=data['inn_to'])

                if inn_to.exists() and acc_sum >= amount:
                    users_count = inn_to.count()
                    sum_part = round(amount / users_count, 2)

                    # со счёта донора списать всю сумму

                    result_sum = float(acc_sum) - sum_part * users_count
                    us.account = result_sum
                    us.save()

                    # на счёт каждого записать по части
                    inn_to.update(account=models.F('account') + sum_part)

                    return Response(serializer.data)
                else:
                    return Response('перевод не выполнен', status=status.HTTP_400_BAD_REQUEST)
            else:

                return Response('На счёте недостаточно средств', status=status.HTTP_400_BAD_REQUEST)
