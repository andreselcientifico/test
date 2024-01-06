from tkinter import ttk,filedialog
from matplotlib import pyplot as plt
from unidecode import unidecode
from PIL import Image, ImageTk
import seaborn as sns
import tkinter as tk
import pandas as pd
import json


class DataProcessing(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        self.root.title("Conversion y Analisis")
        plt.style.use('dark_background')


        # Estilo
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")
        style.configure("TEntry", padding=5, relief="flat", background="#eee")


        self.directory_path = tk.StringVar()
        self.guardar_path = tk.StringVar()


        self.cargar_valores_desde_archivo()

        # Frame principal
        main_frame = ttk.Frame(root, padding=(20, 10))
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar favicon
        favicon_path = "favicon.webp"
        favicon = Image.open(favicon_path)
        favicon = ImageTk.PhotoImage(favicon)
        root.tk.call('wm', 'iconphoto', root._w, favicon)


         # Sección Directorio de Imágenes
        ttk.Label(main_frame, text="Directorio de CSV:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.directory_entry = ttk.Entry(main_frame, textvariable=self.directory_path)
        self.directory_entry.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        ttk.Button(main_frame, text="Seleccionar Directorio", command=self.browse_directory, style="TButton").grid(row=0, column=2, padx=10, pady=10, sticky=tk.W)

        # Sección Directorio para Guardar
        ttk.Label(main_frame, text="Directorio para Guardar:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.guardar_entry = ttk.Entry(main_frame, textvariable=self.guardar_path)
        self.guardar_entry.grid(row=1, column=1, padx=10, pady=10, sticky=(tk.W, tk.E))
        ttk.Button(main_frame, text="Seleccionar Directorio para Guardar", command=self.browse_guardar_directory, style="TButton").grid(row=1, column=2, padx=10, pady=10, sticky=tk.W)

         # botón de editar valores
        ttk.Button(main_frame, text="convertir", command=self.limpiar_y_analizar_csv, style="TButton").grid(row=2, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))

    def cargar_valores_desde_archivo(self):
        try:
            with open("configuracion_ajustes_entrenamiento.json", "r") as file:
                datos = json.load(file)
                self.directory_path.set(datos.get("directorio", ""))
                self.guardar_path.set(datos.get("directorio_guardar", ""))
        except FileNotFoundError:
            # Manejar el caso en que el archivo no existe
            self.guardar_valores_en_archivo()

    def guardar_valores_en_archivo(self):
        datos = {
            "directorio": self.directory_path.get(),
            "directorio_guardar": self.guardar_path.get(),
        }
        with open("configuracion_ajustes_entrenamiento.json", "w") as file:
            json.dump(datos, file)

    def browse_directory(self):
        archivo_path = filedialog.askopenfilename()
        if archivo_path:
            self.directory_path.set(archivo_path)
            self.guardar_valores_en_archivo()

    def browse_guardar_directory(self):
        guardar_path = filedialog.askdirectory()
        if guardar_path:
            self.guardar_path.set(guardar_path)
            self.guardar_valores_en_archivo()  # Guardar los valores actualizados en el archivo


    def limpiar_y_analizar_csv(self):
        input_file = self.directory_path.get()
        output_file = self.guardar_path.get()
        # Leer el archivo CSV y limpiar los datos
        df = pd.read_csv(input_file, encoding='utf-8')
        df = df.applymap(lambda x: unidecode(str(x)) if pd.notnull(x) else x)

        # Organizar las columnas si es necesario
        # Puedes personalizar el orden de las columnas según tus necesidades
        column_order = ['departamento','codigodanedepartamento','municipio','codigodanemunicipio','tipoarea','sitio','ano','mes','rangoedad','grupoetnico','condicion','estado','genero','latitudcabecera','longitudcabecera','tipoevento','Ubicación','Actividad']
        df = df[column_order]

        # Guardar el DataFrame limpio en un nuevo archivo CSV
        df.to_csv(output_file + '_limpio.csv', index=False, encoding='utf-8')

        # Gráficos de barras
        plt.figure(figsize=(12, 8))

        # Gráfico de víctimas por año
        plt.subplot(2, 3, 1)
        sns.countplot(x='ano', data=df)
        plt.title('Víctimas por Año')

        # Gráfico de víctimas por mes
        plt.subplot(2, 3, 2)
        sns.countplot(x='mes', data=df)
        plt.title('Víctimas por Mes')

        # Gráfico de víctimas por departamento
        plt.subplot(2, 3, 3)
        sns.countplot(x='departamento', data=df)
        plt.title('Víctimas por Departamento')
        plt.xticks(rotation=45, ha='right')

        # Gráfico de víctimas por actividad
        plt.subplot(2, 3, 4)
        sns.countplot(x='Actividad', data=df)
        plt.title('Víctimas por Actividad')
        plt.xticks(rotation=45, ha='right')

        # Gráfico de víctimas por género
        plt.subplot(2, 3, 5)
        sns.countplot(x='genero', data=df)
        plt.title('Víctimas por Género')

        # Gráfico de víctimas por estado
        plt.subplot(2, 3, 6)
        sns.countplot(x='estado', data=df)
        plt.title('Víctimas por Estado')

        plt.tight_layout()

        # Guardar la figura en un archivo de imagen
        plt.savefig(output_file + '_graficos.png')

        # Mostrar la gráfica en una ventana
        plt.show()

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
    root = tk.Tk()
    app = DataProcessing(root)
    root.mainloop()