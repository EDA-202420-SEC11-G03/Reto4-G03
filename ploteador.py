import matplotlib.pyplot as plt

# Datos de la tabla
tamanos = [10, 20, 30, 40, 50, 60, 70, 80, 90, "large"]
tiempos = [
    0.072639008274866, 0.200805998274829, 0.226251982745000,
    0.2314057482787873, 0.20925082630083, 0.44708993849602,
    0.396745900000006, 0.411229137400005, 0.428274839283929,
    0.4824579999985872
]

# Reemplazar "large" por un valor numérico para graficar
tamanos_numericos = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# Crear la gráfica de líneas
plt.figure(figsize=(10, 6))
plt.plot(tamanos_numericos, tiempos, marker='o', linestyle='-', label="Tiempos de Ejecución")
plt.title("Tiempos de Ejecución Simulados", fontsize=14)
plt.xlabel("Tamaño del Problema", fontsize=12)
plt.ylabel("Tiempo (s)", fontsize=12)
plt.xticks(tamanos_numericos, labels=tamanos)
plt.grid(True)
plt.legend()
plt.tight_layout()

# Guardar la gráfica como imagen
plt.savefig("./tiempos_ejecucion_simulados.png")
plt.show()