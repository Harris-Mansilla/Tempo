from pathlib import Path
import base64
root=Path(__file__).resolve().parent
html=(root/'index.html').read_text()
html=html.replace('<link rel="stylesheet" href="styles.css">','<style>\n'+(root/'styles.css').read_text()+'\n</style>')
html=html.replace('<script src="data.js"></script>','<script>\n'+(root/'data.js').read_text()+'\n</script>')
html=html.replace('<script src="app.js"></script>','<script>\n'+(root/'app.js').read_text()+'\n</script>')
icon=base64.b64encode((root/'icon.svg').read_bytes()).decode()
html=html.replace('href="icon.svg"','href="data:image/svg+xml;base64,'+icon+'"')
# Portable build must not fetch companion files, even if hosted as a single file.
html=html.replace("if(location.protocol==='http:'||location.protocol==='https:'){", "if(false){")
(root.parent/'Stride.html').write_text(html)
print('Built',len(html),'characters')
