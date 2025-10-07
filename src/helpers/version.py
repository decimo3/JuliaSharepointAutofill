''' Module to hold version class data model '''
class Version:
    ''' Class to hold informations about version '''
    major: int
    minor: int
    patch: int
    extra: int
    def __init__(self, *args: str | int) -> None:
        # Accepts either (self, major, minor, patch, extra) or (self, 'major.minor.patch.extra')
        if len(args) > 1 and all(isinstance(x, int) for x in args):
            # args[1], args[2], args[3] should be int or str convertible to int
            try:
                self.major = int(args[0])
                self.minor = int(args[1])
                self.patch = int(args[2]) if len(args) > 2 else 0
                self.extra = int(args[3]) if len(args) > 3 else 0
            except (ValueError, TypeError) as e:
                raise ValueError('Version arguments must be integers') from e
        elif len(args) == 1 and isinstance(args[0], str):
            # Accepts string like 'major.minor.patch.extra'
            argv = args[0].split('.')
            try:
                self.major = int(argv[0])
                self.minor = int(argv[1])
                self.patch = int(argv[2]) if len(argv) > 2 else 0
                self.extra = int(argv[3]) if len(argv) > 3 else 0
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
            self.patch == value.patch and
            self.extra == value.extra
        )
    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Version):
            raise ValueError('O objeto comparado não é do mesmo tipo!')
        if self.major != other.major:
            return self.major > other.major
        if self.minor != other.minor:
            return self.minor > other.minor
        if self.patch != other.patch:
            return self.patch > other.patch
        return self.extra > other.extra
    def __str__(self) -> str:
        return str(self.major) + '.' + str(self.minor) + '.' + str(self.patch) + '.' + str(self.extra)
