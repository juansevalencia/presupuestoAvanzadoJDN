from flask import Flask, render_template, request, send_file, session
from openpyxl import load_workbook
from datetime import date
import os

app = Flask(__name__)
app.secret_key = "clave_secreta_para_session"

# --- Configuración de plantillas ---
PRESUPUESTOS = {
    "estacado": {
        "plantilla": "plantillas/estacado.xlsx",
        "campos": {
            "ubicacion": "A3",
            "metros": "B11",
            "precio": "D11",
        },
    },
    "nivelacion": {
        "plantilla": "plantillas/nivelacion.xlsx",
        "campos": {
            "ubicacion": "A3",
            "Cantidad Camiones tierra negra con mano de obra": "B12",
            "Precio Camiones tierra negra con mano de obra": "D12",
            "Cantidad Camiones de Relleno": "B13",
            "Precio Camiones de Relleno": "D13",
            "Cantidad Mano de obra fina de tierra negra": "B14",
            "Precio Mano de obra fina de tierra negra": "D14",
            "Tipo de Pasto": "C16",
            "Cantidad Pasto": "B16",
            "Precio Colocacion": "D17",
        },
    },
    "riego": {
        "plantilla": "plantillas/riego.xlsx",
        "campos": {
            "ubicacion": "A4",
            "Costo Materiales de reigo": "D10",
            "Precio Automatizacion": "D11",
            "Precio Mano de obra": "D12",
        },
    },
}

# --- FUNCIONES DE GENERACIÓN POR TIPO ---

def generar_estacado(data):
    conf = PRESUPUESTOS["estacado"]
    wb = load_workbook(conf["plantilla"])
    ws = wb.active

    for campo, celda in conf["campos"].items():
        if campo in data and data[campo]:
            ws[celda] = data[campo]

    ws["A5"] = date.today().strftime("%d/%m/%Y")
    nombre_archivo = f"estacado_{data.get('ubicacion', '')}.xlsx"
    wb.save(nombre_archivo)

    # Calcular total simple
    metros = float(data.get("metros") or 0)
    precio = float(data.get("precio") or 0)
    total = metros * precio
    return nombre_archivo, total


def generar_nivelacion(data):
    conf = PRESUPUESTOS["nivelacion"]
    wb = load_workbook(conf["plantilla"])
    ws = wb.active

    for campo, celda in conf["campos"].items():
        if campo in data and data[campo]:
            ws[celda] = data[campo]

    ws["A5"] = date.today().strftime("%d/%m/%Y")
    nombre_archivo = f"nivelacion_{data.get('ubicacion', '')}.xlsx"
    wb.save(nombre_archivo)

    # Supongamos que el total es suma de precios * cantidades
    try:
        total = (
            float(data.get("Cantidad Camiones tierra negra con mano de obra", 0)) * float(data.get("Precio Camiones tierra negra con mano de obra", 0))
            + float(data.get("Cantidad Camiones de Relleno", 0)) * float(data.get("Precio Camiones de Relleno", 0))
            + float(data.get("Cantidad Mano de obra fina de tierra negra", 0)) * float(data.get("Precio Mano de obra fina de tierra negra", 0))
            + float(data.get("Cantidad Pasto", 0)) * float(data.get("Precio Colocacion", 0))
        )
    except ValueError:
        total = 0

    return nombre_archivo, total


def generar_riego(data):
    conf = PRESUPUESTOS["riego"]
    wb = load_workbook(conf["plantilla"])
    ws = wb.active

    for campo, celda in conf["campos"].items():
        if campo in data and data[campo]:
            ws[celda] = data[campo]

    ws["A5"] = date.today().strftime("%d/%m/%Y")
    nombre_archivo = f"riego_{data.get('ubicacion', '')}.xlsx"
    wb.save(nombre_archivo)

    try:
        total = (
            float(data.get("Costo Materiales de reigo", 0))
            + float(data.get("Precio Automatizacion", 0))
            + float(data.get("Precio Mano de obra", 0))
        )
    except ValueError:
        total = 0

    return nombre_archivo, total


# --- RUTAS FLASK ---

@app.route("/")
def index():
    return render_template("index.html", tipos=PRESUPUESTOS.keys())


@app.route("/formulario/<tipo>")
def formulario(tipo):
    if tipo not in PRESUPUESTOS:
        return "Tipo de presupuesto inválido", 400
    return render_template("formulario.html", tipo=tipo, campos=PRESUPUESTOS[tipo]["campos"].keys())


@app.route("/agregar", methods=["POST"])
def agregar():
    tipo = request.form["tipo"]
    if tipo not in PRESUPUESTOS:
        return "Tipo inválido", 400

    data = dict(request.form)

    if "resumen" not in session:
        session["resumen"] = {}

    if tipo == "estacado":
        archivo, total = generar_estacado(data)
        session["resumen"]["total_estacado"] = total

    elif tipo == "nivelacion":
        archivo, total = generar_nivelacion(data)
        session["resumen"]["total_nivelacion"] = total

    elif tipo == "riego":
        archivo, total = generar_riego(data)
        session["resumen"]["total_riego"] = total

    session["resumen"]["ubicacion"] = data.get("ubicacion", "")
    session.modified = True

    return send_file(archivo, as_attachment=True)


@app.route("/resumen")
def resumen():
    resumen_data = session.get("resumen", {})
    if not resumen_data:
        return "No hay presupuestos cargados todavía."

    wb = load_workbook("resumen.xlsx")
    ws = wb.active

    ws["A3"] = resumen_data.get("ubicacion", "")
    ws["A5"] = date.today().strftime("%d/%m/%Y")
    ws["C11"] = resumen_data.get("total_nivelacion", 0)
    ws["C13"] = resumen_data.get("total_riego", 0)
    ws["C15"] = resumen_data.get("total_estacado", 0)

    resumen_filename = "resumen_general.xlsx"
    wb.save(resumen_filename)

    return send_file(resumen_filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
