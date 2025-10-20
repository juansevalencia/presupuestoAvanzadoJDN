# 🧾 Sistema de Generación de Presupuestos de Obras El Jardinero Del Norte

El Jardinero Del Norte requeria generar presupuestos en el momento de parte de la gente de ventas a la hora de visitar las obras.
En una epoca sin papel tener una computadora no es algo factible.
Tampoco tener una persona remota atras de una computadora solamente para llenar valores en un excel.
Este proyecto viene a dejar de lado el error humano y a dar un feedback inmediato para los clientes.

Este proyecto es una **aplicación web en Flask** diseñada para **automatizar la creación de presupuestos de obras** como *estacado*, *nivelación* y *riego*.  
Permite generar planillas de Excel profesionales a partir de formularios simples y consolidar los totales en un **resumen general automático**.

## 🚀 Funcionalidades principales

- 🧩 **Menú de presupuestos dinámico:** el usuario elige qué tipo de presupuesto generar (*estacado*, *nivelación*, *riego*).  
- 📝 **Formularios adaptables:** cada presupuesto muestra solo los campos relevantes definidos en el backend.  
- 📊 **Plantillas Excel personalizadas:** los datos ingresados se insertan automáticamente en las celdas correctas (`openpyxl`).  
- 📍 **Ubicación única:** la ubicación del proyecto se ingresa una sola vez y se reutiliza para todos los presupuestos.  
- 🧮 **Resumen general:** genera un `resumen_general.xlsx` con los totales de cada tipo de obra.  
- 💾 **Descarga inmediata:** cada presupuesto (y el resumen) se descarga directamente desde el navegador.

<img width="499" height="245" alt="image" src="https://github.com/user-attachments/assets/66f7c905-b172-47ea-90fa-c47b9bf97ecf" />

