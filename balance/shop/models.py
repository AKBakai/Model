from django.db import models
from django.forms import ValidationError

class User(models.Model):
    name = models.CharField(max_length=50, verbose_name='имя покупателя')
    money = models.IntegerField(verbose_name='деньги')


    
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


class Product(models.Model):
    nazvaniya = models.CharField(max_length=50, verbose_name='Продукт')
    price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, verbose_name='Цена')
    amount = models.PositiveIntegerField(default=1)



    def __str__(self) -> str:
        return self.nazvaniya

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_s')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_s')
    amount = models.PositiveIntegerField(default=1)
    full_price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    

    def __str__(self) -> str:
        return f'Покупатель: {self.user}, продукт: {self.product}'

    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'

    # def clean(self):        
    #     if self.user.money is None:
    #         raise ValidationError('У вас нету денег')
    #     check_sale = self.user.money >= self.product.price
    #     if check_sale:
    #         self.user.money = float(self.user.money) - float(self.product.price)
    #         self.user.save()
    #     else:
    #         raise ValidationError('Недостаточно средств')
    #     super().clean()


    def clean(self):
        self.full_price = self.amount * self.product.price
        check_sale = self.user.money >= self.full_price

        if self.user.money is None:
            raise ValidationError('У вас нету денег')
        
        if not check_sale:
            raise ValidationError('Недостаточно средств')
        
        if check_sale:
            self.user.money = float(self.user.money) - float(self.full_price)
            self.user.save()
            
        check_amount = self.product.amount >= self.amount
        if check_amount:
            self.product.amount = self.product.amount - self.amount
            self.product.save() 
        else:
            raise ValidationError('В складе есть кол-во {}'.format(check_amount))
        super().clean()
