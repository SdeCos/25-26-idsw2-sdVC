"""Reescribe en TODOS los .md del repo las rutas absolutas viejas
`/RUP/...svg|puml|png` para que apunten a `/images/RUP/...` o `/modelosUML/RUP/...`.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/Users/sauldecos/git/ids/25-26-idsw2-sdVC")

# Coincide con `/RUP/<...>.<ext>` (URL absoluta desde la raíz del repo)
# precedida por `](`, `src="` o espacio, para no estropear texto narrativo
# (poco probable, pero por si acaso).
PAT = re.compile(
    r'(?P<open>\]\(|src=")(?P<url>/RUP/[^)"\s]+)\.(?P<ext>svg|puml|png)(?P<close>[)"])'
)


def main() -> None:
    cambiados = 0
    for md in ROOT.rglob("*.md"):
        # No tocar nada bajo .git/
        if ".git" in md.parts:
            continue
        original = md.read_text(encoding="utf-8")
        def repl(m: re.Match) -> str:
            ext = m.group("ext")
            asset = "/modelosUML" if ext == "puml" else "/images"
            url = m.group("url")  # empieza por "/RUP/..."
            return f"{m.group('open')}{asset}{url}.{ext}{m.group('close')}"
        nuevo = PAT.sub(repl, original)
        if nuevo != original:
            md.write_text(nuevo, encoding="utf-8")
            cambiados += 1
            print(f"actualizado: {md.relative_to(ROOT)}")
    print(f"\nTotal archivos actualizados: {cambiados}")


if __name__ == "__main__":
    main()
