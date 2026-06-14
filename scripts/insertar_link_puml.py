"""Inserta `[Código PlantUML](...)` justo debajo del `</div>` que cierra el
bloque de diagrama de colaboración en cada README de análisis. Idempotente:
si ya hay un enlace al .puml inmediatamente después del </div>, no duplica.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/Users/sauldecos/git/ids/25-26-idsw2-sdVC")
ANALISIS = ROOT / "RUP" / "01-analisis" / "casos-uso"


def main() -> None:
    cambiados = 0
    for cu_dir in sorted(p for p in ANALISIS.iterdir() if p.is_dir()):
        readme = cu_dir / "README.md"
        if not readme.exists():
            continue
        cu = cu_dir.name
        link = f"[Código PlantUML](/modelosUML/RUP/01-analisis/casos-uso/{cu}/colaboracion.puml)"
        original = readme.read_text(encoding="utf-8")

        # Localiza el bloque del diagrama de colaboración: imagen seguida de </div>.
        # El patrón canónico es:
        #   |![...](.../colaboracion.svg)|
        #   |-|
        #   |...|
        #   <linea en blanco>
        #   </div>
        # Buscamos el primer `</div>` que vaya después de la primera referencia
        # a colaboracion.svg y que aún no esté seguido del enlace.
        svg_match = re.search(r"colaboracion\.svg", original)
        if not svg_match:
            continue
        div_match = re.search(r"</div>\s*", original[svg_match.end():])
        if not div_match:
            continue
        insert_pos = svg_match.end() + div_match.end()

        # Idempotencia: si el enlace ya aparece en los siguientes ~200 chars, no insertar.
        ventana = original[insert_pos: insert_pos + 200]
        if "colaboracion.puml" in ventana:
            continue

        nuevo = original[:insert_pos] + f"\n{link}\n" + original[insert_pos:]
        readme.write_text(nuevo, encoding="utf-8")
        cambiados += 1
        print(f"insertado en: {readme.relative_to(ROOT)}")
    print(f"\nTotal READMEs actualizados: {cambiados}")


if __name__ == "__main__":
    main()
