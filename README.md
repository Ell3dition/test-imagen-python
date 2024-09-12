# Introduction
Este servicio esta dentro del proyecto de Salud en AquaChile, este modulo se encarga de almacenar los nuevos casos
de necropsia en conjunto con sus registros fotograficos.

1. Centros y Jaulas:
	- GET /centers: Devuelve los centros a los que pertenece el usuario junto con las jaulas asociadas

2. Necropsia Casos:
	- GET /necropsy_cases: Devuelve todos los Casos de necropsia en conjunto con sus registros, filtrado por usuario en los ultimos 7 días.
	- POST /necropsy_cases: Crea todos los casos enviados en una lista

3. Necropsia Analisis:
   	- GET /analysis/characteristics/: Devuelve los datos maestros de la tabla necropsia_caracteristicas
	- GET /analysis/{id_analysis}/: Devuelve la información para un analisis de necropsia en especifico
    - POST /analysis/: Crea un analisis de necropsia para un registro.

4. Necropsia Diagnosticos
	- GET /diagnostics/{id_diagnostic}/: Devuelve la información para un Diagnostico de necropsia en especifico
    - POST /diagnostics/: Crea un diagnostico de necropsia para un caso.


# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
2.	Software dependencies
3.	Latest releases
4.	API references

# Build and Test
TODO: Describe and show how to build your code and run the tests.

# Contribute
TODO: Explain how other users and developers can contribute to make your code better.

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)
