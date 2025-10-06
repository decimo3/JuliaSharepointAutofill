''' Module to hold version class data model '''
class Version:
    ''' Class to hold informations about version '''
    major: int
    minor: int
    patch: int
    def __init__(self, *args: str | int) -> None:
        # Accepts either (self, major, minor, patch) or (self, 'major.minor.patch')
        if len(args) == 4:
            # args[1], args[2], args[3] should be int or str convertible to int
            try:
                self.major = int(args[1])
                self.minor = int(args[2])
                self.patch = int(args[3])
            except (ValueError, TypeError) as e:
                raise ValueError('Version arguments must be integers') from e
        elif len(args) == 2 and isinstance(args[1], str):
            # Accepts string like 'major.minor.patch'
            argv = args[1].split('.', maxsplit=3)
            if len(argv) < 3:
                raise ValueError('Version string must be in format major.minor.patch')
            try:
                self.major = int(argv[0])
                self.minor = int(argv[1])
                self.patch = int(argv[2])
            except (ValueError, TypeError) as e:
                raise ValueError('Version string must contain only integers') from e
        else:
            raise ValueError('Invalid arguments for Version')
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Version):
            raise ValueError('O objeto comparado não é do mesmo tipo!')
        return (
            self.major == value.major and
            self.minor == value.minor and
            self.patch == value.patch
        )
    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Version):
            raise ValueError('O objeto comparado não é do mesmo tipo!')
        if self.major != other.major:
            return self.major > other.major
        if self.minor != other.minor:
            return self.minor > other.minor
        return self.patch > other.patch
    def __str__(self) -> str:
        return str(self.major) + '.' + str(self.minor) + '.' + str(self.patch)
