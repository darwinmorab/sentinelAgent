# Quick Start Guide - SentinelAgent

## Instalación rápida (5 minutos)

### 1. Clonar e instalar
```bash
git clone https://github.com/darwinmorab/sentinelAgent.git
cd sentinelAgent
pip install -r requirements.txt
```

### 2. Ejecutar el agente
```bash
# Monitoreo simple (una vez)
python sentinel_agent.py

# Monitoreo continuo
python sentinel_agent.py --continuous
```

### 3. Monitorear tu sistema POS
```bash
# Monitorear un endpoint específico
python sentinel_agent.py --endpoint http://tu-pos.ejemplo.com/health --continuous
```

### 4. Usar configuración personalizada
```bash
# Copiar ejemplo de configuración
cp config.example.json mi-config.json

# Editar configuración
nano mi-config.json

# Ejecutar con configuración
python sentinel_agent.py --config mi-config.json --continuous
```

## Ejemplo de salida

```
2026-02-13 10:30:45 - SentinelAgent - INFO - === Starting Monitoring Cycle ===
2026-02-13 10:30:46 - SentinelAgent - INFO - Health Status: healthy
2026-02-13 10:30:46 - SentinelAgent - INFO - Active Alerts: 0
2026-02-13 10:30:46 - SentinelAgent - INFO - === Monitoring Cycle Complete ===
```

## Casos de uso comunes

### Monitoreo de servidor POS local
```bash
python sentinel_agent.py --endpoint http://localhost:8080/health --continuous
```

### Monitoreo con alertas personalizadas
Edita `config.json`:
```json
{
  "alert_thresholds": {
    "cpu_percent": 70.0,
    "memory_percent": 80.0,
    "disk_percent": 85.0
  }
}
```

### Integración con scripts
```python
from sentinel_agent import SentinelAgent

agent = SentinelAgent()
health = agent.get_health_status()

if health.status != 'healthy':
    # Enviar alerta
    print(f"⚠️ Sistema en estado: {health.status}")
```

## Métricas monitoreadas por defecto

- **CPU**: Porcentaje de uso
- **Memoria**: Porcentaje de uso y MB disponibles
- **Disco**: Porcentaje de uso y GB libres
- **Uptime**: Tiempo de ejecución del agente
- **POS Health**: Estado del endpoint HTTP (si configurado)

## Próximos pasos

1. Ver `examples.py` para más ejemplos de uso
2. Leer `README.md` para documentación completa
3. Personalizar `config.example.json` según tus necesidades
4. Integrar con tu sistema de monitoreo existente

## Soporte

Para problemas o preguntas, abre un issue en:
https://github.com/darwinmorab/sentinelAgent/issues
