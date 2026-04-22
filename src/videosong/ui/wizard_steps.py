from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WizardStep:
    index: int
    key: str
    title: str
    description: str


WIZARD_STEPS: tuple[WizardStep, ...] = (
    WizardStep(
        index=0,
        key="format",
        title="Passo 1 - Formato",
        description="Escolha entre video completo ou somente audio.",
    ),
    WizardStep(
        index=1,
        key="destination",
        title="Passo 2 - Pasta de destino",
        description="Selecione a pasta em que o arquivo sera salvo.",
    ),
    WizardStep(
        index=2,
        key="urls",
        title="Passo 3 - Lista de URLs",
        description="Adicione uma URL por vez para montar a lista desta execucao.",
    ),
    WizardStep(
        index=3,
        key="review",
        title="Passo 4 - Revisao",
        description="Revise a configuracao antes de iniciar o download.",
    ),
)
