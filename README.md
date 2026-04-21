# VideoSong

Aplicativo desktop em Python com interface simples em `tkinter` para baixar videos da internet e, opcionalmente, salvar apenas o audio.

## Objetivo

Construir um app leve, local e facil de evoluir, com foco em:

- colar uma URL
- escolher video completo ou somente audio
- selecionar pasta de destino
- acompanhar o status do download
- manter o projeto simples o bastante para iterarmos aqui no Codex

## Estado Atual

O fluxo atual do aplicativo ja permite:

- informar uma URL com `http://` ou `https://`
- escolher entre download de `video` ou `audio`
- selecionar a pasta de destino
- iniciar o download local com `yt-dlp`
- acompanhar mensagens simples de validacao, erro e sucesso

## Estrutura

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

Observacao importante: `requirements.txt` instala apenas dependencias Python. Runtimes de sistema como `Node.js`, `ffmpeg` e `ffprobe` nao podem ser embutidos ali.

## Pre-Requisito para YouTube

Para URLs do YouTube, o `yt-dlp` precisa de um runtime JavaScript compativel. Neste projeto, o caminho recomendado no Windows e instalar `Node.js` LTS 20+.

Setup automatico no Windows:

```powershell
.\scripts\setup_windows.ps1
```

Validacao manual depois do setup:

```powershell
node --version
where.exe node
```

Saida esperada: um `node.exe` real, preferencialmente em `C:\Program Files\nodejs\node.exe`, e nao o executavel interno de `WindowsApps`.

## Como Executar

```powershell
python main.py
```

## Como Usar

1. Abra o aplicativo com `python main.py`.
2. Cole a URL completa do video.
3. Escolha `Video completo` ou `Somente audio`.
4. Clique em `Escolher pasta` e selecione o destino do arquivo.
5. Clique em `Iniciar download`.

## Comportamento Atual do Download

- modo `video`: salva o arquivo final em `.mp4`
- modo `audio`: extrai e salva o arquivo final em `.mp3`
- pasta de destino: e criada automaticamente se ainda nao existir
- playlists: sao ignoradas nesta fatia inicial para manter o fluxo simples
- observacao: a conversao para `.mp3` depende do `ffmpeg` estar disponivel no ambiente

## Validacao Rapida

Executar os testes locais:

```powershell
python -m pytest -q
```

Validar o setup do runtime JavaScript no Windows sem abrir a interface:

```powershell
.\scripts\setup_windows.ps1
```

## Empacotamento Windows

Instalar as dependencias de desenvolvimento:

```powershell
python -m pip install -r requirements-dev.txt
```

Gerar o executavel localmente:

```powershell
.\scripts\build_windows.ps1
```

Saida esperada: `dist\VideoSong.exe`

Observacao: o script limpa `build\` e `dist\` antes de gerar um executavel novo, para evitar residuos de empacotamentos antigos.

Executar o binario gerado:

```powershell
.\dist\VideoSong.exe
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
- `pyinstaller`: base inicial para gerar o executavel Windows
- `Node.js` LTS 20+: runtime JavaScript exigido pelo `yt-dlp` para URLs do YouTube
