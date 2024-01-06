import pandas as pd
import os
from unidecode import unidecode

def limpiar_y_analizar_csv(input_file, output_file):
    # Leer el archivo CSV y limpiar los datos
    df = pd.read_csv(input_file, encoding='utf-8')
    df = df.applymap(lambda x: unidecode(str(x)) if pd.notnull(x) else x)

    # Organizar las columnas si es necesario
    # Puedes personalizar el orden de las columnas según tus necesidades
    column_order = ['departamento','codigodanedepartamento','municipio','codigodanemunicipio','tipoarea','sitio','ano','mes','rangoedad','grupoetnico','condicion','estado','genero','latitudcabecera','longitudcabecera','tipoevento','Ubicación','Actividad']
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

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.realpath(__file__))
    input_csv = f"{base_dir}/data/Situaci_n_V_ctimas_Minas_Antipersonal_en_Colombia_20240103.csv"
    output_csv = f"{base_dir}/data/Situaci_n_V_ctimas_Minas_Antipersonal_en_Colombia_20240103_resultado.csv"

    limpiar_y_analizar_csv(input_csv, output_csv)
