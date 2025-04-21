from datetime import datetime

def debug(msg: str, entidade: str = "", extra: dict = None):
    """Imprime mensagem de debug padronizada."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entidade_str = f"[{entidade}]" if entidade else ""
    extra_str = f" | {extra}" if extra else ""
    print(f"[DEBUG]{entidade_str} {now} - {msg}{extra_str}")

def erro(msg: str, entidade: str = "", extra: dict = None):
    """Imprime mensagem de erro padronizada."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entidade_str = f"[{entidade}]" if entidade else ""
    extra_str = f" | {extra}" if extra else ""
    print(f"[ERRO]{entidade_str} {now} - {msg}{extra_str}")