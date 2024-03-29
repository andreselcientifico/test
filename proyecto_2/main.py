import pandas as pd
import os
from unidecode import unidecode

# Definir una función para limpiar y analizar el archivo CSV
def limpiar_y_analizar_csv(input_file, output_file):
    # Leer el archivo CSV y limpiar los datos
    df = pd.read_csv(input_file, encoding='utf-8')
    df = df.apply(lambda x: x.map(lambda y: unidecode(str(y)) if pd.notnull(y) else y))

    # Intercambiar la información entre las columnas 'estado' y 'genero'
    df['temp'] = df['estado']
    df['estado'] = df['genero']
    df['genero'] = df['temp']
    df = df.drop('temp', axis=1)

    # Mapear las etiquetas de género y estado de manera insensible a mayúsculas y minúsculas
    df['genero'] = df['genero'].str.lower().map({'hombre': 'Masculino', 'mujer': 'Femenino'})

    # Organizar las columnas si es necesario
    # Puedes personalizar el orden de las columnas según tus necesidades
    column_order = ['departamento', 'codigodanedepartamento', 'municipio', 'codigodanemunicipio', 'tipoarea', 'sitio', 'ano', 'mes', 'rangoedad', 'grupoetnico', 'condicion', 'estado', 'genero', 'latitudcabecera', 'longitudcabecera', 'tipoevento', 'Ubicación', 'Actividad']
    df = df[column_order]

    # Guardar el DataFrame limpio en un nuevo archivo CSV
    df.to_csv(output_file + '_limpio.csv', index=False, encoding='utf-8')

    # Información resumida en consola
    print("Total de víctimas por año:")
    print(df['ano'].value_counts().sort_index())

    print("\nTotal de víctimas por mes:")
    print(df['mes'].value_counts().sort_index())

    print("\nTotal de víctimas por departamento:")
    print(df['departamento'].value_counts())

    print("\nTotal de víctimas por actividad:")
    print(df['Actividad'].value_counts())

    print("\nTotal de víctimas por género:")
    print(df['genero'].value_counts())

    print("\nTotal de víctimas por estado:")
    print(df['estado'].value_counts())

    # Escribir la información resumida en un archivo de texto
    with open(output_file + '_resumen.txt', 'w', encoding='utf-8') as file:
        file.write("Total de víctimas por año:\n")
        file.write(str(df['ano'].value_counts().sort_index()) + '\n\n')

        file.write("Total de víctimas por mes:\n")
        file.write(str(df['mes'].value_counts().sort_index()) + '\n\n')

        file.write("Total de víctimas por departamento:\n")
        file.write(str(df['departamento'].value_counts()) + '\n\n')

        file.write("Total de víctimas por actividad:\n")
        file.write(str(df['Actividad'].value_counts()) + '\n\n')

        file.write("Total de víctimas por género:\n")
        file.write(str(df['genero'].value_counts()) + '\n\n')

        file.write("Total de víctimas por estado:\n")
        file.write(str(df['estado'].value_counts()) + '\n')

# Verificar si el script se ejecuta directamente
if __name__ == "__main__":
    # Obtener la ruta del directorio actual
    base_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Definir las rutas de entrada y salida del archivo CSV
    input_csv = f"{base_dir}/data/Situaci_n_V_ctimas_Minas_Antipersonal_en_Colombia_20240103.csv"
    output_csv = f"{base_dir}/data/Situaci_n_V_ctimas_Minas_Antipersonal_en_Colombia_20240103_resultado.csv"

    # Llamar a la función para limpiar y analizar el archivo CSV
    limpiar_y_analizar_csv(input_csv, output_csv)
