from dataclasses import dataclass, asdict, fields
from typing import Any


@dataclass
class AbstractModel:
    def _validar_dados(self):
        for campo in fields(self):
            valor = getattr(self, campo.name)

            if not isinstance(valor, campo.type):
                raise TypeError(
                    f"Erro ao criar instância: o campo '{campo.name}' "
                    f"espera um valor do tipo '{campo.type.__name__}', "
                    f"mas recebeu '{type(valor).__name__}'."
                )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def __post_init__(self):
        self._validar_dados()
