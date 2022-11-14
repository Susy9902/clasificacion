from django.db import models


# Create your models here.
class DB_global(models.Model):
    CRITERIO_CHOICES = (
        (0, "Conexa"),
        (1, "Compacta"),
        (2, "Fuertemente conexa"),
        (3, "Fuertemente compacta"),
        (4, "Completo maximal"),
    )

    CALCULADO_CHOICES = (
        (0, "Minimo"),
        (1, "Medio"),
        (2, "Maximo"),
    )

    nombre = models.CharField(verbose_name="nombre", max_length=255)
    criterio = models.IntegerField(choices=CRITERIO_CHOICES, default=0)
    calculado = models.IntegerField(choices=CALCULADO_CHOICES, default=0)
    umbral = models.FloatField(default=0)
    created = models.DateField(auto_created=True, auto_now=True)


class DB_rasgos(models.Model):
    CRITERIO_CHOICES = (
        (0, "Nominal"),  # Trabaja igual que el Booleano a la hora de trabajar en el clasificar
        (1, "Booleano"),
        (2, "Cuantitativo"),
        (3, "Por intervalos"),
    )

    nombre = models.CharField(verbose_name="nombre", max_length=50)
    criterio = models.IntegerField(choices=CRITERIO_CHOICES, default=0)
    db_global_id = models.ForeignKey(DB_global, on_delete=models.CASCADE)


class DB_rasgo_dominio(models.Model):
    valor = models.CharField(max_length=50)
    db_rasgos_id = models.ForeignKey(DB_rasgos, on_delete=models.CASCADE)


class DB_objetos(models.Model):
    db_global_id = models.ForeignKey(DB_global, on_delete=models.CASCADE)
    nombre = models.CharField(verbose_name="nombre", max_length=50)


class DB_grupos(models.Model):
    db_objeto_id = models.ForeignKey(DB_objetos, on_delete=models.CASCADE)
    grupo = models.IntegerField()


class DB_objetos_rasgos(models.Model):
    db_objetos_id = models.ForeignKey(DB_objetos, on_delete=models.CASCADE)
    db_rasgos_dominio_id = models.ForeignKey(DB_rasgo_dominio, on_delete=models.CASCADE)
