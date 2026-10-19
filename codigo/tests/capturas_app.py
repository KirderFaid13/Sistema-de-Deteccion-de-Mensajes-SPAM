"""Ejecuta un recorrido real por la aplicación en ejecución y guarda capturas de pantalla.
Requiere la app corriendo en http://127.0.0.1:5000 y Playwright con Chromium.
Las entradas son mensajes de demostración escritos para la prueba (no provienen del corpus)."""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parents[1] / "results" / "capturas"
OUT.mkdir(parents=True, exist_ok=True)
URL = "http://127.0.0.1:5000"
SPAM = "Congratulations! You have won a 500 GBP voucher. Text CLAIM to 80086 now to collect your prize"
DUDOSO = "You have been selected for a special offer, reply to this number"
HAM = "Are we still meeting for lunch tomorrow at 1pm?"

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1000, "height": 640}, device_scale_factor=2)
    pg.goto(URL); pg.fill("textarea[name=texto]", SPAM)
    pg.screenshot(path=str(OUT / "cap1_formulario.png"), full_page=True)
    pg.click("button[type=submit]"); pg.wait_for_load_state()
    pg.screenshot(path=str(OUT / "cap2_resultado_spam.png"), full_page=True)
    pg.goto(URL); pg.fill("textarea[name=texto]", HAM); pg.click("button[type=submit]"); pg.wait_for_load_state()
    pg.screenshot(path=str(OUT / "cap3_resultado_legitimo.png"), full_page=True)
    pg.goto(URL); pg.fill("textarea[name=texto]", DUDOSO); pg.click("button[type=submit]"); pg.wait_for_load_state()
    pg.screenshot(path=str(OUT / "cap4_resultado_pendiente.png"), full_page=True)
    pg.goto(URL + "/pendientes")
    pg.screenshot(path=str(OUT / "cap5_bandeja_pendientes.png"), full_page=True)
    pg.fill("input[name=revisor]", "Revisor demo")
    pg.fill("input[name=comentario]", "Oferta no solicitada que pide responder")
    pg.click("button[name=etiqueta][value='1']"); pg.wait_for_load_state()
    pg.screenshot(path=str(OUT / "cap6_revisiones.png"), full_page=True)
    b.close()
print("capturas en", OUT)
