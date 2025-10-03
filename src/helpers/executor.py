''' Module to wrap calls to external programs '''
import subprocess

def execute(*args: str) -> str:
    ''' Function to execute and return code and stdout '''
    if not args:
        raise ValueError('Não foram passados argumentos para a função!')
    command = ' '.join(args)
    try:
        result = subprocess.run(
            args=command,
            capture_output=True,
            text=True,
            shell=False,
            check=True
            )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(e.stderr or f'O programa {args[0]} retornou com erro desconhecido!')
        return ''
    except FileNotFoundError as e:
        print(e.strerror or f'O sistema não pode encontrar o programa {args[0]}!')
        return ''
