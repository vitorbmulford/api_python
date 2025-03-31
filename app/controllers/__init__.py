# Pode estar vazio ou:
from .operadoras_controller import operadoras_bp
from .healthcheck_controller import healthcheck_bp

__all__ = ['operadoras_bp', 'healthcheck_bp']  # Controla o que é exportado