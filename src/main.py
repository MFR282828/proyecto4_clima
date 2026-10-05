import sys
from src.apis import ClienteAPIClima


def mostrar_menu():
    print("\n========================================")
    print(" SISTEMA DE ALERTAS Y RIESGOS CLIMÁTICOS")
    print("========================================")
    print("1. Consultar clima y riesgo por ciudad")
    print("2. Evaluar lista predefinida de ciudades")
    print("3. Salir")


def main():
    cliente_api = ClienteAPIClima()
    historial_lecturas = []

    while True:
        mostrar_menu()
        opcion = input("\nSeleccione una opción (1-3): ").strip()

        if opcion == "1":
            ciudad = input(
                "\nIngrese el nombre de la ciudad (ej. Lima, Arequipa, Cusco): "
            ).strip()
            if not ciudad:
                print("[ADVERTENCIA] Debe ingresar un nombre válido.")
                continue

            print(f"\nConsultando API para '{ciudad}'...")
            lectura = cliente_api.obtener_clima_por_ciudad(ciudad)

            if lectura:
                historial_lecturas.append(lectura)
                print("\nResultado:")
                print(lectura)

        elif opcion == "2":
            ciudades_evaluar = ["Lima", "Cusco", "Puno", "Piura", "Arequipa"]
            print("\nProcesando lote de ciudades...")

            for c in ciudades_evaluar:
                lectura = cliente_api.obtener_clima_por_ciudad(c)
                if lectura:
                    historial_lecturas.append(lectura)
                    print(lectura)

        elif opcion == "3":
            print("\nCerrando aplicación... ¡Hasta pronto!")
            sys.exit(0)

        else:
            print("\n[ERROR] Opción no válida. Intente del 1 al 3.")


if __name__ == "__main__":
    main()