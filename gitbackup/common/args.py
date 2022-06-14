import argparse


class Args:
    def __init__(self) -> None:
        self.args = argparse.ArgumentParser(
            usage="%(prog)s [OPTION] [FILE]...",
            description="Backup remote Git repos to a backup location."
        )
        self.args.add_argument(
            "--config",
            default="/data/config.ini",
            help="Path to config file, default: /data/config.ini"
        )
        self.args.add_argument(
            "--backup-all",
            action='store_true',
            help="Backup all repos, regardless of previous backup state."
        )
        self.args.add_argument(
            "-v", "--version", action="version",
            version=f"{self.args.prog} version 1.0.0"
        )
        self.values = self.args.parse_args()

    @property
    def config_file(self):
        return self.values.config
