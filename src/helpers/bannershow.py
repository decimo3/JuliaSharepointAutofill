''' Module to write a banner with info of program '''

PRESENTATION_LENGHT = 100

def print_center_presentation(text: str) -> None:
    ''' Function to centralize text on defined lenght '''
    spaces = ((PRESENTATION_LENGHT - len(text)) / 2) - 4
    result = '# '
    result += str(' ' * int(spaces))
    result += text
    result += str(' ' * int(spaces))
    result += ' #'
    print(result)

def print_header_presentation() -> None:
    ''' Function to print startup banner '''
    print()
    print('#' * PRESENTATION_LENGHT)
    print_center_presentation('Programa de autopreenchimento do Sharepoint do MestreRuan')
    print_center_presentation('Repositório: https://github.com/decimo3/JuliaSharepointAutofill')
    print('#' * PRESENTATION_LENGHT)
    print()
