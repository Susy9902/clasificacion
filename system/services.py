from typing import List, Tuple, Optional
from datetime import datetime
from django.shortcuts import get_object_or_404
from system.models import DB_global, DB_objetos, DB_rasgos, DB_rasgo_dominio, DB_grupos, DB_objetos_rasgos
from system.validators import Validator
from django.contrib.auth.decorators import login_required


class DB_GlobalService:
    def add(self, nombre: str, rasgos: List[dict]) -> Optional[DB_global]:
        # Validate data
        if not Validator.db_is_valid({'nombre': nombre, 'rasgos': rasgos}):
            return None

        # Agregar modelo DB Global
        model = DB_global()
        model.nombre = nombre
        model.save()
        
        # Agregar modelo rasgos
        for rasgo in rasgos:
            rasgo_model = DB_rasgos()
            rasgo_model.nombre = rasgo.get('nombre')
            rasgo_model.criterio = rasgo.get('criterio')
            rasgo_model.db_global_id = model
            rasgo_model.save()
            
            # Agregar Dominio
            for dominio in rasgo.get('dominio'):
                dominio_model = DB_rasgo_dominio()
                dominio_model.valor = dominio
                dominio_model.db_rasgos_id = rasgo_model
                dominio_model.save()
        return model
        
    def detail_modificar(self, pk: int) -> List[dict]:
        lista, tmp = [], []
        for rasgo in DB_rasgos.objects.filter(db_global_id__id=pk):
            tmp = []
            for dominio in DB_rasgo_dominio.objects.filter(db_rasgos_id=rasgo):
                tmp.append(dominio.valor if rasgo.criterio != 3 else [x for x in dominio.valor.split('-')])
            lista.append({
                'nombre': rasgo.nombre,
                'criterio': rasgo.criterio,
                'dominio': tmp
            })
        return lista
        
    def detail(self, pk: int) -> List[dict]:        
        lista, tmp = [], []
        for rasgo in DB_rasgos.objects.filter(db_global_id__id=pk):
            tmp = []
            for dominio in DB_rasgo_dominio.objects.filter(db_rasgos_id=rasgo):
                tmp.append(dominio.valor)
            lista.append({
                'nombre': rasgo.nombre,
                'criterio': rasgo.criterio,
                'dominio': tmp
            })
        return lista
    
        # return [{
        #         'nombre': rasgo.nombre,
        #         'criterio': rasgo.criterio,
        #         'dominio': [dominio.valor for dominio in DB_rasgo_dominio.objects.filter(db_rasgos_id=rasgo)]
        #     } for rasgo in DB_rasgos.objects.filter(db_global_id__id=pk)]
    
    def delete(self, pk: int) -> None:
        model = get_object_or_404(DB_global, pk=pk)
        if model is not None:
            model.delete()
    
    def edit(self, pk: int, nombre: str, rasgos: List[dict]) -> None:
        # Editar modelo DB Global
        model = DB_global.objects.get(pk=pk)
        if model is None:
            return None
        
        # Validate data
        if not Validator.db_is_valid({'nombre': nombre, 'rasgos': rasgos}):
            return None
        
        model.nombre = nombre
        model.save()
        
        # Eliminar todos los rasgos para meter los nuevos
        DB_rasgos.objects.filter(db_global_id__id=pk).delete()
        
        # Agregar modelo rasgos
        for rasgo in rasgos:
            rasgo_model = DB_rasgos()
            rasgo_model.nombre = rasgo.get('nombre')
            rasgo_model.criterio = rasgo.get('criterio')
            rasgo_model.db_global_id = model
            rasgo_model.save()
            
            # Agregar Dominio
            for dominio in rasgo.get('dominio'):
                dominio_model = DB_rasgo_dominio()
                dominio_model.valor = dominio
                dominio_model.db_rasgos_id = rasgo_model
                dominio_model.save()
        return model
    
    def list(self) -> List[DB_global]:
        return DB_global.objects.all().order_by('created')


