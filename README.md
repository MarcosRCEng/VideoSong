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

## Pre-Requisitos de Sistema

Para evitar pendencias no uso local e no pacote Windows, o projeto depende destes binarios externos durante o setup/build:

- `Node.js` LTS 20+: necessario para URLs do YouTube
- `ffmpeg` e `ffprobe`: necessarios para merge final de `.mp4` e extracao final de `.mp3`

Setup automatico no Windows:

```powershell
.\scripts\setup_windows.ps1
```

Ou, para usuarios finais, use o instalador Windows gerado em `dist\releases\VideoSong-<release>-setup.exe`.

Validacao manual depois do setup:

```powershell
node --version
ffmpeg -version
ffprobe -version
where.exe node
where.exe ffmpeg
where.exe ffprobe
```

Saida esperada: binarios reais e utilizaveis, preferencialmente fora de `WindowsApps`.

## Pre-Requisito para YouTube

Para URLs do YouTube, o `yt-dlp` precisa de um runtime JavaScript compativel. Neste projeto, o caminho recomendado no Windows e instalar `Node.js` LTS 20+.

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
- observacao: em execucao local o app procura `ffmpeg` e `ffprobe` no ambiente; no pacote Windows gerado por `.\scripts\build_windows.ps1`, ambos sao incluidos dentro do executavel gerado em `dist\`

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
.\scripts\build_windows.ps1 -ReleaseLabel sprint-2
```

Gerar o instalador Windows a partir do executavel ja empacotado:

```powershell
.\scripts\build_installer.ps1 -ReleaseLabel sprint-2
```

Ou sem PowerShell:

```bat
scripts\build_installer.cmd sprint-2
```

Saida esperada:

- `dist\VideoSong.exe`
- `dist\releases\VideoSong-sprint-2.exe`
- `dist\releases\VideoSong-sprint-2-setup.exe`

Observacoes:

- o script usa uma pasta temporaria isolada do Windows para o PyInstaller e depois publica o resultado final em `dist\`, evitando residuos travados de builds anteriores
- o build exige `Node.js`, `ffmpeg` e `ffprobe` utilizaveis na maquina de empacotamento
- quando presentes, `ffmpeg` e `ffprobe` sao embutidos no pacote final para evitar dependencia extra na maquina de destino
- o instalador Windows usa Inno Setup 6 e copia o `VideoSong.exe` para `Program Files\VideoSong`, criando atalhos basicos
- durante a instalacao, o setup oferece instalar `Node.js` LTS via `winget` quando ele ainda nao estiver disponivel na maquina
- use um `ReleaseLabel` por sprint fechada, como `sprint-2`, para manter um executavel versionado por marco do projeto

## Logs Locais

Erros relevantes do app passam a ser registrados em arquivo local para diagnostico simples:

- execucao pelo codigo-fonte: `logs\videosong-errors.log`
- execucao pelo `.exe`: `logs\videosong-errors.log` ao lado do executavel gerado

Executar o binario gerado:

```powershell
.\dist\VideoSong.exe
```

Executar o instalador gerado:

```powershell
.\dist\releases\VideoSong-sprint-2-setup.exe
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
- `ffmpeg` e `ffprobe`: binarios necessarios para merge de video e extracao de audio
