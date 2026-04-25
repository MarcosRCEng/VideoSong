# VideoSong

Aplicativo desktop em Python com interface `tkinter` para baixar videos localmente com `yt-dlp`, escolhendo entre video completo em `.mp4` ou somente audio em `.mp3`.

## Objetivo

Manter um app pequeno, local e facil de evoluir para:

- escolher o formato uma vez por execucao
- selecionar ou reaproveitar a pasta de destino
- montar uma fila com uma ou varias URLs
- acompanhar progresso em tempo real
- diagnosticar erros locais sem expor detalhes tecnicos na interface

## Estado Atual

O fluxo atual usa um wizard em etapas:

1. escolher `Video completo` ou `Somente audio`
2. confirmar a pasta de destino
3. adicionar URLs manualmente ou colar varias linhas em lote
4. revisar a fila e iniciar o download

Durante a execucao, o app:

- processa a fila em ordem, uma URL por vez
- mantem a interface responsiva usando uma thread de download
- mostra status, progresso global e progresso por item
- exibe tempo decorrido, velocidade e ETA quando o `yt-dlp` fornece esses dados
- continua a fila mesmo se um item falhar
- permite solicitar cancelamento da fila em andamento
- permite abrir a pasta de destino ao final
- permite limpar da tela os itens concluidos, mantendo itens com erro

As ultimas preferencias de formato e pasta sao salvas localmente para reduzir repeticao entre usos.

## Estrutura

```text
VideoSong/
|-- docs/
|   |-- AGENTS.md
|   |-- TASKS.md
|   `-- VIBE_PLAN.md
|-- scripts/
|   |-- build_installer.cmd
|   |-- build_installer.ps1
|   |-- build_windows.ps1
|   |-- setup_windows.ps1
|   `-- VideoSongInstaller.iss
|-- src/
|   `-- videosong/
|       |-- services/
|       |   |-- download_queue.py
|       |   |-- download_service.py
|       |   |-- error_log.py
|       |   `-- settings_service.py
|       |-- ui/
|       |   |-- main_window.py
|       |   |-- url_batch_parser.py
|       |   |-- url_list_manager.py
|       |   |-- wizard_messages.py
|       |   |-- wizard_review.py
|       |   |-- wizard_state.py
|       |   `-- wizard_steps.py
|       `-- app.py
|-- tests/
|-- main.py
|-- requirements.txt
|-- requirements-dev.txt
|-- VideoSong.spec
`-- README.md
```

## Ambiente Local

Criar e ativar o ambiente virtual no PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instalar dependencias Python:

```powershell
python -m pip install -r requirements.txt
```

`requirements.txt` instala apenas dependencias Python. Runtimes de sistema como `Node.js`, `ffmpeg` e `ffprobe` precisam ser instalados separadamente.

## Pre-Requisitos de Sistema

Para uso local completo e para gerar o pacote Windows, o projeto depende destes binarios externos:

- `Node.js` LTS 20+: necessario para URLs do YouTube
- `ffmpeg` e `ffprobe`: necessarios para merge final de `.mp4` e extracao final de `.mp3`

Setup automatico recomendado no Windows:

```powershell
.\scripts\setup_windows.ps1
```

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

## Como Executar

```powershell
python main.py
```

## Como Usar

1. Abra o aplicativo com `python main.py`.
2. No passo de formato, escolha `Video completo` ou `Somente audio`.
3. No passo de destino, confirme a pasta sugerida ou clique em `Escolher pasta`.
4. No passo de URLs, adicione uma URL por vez ou cole varias URLs, uma por linha.
5. Na revisao, confira a fila e clique em `Iniciar download`.
6. Acompanhe o progresso global e por item.
7. Ao final, use `Abrir pasta` para acessar os arquivos baixados ou `Limpar concluidos` para remover itens concluidos da tela.

## Comportamento do Download

- modo `video`: salva o arquivo final em `.mp4`
- modo `audio`: extrai e salva o arquivo final em `.mp3`
- pasta de destino: e criada automaticamente se ainda nao existir
- playlists: sao ignoradas para manter o fluxo previsivel
- fila: cada URL e processada sequencialmente
- falhas: itens com erro recebem mensagem amigavel e a fila segue para o proximo item
- cancelamento: o app solicita cancelamento da fila; o item atual encerra com seguranca e os proximos nao sao iniciados
- pacote Windows: `ffmpeg` e `ffprobe` sao incluidos no executavel quando encontrados durante o build

## Logs Locais

Erros relevantes sao registrados em arquivo local para diagnostico:

- execucao pelo codigo-fonte: `logs\videosong-errors.log`
- execucao pelo `.exe`: `logs\videosong-errors.log` ao lado do executavel gerado

## Validacao Rapida

Executar todos os testes locais:

```powershell
python -m pytest -q
```

Validar dependencias de sistema no Windows:

```powershell
.\scripts\setup_windows.ps1
```

## Empacotamento Windows

Instalar dependencias de desenvolvimento:

```powershell
python -m pip install -r requirements-dev.txt
```

Gerar o executavel localmente:

```powershell
.\scripts\build_windows.ps1 -ReleaseLabel sprint-7
```

Gerar o instalador Windows a partir do executavel empacotado:

```powershell
.\scripts\build_installer.ps1 -ReleaseLabel sprint-7
```

Ou sem PowerShell:

```bat
scripts\build_installer.cmd sprint-7
```

Saida esperada:

- `dist\VideoSong.exe`
- `dist\releases\VideoSong-sprint-7.exe`
- `dist\releases\VideoSong-sprint-7-setup.exe`

Observacoes:

- o build exige `Node.js`, `ffmpeg` e `ffprobe` utilizaveis na maquina de empacotamento
- o script de build usa uma pasta temporaria isolada e publica o resultado final em `dist\`
- o instalador Windows usa Inno Setup 6 e cria atalhos basicos
- durante a instalacao, o setup oferece instalar `Node.js` LTS via `winget` quando ele ainda nao estiver disponivel
- use um `ReleaseLabel` por sprint fechada, como `sprint-7`, para manter artefatos versionados

## Fluxo de Trabalho

O projeto usa dois arquivos curtos para reduzir contexto e manter execucao objetiva:

- `docs/VIBE_PLAN.md` define a visao, fases e decisoes do projeto
- `docs/TASKS.md` lista tarefas acionaveis e status real de cada entrega

Toda entrega deve:

1. usar uma branch propria da tarefa
2. implementar a menor fatia funcional possivel
3. validar localmente
4. atualizar `docs/TASKS.md`
5. ficar pronta para commit, sem commitar sem autorizacao

## Dependencias

- `yt-dlp`: base para downloads de video e audio
- `pytest`: testes rapidos do projeto
- `pyinstaller`: empacotamento Windows
- `Node.js` LTS 20+: runtime JavaScript exigido pelo `yt-dlp` para URLs do YouTube
- `ffmpeg` e `ffprobe`: binarios necessarios para merge de video e extracao de audio
