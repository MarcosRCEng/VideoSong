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
        key="url",
        title="Passo 1 - URL do video",
        description="Cole uma URL completa para preparar o fluxo do download.",
    ),
    WizardStep(
        index=1,
        key="format",
        title="Passo 2 - Formato",
        description="Escolha entre video completo ou somente audio.",
    ),
    WizardStep(
        index=2,
        key="destination",
        title="Passo 3 - Pasta de destino",
        description="Selecione a pasta em que o arquivo sera salvo.",
    ),
    WizardStep(
        index=3,
        key="review",
        title="Passo 4 - Revisao",
        description="Revise a configuracao antes de iniciar o download.",
    ),
)