class DB_gruposService:
    def crear_matriz_semejanza(self, db_global) -> List[List[Tuple]]:
        """Armar la matriz de semajanza y guardar el valor con la asociacion entre objetos"""
        items = []
        for model in DB_objetos.objects.filter(db_global_id=db_global):
            items.append({
                'id': model.id,
                'nombre': model.nombre,
                'dominio': [
                rasgo.db_rasgos_dominio_id.valor for rasgo in
                DB_objetos_rasgos.objects.filter(db_objetos_id=model).order_by('db_rasgos_dominio_id__db_rasgos_id__nombre')
            ]})

        table = [[-1 for _ in range(len(items))] for _ in range(len(items))]
        for i in range(len(items)):
            for j in range(len(items)):
                arr_1 = items[i]['dominio']
                arr_2 = items[j]['dominio']
                tmp = []
                for k in range(len(arr_1)):
                    tmp.append(1 if arr_1[k] == arr_2[k] else 0)
                valor = sum(tmp) / len(arr_2)
                table[i][j] = (items[i]['id'], items[j]['id'], valor, items[j]['nombre'])
        return table

    def mostrar_matriz_semajanza(self, db_global):
        """Mostrar la matriz de semanajza a partir de la generada"""
        matriz = self.crear_matriz_semejanza(db_global)
        if len(matriz) == 0:
            return []

        objetos = [x[3] for x in matriz[0]]

        headers = ['']
        headers.extend(objetos)
        tabla = [headers]
        for i in range(len(matriz)):
            tmp = [objetos[i]]
            for j in range(len(matriz)):
                tmp.append(round(matriz[i][j][2], 4))
            tabla.append(tmp)
        return tabla
    
    def agrupar_matriz(self, db_global, umbral):
        """Guardar los resultados de la agrupacion de una base de datos"""
        matriz = self.crear_matriz_semejanza(db_global)
        if len(matriz) == 0:
            return []

        # Matriz => values [FIL_OBJ, COL_OBJ, SEMEJANZA]
        restantes = [x[1] for x in matriz[0]]  # Extraer todos los objectos de las columnas
        visitadas, grupos = [], []
        for i in range(len(matriz)):
            # No revisar objectos en la fila no recorridos
            if matriz[i][0][1] in visitadas:
                continue

            self._create_group(matriz, grupos, visitadas, restantes, umbral, i)
        
        # Agregar los restantes en un grupo aparte
        if len(restantes) > 0:
            grupos.append(restantes)
        return grupos
    
    def _create_group(self, matriz, grupos, visitadas, restantes, umbral, i):
        # Mayor => values [SEMEJANZA, OBJECT]
        mayor = self._buscar_mayor_matriz(matriz, visitadas, i)

        # Verificar si se encontro un mayor
        if mayor[1] is None:
            return

        # Armamos el grupo
        grupo = []
        if umbral <= mayor[0]:
            obj = matriz[i][0][0]  # matriz[i][mayor[1]][1]
            
            # Agregar encontrado al grupo
            visitadas.append(obj)
            restantes.remove(obj)
            grupo.append(obj)
            
            self._set_grupo(matriz, grupo, visitadas, restantes, umbral, mayor[1])
            if len(grupo) > 0:
                grupos.append(grupo)
    
    def _set_grupo(self, matriz, grupo, visitadas, restantes, umbral, i):
        obj = matriz[i][0][0]  # matriz[i][mayor[1]][1]
        
        # Agregar encontrado al grupo
        visitadas.append(obj)
        restantes.remove(obj)
        grupo.append(obj)

        # Mayor => values [SEMEJANZA, OBJECT]
        mayor = self._buscar_mayor_matriz(matriz, visitadas, i)

        # Verificar si se encontro un mayor
        if mayor[1] is None:
            return
    
        # print('A', i, obj, matriz[mayor[1]][0][2], mayor[1])

        if umbral <= mayor[0]:
            self._set_grupo(matriz, grupo, visitadas, restantes, umbral, mayor[1])
    
    def _get_grupo(self, matriz, umbral, mayor, grupo, visitadas, restantes, i):
        # Comprobamos e umbral con la mayor semejanza no visitada
        obj = matriz[i][0][0]  # matriz[i][mayor[1]][1]
        # print('A', i, obj, matriz[i][0][2], mayor[1])

        if umbral <= mayor[0]:
            visitadas.append(obj)
            restantes.remove(obj)

            # Agregar encontrado al grupo
            grupo.append(obj)

            obj = matriz[mayor[1]][0][0]
            grupo.append(obj)
            visitadas.append(obj)
            restantes.remove(obj)

            # Busco el siguiente mayor
            i = mayor[1]
            mayor = self._buscar_mayor_matriz(matriz, visitadas, i)
            # print('B', i, obj, matriz[mayor[1]][0][2], mayor[1])

            # Verificar si se encontro un mayor
            if mayor[1] is None:
                return
            self._get_grupo(matriz, umbral, mayor, grupo, visitadas, restantes, i)

    def _buscar_mayor_matriz(self, matriz, visitadas, fil):
        mayor = (-9999, None)
        # Mayor => values [SEMEJANZA, OBJECT]
        for j in range(len(matriz)):
            if matriz[fil][j][1] in visitadas or fil == j:
                continue
            if matriz[fil][j][2] > mayor[0]:
                # print('mayor', matriz[fil][j][2], j)
                mayor = (matriz[fil][j][2], j)
        return mayor

    def calcular_umbral(self, db_global: int, tipo: str) -> float:
        matriz = self.crear_matriz_semejanza(db_global)
        # Matriz => values [FIL_OBJ, COL_OBJ, SEMEJANZA]
        
        if tipo == '0':
            minimos = []
            for fil in range(len(matriz)):
                menor = 9999
                for col in range(len(matriz)):
                    if fil == col:
                        continue

                    if matriz[fil][col][2] < menor:
                        menor = matriz[fil][col][2]
                minimos.append(menor)
            mayor = -9999
            for min in minimos:
                if min > mayor:
                    mayor = min
            return round(mayor, 4)
        if tipo == '1':
            suma_max = 0
            for fil in range(len(matriz)):
                mayor = -9999
                for col in range(len(matriz)):
                    if fil == col:
                        continue

                    if matriz[fil][col][2] > mayor:
                        mayor = matriz[fil][col][2]
                suma_max += mayor
            return round(suma_max / len(matriz), 4)
        if tipo == '2':
            suma = 0
            for fil in range(len(matriz)):
                for col in range(fil+1, len(matriz)):
                    suma += matriz[fil][col][2]
            return round((2 * suma) / (len(matriz)*(len(matriz) - 1)), 4)
        return 1

    def mostrar_grupos(self, pk: int) -> List[list]:
        """Mostrar los grupos de la base de datos"""
        grupos = []
        visited = []
        for grupo in DB_grupos.objects.filter(db_objeto_id__db_global_id=pk).order_by('grupo').order_by('id'):
            if grupo.grupo in visited:
                grupos[grupo.grupo].append(grupo.db_objeto_id.nombre)
            else:
                grupos.append([grupo.db_objeto_id.nombre])
                visited.append(grupo.grupo)
        return grupos
    
    def clasificar(self, pk: int, criterio: int, umbral: float, calculado: int, groups: List[list]) -> None:
        """
        Clasificar elementos:
            Pasos:
                1 - Asignar valores (Criterio, Umbral, etc ...)
                2 - Agrupar por objetos
        """
        # Editar modelo DB Global
        model = DB_global.objects.get(pk=pk)
        if model is None:
            return
        model.criterio = criterio
        model.calculado = calculado
        model.umbral = umbral
        model.save()
        
        deleted = DB_grupos.objects.filter(db_objeto_id__db_global_id=pk).delete()
        i = 0
        for grupo in groups:
            for element in grupo:
                try:
                    obj = DB_grupos()
                    obj.db_objeto_id = DB_objetos.objects.get(pk=element)
                    obj.grupo = i
                    obj.save()
                except DB_objetos.DoesNotExist:
                    pass
            i += 1

