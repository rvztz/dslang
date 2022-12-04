# dslang
Proyecto final para la clase de compiladores Ago - Dic 2022


## Configuración
Para instalar:
- `make install`

Una vez instalado, un nuevo virtual environment será creado en el directorio actual. 

Para activar el entorno:
- `source venv/bin/activate` en bash
- `venv\Scripts\activate.bat` en cmd

Una vez activado el entorno, para compilar un archivo:
- `python dlang.py <nombre_del_archivo>`

## Uso
**Program ID**: programa en dlang debe empezar con el siguiente identificador:
```c#
program my_program;
```
Este identificadorr no puede ser redefinido o declarado otra vez en el código. 

**Variables**: Las variables en dslang son *strongly typed*. Al declarar una variable, se debe declarar también el tipo. En el caso de los arreglos, se deben instanciar las dimensiones usando constantes enteras. 

```c#
var float: myfloat; 
var int: arr[4][4];
```

El lenguaje soporta los siguientes tipos para declaración de variables:
- *int*: Números enteros
- *float*: Números flotantes
- *string*: Letreros. Deben declararse entre ''.
- *bool*: [True/False]

Es posible declarar y asignar variables usando el operador `:=`. Este operador instancia una nueva variable y asigna el tipo y valor del lado derecho:

```c#
idx := 0;
my_new_float := 2.0;
my_str := 'hola mundo';
```

**Input/Output** 
Para imprimir algún valor se debe usar el comando `write()`:
```c#
my_str := 'hola mundo';
write(my_str);
```

`write()` no soporta impresión de llamadas a funciones o expresiones. Sin embargo, estas pueden ser asignadas para ser impresas.

Para ingresar valores desde la consola se puede usar el comando `read()`
```c#
var int: xj;
read(xj);
write(xj);
```


