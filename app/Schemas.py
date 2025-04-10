# app/routers/schemas.py
from typing import Type, Optional, Dict, Any
from pydantic import BaseModel, create_model
from dataclasses import fields as dataclass_fields
from app.models.AbstractModel import AbstractModel

def gerar_schema_entrada(model_cls: Type[AbstractModel]) -> Type[BaseModel]:
    campos: Dict[str, Any] = {}
    
    for campo in dataclass_fields(model_cls):
        if campo.name == "id":
            continue
        campos[campo.name] = (campo.type, ...)
    
    return create_model(f"{model_cls.__name__}Entrada", **campos)

def gerar_schema_saida(model_cls: Type[AbstractModel]) -> Type[BaseModel]:
    campos: Dict[str, Any] = {}
    
    for campo in dataclass_fields(model_cls):
        if campo.name == "id":
            continue
        campos[campo.name] = (campo.type, ...)
    campos["id"] = (int, ...)
    
    return create_model(f"{model_cls.__name__}Saida", **campos)

def gerar_schema_atualizar(model_cls: Type[AbstractModel]) -> Type[BaseModel]:
    campos: Dict[str, Any] = {}
    
    for campo in dataclass_fields(model_cls):
        if campo.name == "id":
            continue
        campos[campo.name] = (Optional[campo.type], None)
        
    return create_model(f"{model_cls.__name__}Atualizar", **campos)
