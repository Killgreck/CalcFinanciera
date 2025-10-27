# 💰 Calculadora Financiera - Amortización de Créditos

Aplicación web desarrollada con Streamlit para calcular y gestionar tablas de amortización de créditos con soporte completo para diferentes tipos de tasas de interés y abonos extraordinarios.

## 🎯 Características

- ✅ Ingreso de parámetros del crédito (monto, tasa, plazo, frecuencia, fecha de inicio)
- ✅ Reconocimiento de tipo de tasa (nominal/efectiva, anticipada/vencida)
- ✅ Cálculo automático de tasa equivalente al periodo de pago
- ✅ Generación de tabla de amortización completa y verificable
- ✅ Registro de abonos extraordinarios (programados y ad-hoc)
- ✅ Recálculo automático con estrategias de reducción de cuota o plazo
- ✅ Exportación de resultados a CSV y Excel
- ✅ Visualizaciones interactivas con gráficos
- ✅ Interfaz intuitiva y responsive

## 📋 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/CalcFinanciera.git
cd CalcFinanciera
```

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## 💻 Uso

1. Ejecutar la aplicación:
```bash
streamlit run app.py
```

2. La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

3. Configurar los parámetros del crédito en el panel lateral:
   - Monto del crédito
   - Tipo de tasa (Nominal/Efectiva)
   - Modalidad (Vencida/Anticipada)
   - Tasa de interés
   - Frecuencia de la tasa
   - Plazo y frecuencia de pago
   - Fecha de inicio

4. Visualizar la tabla de amortización y gráficos

5. (Opcional) Agregar abonos extraordinarios y ver el recálculo automático

6. Exportar los resultados a CSV o Excel

## 📁 Estructura del Proyecto

```
CalcFinanciera/
├── app.py                          # Aplicación principal de Streamlit
├── requirements.txt                # Dependencias del proyecto
├── README.md                       # Este archivo
├── .gitignore                      # Archivos ignorados por Git
├── specc/                          # Especificaciones del proyecto
│   ├── 01.md                       # Requisitos funcionales
│   └── 02.md                       # Fórmulas financieras
├── src/
│   ├── utils/                      # Módulos de utilidades
│   │   ├── __init__.py
│   │   ├── interest_rates.py      # Conversión de tasas
│   │   ├── amortization.py        # Cálculo de amortización
│   │   └── export.py              # Exportación de datos
│   └── components/                 # Componentes de UI
│       ├── __init__.py
│       ├── input_form.py          # Formulario de entrada
│       ├── display.py             # Visualización de resultados
│       └── payments.py            # Gestión de abonos
└── exports/                        # Carpeta para archivos exportados
    └── .gitkeep
```

## 🧮 Fórmulas Implementadas

La aplicación implementa las siguientes fórmulas de ingeniería financiera:

### Conversión de Tasas
- Tasa Nominal a Efectiva periódica: `ep = Nominal / frecuencia`
- Tasa Anticipada a Efectiva: `ie = ia / (1 - ia)`
- Tasa Efectiva a Anticipada: `ia = ie / (1 + ie)`
- Equivalencia de tasas: `ie = (1 + i)^t - 1`

### Valor del Dinero en el Tiempo
- Valor Futuro: `VF = VP × (1 + i)^n`
- Valor Presente: `VP = VF / (1 + i)^n`

### Anualidades
- VP de Anualidad Vencida: `VP = A × [(1 - (1 + i)^-n) / i]`
- Cálculo de cuota: Despeje de A de la fórmula anterior

### Amortización
- Interés del periodo: `Interés = Saldo × tasa_periodo`
- Abono a capital: `Abono = Cuota - Interés`
- Nuevo saldo: `Saldo_nuevo = Saldo_anterior - Abono`

## 🛠️ Tecnologías Utilizadas

- **Streamlit**: Framework para aplicaciones web interactivas
- **Pandas**: Manipulación y análisis de datos
- **NumPy**: Cálculos numéricos
- **Plotly**: Visualizaciones interactivas
- **OpenPyXL**: Exportación a Excel
- **Python-dateutil**: Manejo de fechas

## 📊 Funcionalidades Detalladas

### Tipos de Tasa Soportados
- **Nominal**: Tasa anual que se divide por la frecuencia
- **Efectiva**: Tasa que considera capitalización compuesta
- **Anticipada**: Interés pagado al inicio del periodo
- **Vencida**: Interés pagado al final del periodo

### Frecuencias Soportadas
- Mensual
- Bimestral
- Trimestral
- Cuatrimestral
- Semestral
- Anual

### Estrategias de Abonos Extraordinarios
- **Reducir Plazo**: Mantiene la cuota original y reduce el número de pagos
- **Reducir Cuota**: Mantiene el plazo original y reduce el monto de cada cuota

## 📝 Ejemplos de Uso

### Ejemplo 1: Crédito Básico
- Monto: $100,000
- Tasa: 12% Nominal Anual Vencida
- Plazo: 12 meses
- Frecuencia: Mensual

### Ejemplo 2: Con Abono Extraordinario
- Mismo crédito del Ejemplo 1
- Abono de $10,000 en el periodo 6
- Estrategia: Reducir Plazo

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👤 Autor

Desarrollado con ❤️ usando Python y Streamlit

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias, por favor abre un issue en el repositorio de GitHub.

---

**Nota**: Esta aplicación utiliza fórmulas estándar de ingeniería financiera. Los resultados son aproximados y deben ser verificados con un asesor financiero profesional para decisiones importantes.
