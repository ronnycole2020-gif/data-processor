import os
import pandas as pd
from datetime import datetime

def main():
    # Leer rutas desde variables de entorno; si no existen, usar valores predeterminados (conveniente para pruebas)
    input_path = os.getenv("INPUT_PATH", "/data/input.csv")
    output_path = os.getenv("OUTPUT_PATH", "/data/output.csv")

    print(f"[{datetime.now()}] Iniciando procesamiento...")
    print(f"Entrada: {input_path}")
    print(f"Salida: {output_path}")

    # Leer CSV
    df = pd.read_csv(input_path)

    # Ejemplo de procesamiento: eliminar duplicados, añadir columna de tiempo de procesamiento
    df = df.drop_duplicates()
    df["processed_at"] = datetime.now().isoformat()

    # Escribir salida
    df.to_csv(output_path, index=False)

    print(f"Procesamiento completado. Filas: {len(df)}. Archivo escrito en: {output_path}")

if __name__ == "__main__":
    main()