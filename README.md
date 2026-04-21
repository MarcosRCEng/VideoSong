# VideoSong

Aplicativo desktop em Python com interface simples em `tkinter` para baixar videos da internet e, opcionalmente, salvar apenas o audio.

## Objetivo

Construir um app leve, local e facil de evoluir, com foco em:

- colar uma URL
- escolher video completo ou somente audio
- selecionar pasta de destino
- acompanhar o status do download
- manter o projeto simples o bastante para iterarmos aqui no Codex

## Estrutura Inicial

```text
VideoSong/
|-- docs/
|   |-- TASKS.md
|   `-- VIBE_PLAN.md
|-- src/
|   `-- videosong/
|       |-- ui/
|       |   `-- main_window.py
|       |-- __init__.py
|       `-- app.py
|-- tests/
|   `-- test_imports.py
|-- .gitignore
|-- main.py
|-- requirements.txt
`-- README.md
```

## Ambiente Local

Criar ambiente virtual:

```powershell
python -m venv .venv
```

Ativar no PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```powershell
python -m pip install -r requirements.txt
```

## Como Executar

```powershell
python main.py
```

## Fluxo de Trabalho

O projeto usa dois arquivos curtos para reduzir contexto e manter execucao objetiva:

- `docs/VIBE_PLAN.md` define a visao, fases e decisoes
- `docs/TASKS.md` lista tarefas acionaveis e seu status

Toda entrega deve, idealmente:

1. atualizar a tarefa em andamento
2. implementar a menor fatia funcional possivel
3. testar a mudanca
4. marcar o resultado na tarefa
5. registrar um commit coerente

## Dependencias

- `yt-dlp`: base para downloads de video e audio
- `pytest`: testes rapidos do projeto

## Proximos Passos

- implementar servico de download
- integrar escolha de pasta de destino
- adicionar opcoes de audio e video na interface
- exibir progresso e mensagens de erro amigaveis
