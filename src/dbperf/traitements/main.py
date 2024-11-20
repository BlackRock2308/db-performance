# -*- coding: UTF-8 -*-
"""main projet data traitement en pyspark

usage: python3 -m data_traitement [string]"""
from src.dbperf.utils.spark_session import spark  # isort:skip*
import argparse
from typing import Any
from src.dbperf.utils.logger import logger



from src.dbperf.traitements.transformations.data_processor import process_data  # isort:skip





def _wrapper() -> Any:
    """Wrapper interne de la fonction main pour l'initialisation du logging et la récupération
    des arguments

    Returns:
        Any: Le retour de la fonction main
    """

    # parsing des arguments

    logger.info("Récupération des arguments passés au main")

    parser = argparse.ArgumentParser(
        usage="python3 -m main [-h] script option",
    )
    parser.add_argument(
        "--traitement",
        "-t",
        type=str,
        action="store",
        metavar="traitement",
        help="traitement à executer",
    )

    args = parser.parse_args()

    # appelle de la fonction main
    return main(args)


def main(args: argparse.Namespace) -> int:
    """La fonction main du programme, qui implémente la logique applicative.

    Args:
        args (argparse.Namespace): Les arguments passés au programme

    Returns:
        int: Le code de retour de l'application (accessible via $? dans le shell)
    """

    try:
        # Execution du script
        execution_script(args.traitement)

        logger.info("Fin du traitement")

        # code de retour du programme, peut être exploité dans bash (utilisez echo $? pour le print)
        return 0

    except Exception as exception:
        # la gestion d'erreur peut être plus poussée avec des exceptions custom
        logger.error(
            f"Une erreur est survenue dans l'exécution du programe: {type(exception).__name__}: {exception}"
        )
        raise

    finally:
        # mettre ici toute opération de cleanup nécessaire

        logger.info("Fin du programme")

        spark.stop()


def execution_script(nom_traitement: str) -> None:
    """Execute le script demandé via l'appel de la fonction présente dans l'objet globals

    Args:
        - nom_traitement : nom du script
        - kwarg : option donnée au script
    """

    # QUESTION blinder le fait qu'on ne peut executer qu'une liste précise de script ?

    logger.info(f"Lancement du traitement : {nom_traitement}")

    if nom_traitement in globals().keys():
        globals()[nom_traitement]()
    else:
        raise Exception(f"{nom_traitement} n'existe pas")


if __name__ == "__main__":
    _wrapper()