"""Reescribe en los README de RUP/ las rutas de .puml/.svg/.png para apuntar
a /modelosUML/RUP/... y /images/RUP/... (rutas absolutas desde la raíz del repo).

Tras esto, comprueba qué README de análisis no tienen enlace al .puml justo
debajo del diagrama y lo inserta.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/Users/sauldecos/git/ids/25-26-idsw2-sdVC")
RUP = ROOT / "RUP"

# Coincide tanto con `](./foo.svg)`, `](foo.puml)`, como con `src="./foo.svg"`.
# El primer carácter del path debe ser [A-Za-z] (descarta absolutos `/...`,
# URLs `http...`, anclas `#...`).
LINK_RE = re.compile(
    r'(?P<open>\]\(|src=")(?P<dot>\./)?(?P<path>[A-Za-z][^)"\s]*)\.(?P<ext>svg|puml|png)(?P<close>[)"])'
)


def asset_root(ext: str) -> str:
    return "/modelosUML" if ext == "puml" else "/images"


def transform_content(content: str, readme_dir_rel: str) -> str:
    def repl(m: re.Match) -> str:
        ext = m.group("ext")
        path = m.group("path")
        new_url = f"{asset_root(ext)}/{readme_dir_rel}/{path}.{ext}"
        return f"{m.group('open')}{new_url}{m.group('close')}"

    return LINK_RE.sub(repl, content)


def main() -> None:
    cambiados = 0
    # Glob case-insensitive: cubre README.md y README.MD.
    archivos = {p for p in RUP.rglob("*.md")} | {p for p in RUP.rglob("*.MD")}
    for readme in archivos:
        rel_dir = readme.parent.relative_to(ROOT).as_posix()  # p.ej. "RUP/01-analisis/casos-uso/crearAlumno"
        original = readme.read_text(encoding="utf-8")
        nuevo = transform_content(original, rel_dir)
        if nuevo != original:
            readme.write_text(nuevo, encoding="utf-8")
            cambiados += 1
            print(f"actualizado: {readme.relative_to(ROOT)}")
    print(f"\nTotal READMEs actualizados: {cambiados}")


if __name__ == "__main__":
    main()
