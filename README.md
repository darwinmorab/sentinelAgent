# sentinelAgent

Sistema de monitoreo para productos de Punto de Venta (POS)

## Descripción

SentinelAgent es un agente de monitoreo diseñado para supervisar la salud y el rendimiento de sistemas de punto de venta. Proporciona:

- Monitoreo de recursos del sistema (CPU, memoria, disco)
- Verificación de salud de endpoints del POS
- Sistema de alertas basado en umbrales configurables
- Historial de métricas
- Registro detallado de eventos

## Características

- ✅ Monitoreo de recursos del sistema en tiempo real
- ✅ Health checks de endpoints HTTP/HTTPS
- ✅ Sistema de alertas configurables
- ✅ Soporte para configuración JSON y YAML
- ✅ Modo continuo y modo de ejecución única
- ✅ Registro de métricas con retención configurable
- ✅ Logs detallados con múltiples niveles

## Instalación

### Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/darwinmorab/sentinelAgent.git
cd sentinelAgent
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Uso básico

Ejecutar un ciclo único de monitoreo:
```bash
python sentinel_agent.py
```

### Modo continuo

Ejecutar monitoreo continuo:
```bash
python sentinel_agent.py --continuous
```

### Con configuración personalizada

Usar archivo de configuración JSON:
```bash
python sentinel_agent.py --config config.example.json --continuous
```

Usar archivo de configuración YAML:
```bash
python sentinel_agent.py --config config.example.yaml --continuous
```

### Monitorear endpoint específico

```bash
python sentinel_agent.py --endpoint http://localhost:8080/health
```

## Configuración

### Archivo de configuración

Puedes crear un archivo de configuración en formato JSON o YAML. Ejemplo JSON:

```json
{
  "monitoring_interval": 60,
  "alert_thresholds": {
    "cpu_percent": 80.0,
    "memory_percent": 85.0,
    "disk_percent": 90.0,
    "response_time_ms": 1000.0
  },
  "pos_endpoint": "http://localhost:8080/health",
  "log_level": "INFO",
  "metrics_retention": 1000
}
```

### Parámetros de configuración

- `monitoring_interval`: Intervalo entre ciclos de monitoreo (segundos)
- `alert_thresholds`: Umbrales para generar alertas
  - `cpu_percent`: Umbral de uso de CPU (%)
  - `memory_percent`: Umbral de uso de memoria (%)
  - `disk_percent`: Umbral de uso de disco (%)
  - `response_time_ms`: Umbral de tiempo de respuesta (ms)
- `pos_endpoint`: URL del endpoint del POS a monitorear
- `log_level`: Nivel de logging (DEBUG, INFO, WARNING, ERROR)
- `metrics_retention`: Número máximo de métricas a retener en memoria

## Métricas monitoreadas

### Métricas del sistema
- Porcentaje de uso de CPU
- Porcentaje de uso de memoria
- Porcentaje de uso de disco
- Memoria disponible (MB)
- Espacio libre en disco (GB)

### Métricas del POS
- Estado del servicio (healthy/unhealthy)
- Código de estado HTTP
- Tiempo de respuesta (ms)

## Alertas

El sistema genera alertas cuando las métricas exceden los umbrales configurados. Las alertas se registran en:
- Archivo de log (`sentinel_agent.log`)
- Salida de consola
- Historial de métricas con estado "alert"

## Logs

Los logs se guardan en `sentinel_agent.log` y también se muestran en consola. Formato de log:
```
2026-02-13 10:30:45,123 - SentinelAgent - INFO - Health Status: healthy
```

## Ejemplos de uso

### Ejemplo 1: Monitoreo simple
```bash
python sentinel_agent.py
```

### Ejemplo 2: Monitoreo continuo con configuración
```bash
python sentinel_agent.py --config config.json --continuous
```

### Ejemplo 3: Monitoreo de endpoint específico
```bash
python sentinel_agent.py --endpoint https://mi-pos.ejemplo.com/api/health --continuous
```

## Uso como módulo

También puedes usar SentinelAgent como módulo en tu código Python:

```python
from sentinel_agent import SentinelAgent

# Crear instancia del agente
agent = SentinelAgent(config_path='config.json')

# Ejecutar un ciclo de monitoreo
result = agent.run_monitoring_cycle()
print(result)

# Obtener estado de salud
health = agent.get_health_status()
print(f"Estado: {health.status}")

# Registrar métrica personalizada
agent.record_metric('transactions_per_minute', 150, 'tpm')

# Obtener resumen de métricas
summary = agent.get_metrics_summary()
print(summary)
```

## Estructura del proyecto

```
sentinelAgent/
├── sentinel_agent.py        # Código principal del agente
├── requirements.txt         # Dependencias de Python
├── config.example.json      # Ejemplo de configuración JSON
├── config.example.yaml      # Ejemplo de configuración YAML
├── README.md               # Este archivo
└── sentinel_agent.log      # Archivo de logs (generado al ejecutar)
```

## Solución de problemas

### Error: "No module named 'psutil'"
Instala las dependencias: `pip install -r requirements.txt`

### Error: "No POS endpoint configured"
Proporciona un endpoint usando `--endpoint` o en el archivo de configuración

### Los logs no se generan
Verifica que tienes permisos de escritura en el directorio actual

## Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo licencia MIT.

## Contacto

Darwin Mora - [@darwinmorab](https://github.com/darwinmorab)

Proyecto: [https://github.com/darwinmorab/sentinelAgent](https://github.com/darwinmorab/sentinelAgent)
