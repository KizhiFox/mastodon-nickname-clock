import sys
import requests
from datetime import datetime, timedelta
from time import sleep


class Clocks:
    clock0 = '🕛'
    clock0_30 = '🕧'
    clock1 = '🕐'
    clock1_30 = '🕜'
    clock2 = '🕑'
    clock2_30 = '🕝'
    clock3 = '🕒'
    clock3_30 = '🕞'
    clock4 = '🕓'
    clock4_30 = '🕟'
    clock5 = '🕔'
    clock_30 = '🕠'
    clock6 = '🕕'
    clock6_30 = '🕡'
    clock7 = '🕖'
    clock7_30 = '🕢'
    clock8 = '🕗'
    clock8_30 = '🕣'
    clock9 = '🕘'
    clock9_30 = '🕤'
    clock10 = '🕙'
    clock10_30 = '🕥'
    clock11 = '🕚'
    clock11_30 = '🕦'

    def get_clock(self, hour: int, half: bool) -> str:
        if hour < 0 or hour > 12:
            raise ValueError
        if half:
            minutes = '_30'
        else:
            minutes = ''
        return getattr(self, f'clock{hour}{minutes}')


clocks = Clocks()


def set_clock(display_name: str, server_name: str, access_token: str):
    time = datetime.now()
    hour = time.hour if time.hour < 12 else time.hour - 12
    half = True if time.minute >= 30 else False

    clock = clocks.get_clock(hour, half)

    print(f'{clock}  {time.hour}:{time.minute}')

    res = requests.patch(
        f'https://{server_name}/api/v1/accounts/update_credentials',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        },
        json={
            'display_name': f'{display_name} {clock}'
        }
    )
    if res.status_code == 200:
        pass
    else:
        print(res.text)
        sys.exit(-1)


def remove_clock(display_name: str, server_name: str, access_token: str):
    res = requests.patch(
        f'https://{server_name}/api/v1/accounts/update_credentials',
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        },
        json={
            'display_name': f'{display_name}'
        }
    )
    if res.status_code == 200:
        pass
    else:
        print(res.text)
        sys.exit(-1)


def get_display_name(server_name: str, access_token: str):
    res = requests.patch(
        f'https://{server_name}/api/v1/accounts/update_credentials',
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    if res.status_code == 200:
        return res.json()['display_name']
    else:
        print(res.text)
        sys.exit(-1)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        server = sys.argv[1]
        token = sys.argv[2]

        name = get_display_name(server, token)
        print(f'Hello, {name}!')

        set_clock(name, server, token)

        while True:
            try:
                current_time = datetime.now()
                next_time = current_time + timedelta(minutes=30)
                if next_time.minute < 30:
                    next_time = next_time.replace(minute=0)
                else:
                    next_time = next_time.replace(minute=30)

                time_to_sleep = next_time - current_time
                sleep(time_to_sleep.total_seconds())

                set_clock(name, server, token)

            except KeyboardInterrupt:
                remove_clock(name, server, token)
                print('Bye!')
                sys.exit(0)

    else:
        print('format: clock.py <server name (e.g. mastodon.example)> <access token>')
        sys.exit(-1)