class DB_ObjetosService:
    def add_list(self, db_global: int, items: List[dict]) -> None:
        # Remove before item
        DB_objetos.objects.filter(db_global_id=db_global).delete()

        for item in items:
            self.add(db_global, item.get('nombre'), item.get('rasgos'))

    def add(self, pk: int, nombre: str, rasgo_valores: List[int]) -> None:
        try:
            db = DB_global.objects.get(id=pk)
            # Agregar modelo DB objetos
            model = DB_objetos.objects.get_or_create(nombre=nombre, db_global_id=db)
            
            # Remove all valores
            if not model[1]:
                delete_ids = DB_objetos_rasgos.objects.filter(db_objetos_id=model[0]).delete()
            
            # Agregar valores de los rasgos
            for rasgo in rasgo_valores:
                try:
                    model_rasgo = DB_rasgo_dominio.objects.get(pk=int(rasgo))
                    obj = DB_objetos_rasgos()
                    
                    obj.db_objetos_id = model[0]
                    obj.db_rasgos_dominio_id = model_rasgo
                    obj.save()
                except DB_rasgo_dominio.DoesNotExist:
                    pass
        except DB_global.DoesNotExist:
            pass

    def get_rasgos(self, db_global):
        return [[{
                'id': item.id,
                'value': item.valor
                } for item in DB_rasgo_dominio.objects.filter(db_rasgos_id=rasgo.id)
            ] for rasgo in DB_rasgos.objects.filter(db_global_id=db_global).order_by('nombre')]

    def detail(self, db_global) -> Tuple[list, List[dict]]:
        return [item.nombre for item in DB_rasgos.objects.filter(db_global_id=db_global).order_by('nombre')], [{
                'nombre': model.nombre,
                'rasgos': [{
                    'id': rasgo.db_rasgos_dominio_id.id,
                    'value': rasgo.db_rasgos_dominio_id.valor,
                    'values': [{
                        'id': item.id,
                        'value': item.valor
                    } for item in DB_rasgo_dominio.objects.filter(db_rasgos_id=rasgo.db_rasgos_dominio_id.db_rasgos_id)]
                } for rasgo in DB_objetos_rasgos.objects.filter(db_objetos_id=model).order_by('db_rasgos_dominio_id__db_rasgos_id__nombre')]
            } for model in DB_objetos.objects.filter(db_global_id=db_global).order_by('nombre')]

    def full_detail(self, db_global) -> Tuple[list, List[List[str]]]:
        items = []
        for model in DB_objetos.objects.filter(db_global_id=db_global):
            tmp = [model.nombre]
            tmp.extend([
                rasgo.db_rasgos_dominio_id.valor for rasgo in
                DB_objetos_rasgos.objects.filter(db_objetos_id=model).order_by('db_rasgos_dominio_id__db_rasgos_id__nombre')
            ])
            items.append(tmp)
        return [item.nombre for item in DB_rasgos.objects.filter(db_global_id=db_global).order_by('nombre')], items
