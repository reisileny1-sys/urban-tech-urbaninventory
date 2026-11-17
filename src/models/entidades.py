from dataclasses import dataclass, field


@dataclass
class Jurisdicao:
    nome: str


@dataclass
class Local:
    id: str
    endereco: str
    jurisdicao: str


@dataclass
class Ativo:
    id: str
    tipo: str
    jurisdicao: str | None = None
    manutencao_pendente: bool = False
    local: str | None = None


@dataclass
class Orgao:
    id: str
    nome: str
    ativos: set[str] = field(default_factory=set)


@dataclass
class Papel:
    nome: str
    permissoes: set[str] = field(default_factory=set)


@dataclass
class Usuario:
    id: str
    nome: str
    orgao: str | None = None
    papeis: set[str] = field(default_factory=set)
    jurisdicao: str | None = None
