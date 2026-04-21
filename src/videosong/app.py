from src.videosong.services.error_log import write_error_log
from src.videosong.ui.main_window import MainWindow


def run() -> None:
    try:
        window = MainWindow()
        window.run()
    except Exception as error:
        write_error_log("Falha nao tratada ao iniciar ou executar a aplicacao.", error)
        raise
