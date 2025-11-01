import importlib
import pkgutil
from pathlib import Path
import streamlit as st

def render():
    st.subheader("🧑‍🎓 Project Team")
    st.caption("Each student renders their own Streamlit component from `students/`.")

    students_pkg = "students"
    pkg_path = str(Path(__file__).resolve().parents[2] / students_pkg)
    modules = []
    for m in pkgutil.iter_modules([pkg_path]):
        if m.name.startswith("_") or m.name == "template_student":
            continue
        modules.append(m.name)

    cols = st.columns(2)
    for i, mod_name in enumerate(sorted(modules)):
        try:
            mod = importlib.import_module(f"{students_pkg}.{mod_name}")
            with cols[i % 2]:
                st.container(border=True)
                mod.render()  # type: ignore[attr-defined]
        except Exception as e:
            st.error(f"Failed to load {mod_name}: {e}")
