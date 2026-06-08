"""Fill the deck HTML placeholders with real values from results/demo_data.json."""
import json, pathlib

d = json.load(open("results/demo_data.json"))
html = pathlib.Path("deck/slides.html").read_text()

r = d["ranked"]
for i in range(5):
    x = r[i] if i < len(r) else {"thickness": 0, "porosity": 0, "specific_energy": 0, "rate": 0}
    html = html.replace(f"RT{i+1}", str(round(x["thickness"])))
    html = html.replace(f"RP{i+1}", f"{round(x['porosity']*100)}%")
    html = html.replace(f"RE{i+1}", str(round(x["specific_energy"])))
    html = html.replace(f"RR{i+1}", f"{x['rate']:.2f}")

b, pw = d["best"], d["power"]["best"]
html = html.replace('id="g-drone">26%<', f'id="g-drone">{round(b["porosity"]*100)}%<')
html = html.replace('id="g-drone-e">270<', f'id="g-drone-e">{round(b["specific_energy"])}<')
html = html.replace('id="g-power">42%<', f'id="g-power">{round(pw["porosity"]*100)}%<')
html = html.replace('id="g-power-e">249<', f'id="g-power-e">{round(pw["specific_energy"])}<')

pathlib.Path("deck/slides_filled.html").write_text(html)
print("filled deck/slides_filled.html")
