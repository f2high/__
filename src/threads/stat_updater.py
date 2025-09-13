from time import time, sleep
from colorama import Fore, Style
from datetime import datetime


def cpm(content: str):
    print(
        f'{Fore.LIGHTBLACK_EX}{datetime.fromtimestamp(time()).strftime(f"[{Fore.LIGHTBLUE_EX}%H{Fore.LIGHTBLACK_EX}:{Fore.LIGHTBLUE_EX}%M{Fore.LIGHTBLACK_EX}:{Fore.LIGHTBLUE_EX}%S{Fore.LIGHTBLACK_EX}]")}{Fore.RESET} '
        + content.replace("->", f"{Fore.LIGHTBLACK_EX}->{Fore.LIGHTBLUE_EX}")
        .replace(
            "(+)",
            f"{Fore.LIGHTBLACK_EX}({Fore.GREEN}+{Fore.LIGHTBLACK_EX}){Fore.LIGHTGREEN_EX}",
        )
        .replace(
            "($)",
            f"{Fore.LIGHTBLACK_EX}({Fore.GREEN}${Fore.LIGHTBLACK_EX}){Fore.GREEN}",
        )
        .replace(
            "(-)",
            f"{Fore.LIGHTBLACK_EX}({Fore.RED}-{Fore.LIGHTBLACK_EX}){Fore.LIGHTRED_EX}",
        )
        .replace(
            "(!)",
            f"{Fore.LIGHTBLACK_EX}({Fore.RED}!{Fore.LIGHTBLACK_EX}){Fore.LIGHTBLUE_EX}",
        )
        .replace(
            "(~)",
            f"{Fore.LIGHTBLACK_EX}({Fore.YELLOW}~{Fore.LIGHTBLACK_EX}){Fore.YELLOW}",
        )
        .replace(
            "(/)",
            f"{Fore.LIGHTBLACK_EX}({Fore.YELLOW}/{Fore.LIGHTBLACK_EX}){Fore.YELLOW}",
        )
        .replace(
            "(#)",
            f"{Fore.LIGHTBLACK_EX}({Fore.BLUE}#{Fore.LIGHTBLACK_EX}){Fore.LIGHTBLUE_EX}",
        )
        .replace(
            "(*)",
            f"{Fore.LIGHTBLACK_EX}({Fore.CYAN}*{Fore.LIGHTBLACK_EX}){Fore.LIGHTBLUE_EX}",
        )
        .replace(
            "[+]",
            f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTGREEN_EX}+{Fore.LIGHTBLACK_EX}]{Fore.LIGHTGREEN_EX}",
        )
        .replace(
            "[-]",
            f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTRED_EX}-{Fore.LIGHTBLACK_EX}]{Fore.LIGHTRED_EX}",
        )
        .replace(
            "[>]",
            f"{Fore.LIGHTBLACK_EX}[{Fore.LIGHTBLUE_EX}>{Fore.LIGHTBLACK_EX}]{Fore.LIGHTBLUE_EX}",
        )
        .replace(
            "(>)",
            f"{Fore.LIGHTBLACK_EX}({Fore.LIGHTBLUE_EX}>{Fore.LIGHTBLACK_EX}){Fore.LIGHTBLUE_EX}",
        ),
        end=f"{Fore.RESET}\r",
    )


def stat_updater(count_queue):
    count_cache = {}

    while True:
        while True:
            try:
                for ts, count in count_queue.get(block=False):
                    ts = int(ts)
                    count_cache[ts] = count_cache.get(ts, 0) + count
            except:
                break

        now = time()
        total_count = 0
        for ts, count in tuple(count_cache.items()):
            if now - ts > 60:
                count_cache.pop(ts)
                continue
            total_count += count

        cpm(f"(+) Checks Per Minute: {total_count:,}")
        sleep(0.10)
