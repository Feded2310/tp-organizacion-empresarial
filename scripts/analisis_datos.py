# Alumno: Federico Javier Doello
# ANÁLISIS DE VENTAS
# Tecnicatura Universitaria en Programación - UTN 2026

import pandas as pd
import matplotlib.pyplot as plt
import os

# CARGA DE DATOS
ruta_datos = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'datos', 'ventas.csv')
df = pd.read_csv(ruta_datos)
df['fecha'] = pd.to_datetime(df['fecha'])

print("=" * 60)
print("ANÁLISIS DE VENTAS - TP ORGANIZACIÓN EMPRESARIAL")
print("=" * 60)
print(f"\nDataset cargado correctamente: {len(df)} registros encontrados.")

# CÁLCULO DE INDICADORES
df['monto_total'] = df['cantidad'] * df['precio_unitario']
total_ventas = df['monto_total'].sum()
print(f"\nVentas totales del período: $ {total_ventas:,.0f}")

ventas_por_producto = df.groupby('producto').agg(
    cantidad_total=('cantidad', 'sum'),
    monto_total=('monto_total', 'sum')
).reset_index()

producto_mas_vendido = ventas_por_producto.loc[ventas_por_producto['cantidad_total'].idxmax()]
print(f"Producto más vendido: {producto_mas_vendido['producto']} ({producto_mas_vendido['cantidad_total']} unidades)")

df['mes'] = df['fecha'].dt.to_period('M')
ventas_por_mes = df.groupby('mes')['monto_total'].sum().reset_index()
ventas_por_mes['mes_str'] = ventas_por_mes['mes'].astype(str)

print(f"\n--- VENTAS POR MES ---")
for _, fila in ventas_por_mes.iterrows():
    print(f"  {fila['mes_str']}: $ {fila['monto_total']:,.0f}")

# GENERACIÓN DE GRÁFICO
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Análisis de Ventas - TP UTN 2026', fontsize=14, fontweight='bold')

axes[0].bar(ventas_por_mes['mes_str'], ventas_por_mes['monto_total'], color='steelblue', edgecolor='white')
axes[0].set_title('Evolución Mensual de Ventas')
axes[0].set_xlabel('Mes')
axes[0].set_ylabel('Monto Total ($)')
axes[0].tick_params(axis='x', rotation=45)
axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x/1000:.0f}K'))

axes[1].barh(ventas_por_producto['producto'], ventas_por_producto['monto_total'], color='darkorange', edgecolor='white')
axes[1].set_title('Ingresos Totales por Producto')
axes[1].set_xlabel('Monto Total ($)')
axes[1].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x/1000:.0f}K'))

plt.tight_layout()

ruta_resultados = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resultados')
os.makedirs(ruta_resultados, exist_ok=True)
ruta_grafico = os.path.join(ruta_resultados, 'grafico_ventas.png')
plt.savefig(ruta_grafico, dpi=150, bbox_inches='tight')
print(f"\nGráfico guardado en: {ruta_grafico}")

print("\n" + "=" * 60)
print("Análisis completado exitosamente.")
print("=" * 60)
