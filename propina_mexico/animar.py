from PIL import Image,ImageDraw,ImageFont,ImageFilter
from pathlib import Path
import math,subprocess,json
P=Path(__file__).resolve().parent;W,H=540,960;FPS=30;D=66
F=P/'fuentes'
CONFIG=json.loads((P/'proyecto.json').read_text(encoding='utf-8'))
HEADLINE=CONFIG['headline']
def font(n):return ImageFont.truetype(str(F/'BarlowCondensed-Bold.ttf'),n)
def mono(n):return ImageFont.truetype(str(F/'IBMPlexMono-Regular.ttf'),n)
BG=(10,17,29);white=(244,241,230);yellow=(255,201,51);blue=(51,124,245);red=(244,62,56)
segments=[(0,3,'Comiste por quinientos pesos…','¿TIENES QUE PAGAR?'),(3,6,'pero la cuenta llega por quinientos setenta y cinco.','75 PESOS EXTRA'),(6,9,'Los setenta y cinco extra dicen: «Propina, quince por ciento».','PROPINA: 15 %'),(9,12,'El cliente pide que la quiten.','A · RETIREN EL CARGO'),(12,16,'El encargado responde: «Aquí se cobra en todas las mesas. El servicio estuvo bien».','B · AQUÍ SE COBRA'),(16,20,'El cliente acepta pagar su consumo, pero se niega a pagar ese extra.','¿QUIÉN TIENE RAZÓN?'),(20,23,'A: el cliente. B: el restaurante. Vota antes de escuchar la respuesta.','ELIGE A O B'),(23,26,'','VOTA AHORA'),(26,29,'En este caso, tiene razón el cliente.','RAZÓN: CLIENTE A'),(29,33,'En México, la propina es voluntaria.','PROPINA VOLUNTARIA'),(33,38,'Profeco señala que no pueden exigirla ni agregarla a la cuenta sin tu consentimiento.','TÚ DECIDES'),(38,42,'Que el servicio haya sido excelente no convierte ese quince por ciento en una obligación.','NO ES OBLIGATORIA'),(42,46,'Puedes pedir que retiren el cargo y pagar lo consumido.','CONSUMO: $500'),(46,51,'Conserva tu comprobante y, si insisten en imponerlo, puedes denunciar ante Profeco.','CONSERVA EL TICKET'),(51,55,'Pero ahora cambia una cosa: el restaurante pregunta primero','CAMBIAMOS UN DATO'),(55,58,'y el cliente acepta agregarla. ¿Eso cambia tu voto?','AHORA SÍ ACEPTÓ'),(58,66,'Y tú, cuando te atienden excelente… ¿dejas propina por agradecimiento o por presión? Te leo.','¿GRATITUD O PRESIÓN?')]
(P/'guion_aprobado.json').write_text(json.dumps({'pais':'México','tipo':'caso ficticio ilustrativo','voz':'pendiente de configurar AI33','headline':HEADLINE,'segmentos_provisionales':segments},ensure_ascii=False,indent=2))
bg=Image.open(P/'restaurante.png').convert('RGB').resize((540,540),Image.Resampling.LANCZOS)
base=Image.new('RGB',(W,H),BG);base.paste(bg,(0,215));shade=Image.new('RGBA',(W,H));ds=ImageDraw.Draw(shade)
for y in range(680,790):ds.line((0,y,W,y),fill=(*BG,int(255*(y-680)/110)))
base=Image.alpha_composite(base.convert('RGBA'),shade).convert('RGB')
def center(draw,text,y,f,color=white):draw.text(((W-draw.textlength(text,font=f))/2,y),text,font=f,fill=color)
def wrap(text,f,width):
 lines=[];line=''
 for w in text.split():
  test=(line+' '+w).strip()
  if ImageDraw.Draw(base).textlength(test,font=f)>width and line:lines.append(line);line=w
  else:line=test
 if line:lines.append(line)
 return lines
def frame(t):
 im=base.copy();d=ImageDraw.Draw(im);sg=next(s for s in segments if s[0]<=t<s[1]);start,end,spoken,title=sg
 d.rounded_rectangle((40,122,480,150),radius=7,fill=(26,37,54));center(d,HEADLINE,126,font(21),yellow)
 f=font(38 if len(title)<22 else 32);center(d,title,164,f)
 # Identidad constante de ambas partes.
 for x,c,label in [(42,blue,'A · CLIENTE'),(302,red,'B · RESTAURANTE')]:
  d.rounded_rectangle((x,275,x+192,306),radius=6,fill=c);d.text((x+10,282),label,font=font(18),fill=white)
 if t<9 or 29<=t<51:
  # Ticket como objeto protagonista, deslizado en 7 cuadros.
  u=min(1,(t-start)*FPS/7);off=int((1-(1-(1-u)**3))*30)
  x0,y0=135,350+off
  d.rounded_rectangle((x0+5,y0+8,x0+275,y0+248),radius=8,fill=(1,4,8))
  d.rounded_rectangle((x0,y0,x0+270,y0+240),radius=8,fill=white)
  center(d,'CUENTA',y0+15,font(25),BG)
  for yy,txt in [(65,'Consumo         $500'),(105,'Propina 15 %     $75'),(185,'TOTAL           $575')]:
   if t>=42 and t<51 and yy==105:txt='Propina          $0'
   if t>=42 and t<51 and yy==185:txt='TOTAL           $500'
   d.text((x0+19,y0+yy),txt,font=mono(15),fill=BG)
  d.line((x0+18,y0+163,x0+252,y0+163),fill=(150,145,130),width=2)
  if (3<=t<9 or 29<=t<42):d.rounded_rectangle((x0+10,y0+97,x0+260,y0+135),radius=5,outline=red,width=3)
 if 20<=t<29 or t>=58:
  d.rounded_rectangle((44,468,496,625),radius=15,fill=BG)
  if 23<=t<26:center(d,str(3-int(t-23)),475,font(95),yellow)
  elif 26<=t<29:
   d.rounded_rectangle((62,485,478,605),radius=7,outline=blue,width=4);center(d,'CLIENTE A',490,font(48),blue);center(d,'COBRO NO AUTORIZADO',548,font(23),white)
  else:
   center(d,'TU VOTO',480,font(23),yellow)
   for x,c,txt in [(60,blue,'A · CLIENTE'),(282,red,'B · LOCAL')]:
    d.rounded_rectangle((x,533,x+198,588),radius=8,fill=c);d.text((x+15,547),txt,font=font(24),fill=white)
 if 51<=t<58:
  d.rounded_rectangle((80,490,460,595),radius=10,fill=BG);center(d,'¿AGREGAMOS PROPINA?',508,font(28),yellow)
  center(d,'EL CLIENTE: «SÍ»' if t>=55 else 'PRIMERO PREGUNTAN',553,font(25),blue)
 # Subtítulos completos provisionales, en zona segura.
 d.rectangle((0,650,540,960),fill=BG)
 for i,line in enumerate(wrap(spoken,font(23),438)):center(d,line,660+i*26,font(23))
 center(d,'CASO ILUSTRATIVO · INFORMACIÓN GENERAL',880,mono(9),(146,155,171))
 center(d,'PRUEBA VISUAL · NARRACIÓN AI33 PENDIENTE',902,mono(9),yellow)
 d.rectangle((40,935,500,938),fill=(35,45,62));d.rectangle((40,935,40+int(460*t/D),938),fill=yellow)
 return im
cmd=['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(P/'Propina_Mexico_Prueba_Visual.mp4')]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for n in range(D*FPS):p.stdin.write(frame(n/FPS).tobytes())
p.stdin.close();assert p.wait()==0
sheet=Image.new('RGB',(540*3,960*2))
for i,t in enumerate([2,7,21,24,31,56]):sheet.paste(frame(t),(i%3*540,i//3*960))
sheet.resize((1080,1280)).save(P/'revision_visual.jpg',quality=92)
(P/'fuentes.md').write_text('''# Propina obligatoria — México
Caso ficticio ilustrativo; cantidades de ejemplo: consumo $500 MXN y propina del 15 % ($75 MXN).
Guion aprobado por el usuario. Tiempos de la prueba visual provisionales; falta voz AI33 y alineación real.

Fuentes consultadas el 12 de noviembre de 2026:
- Profeco, 10 de mayo de 2026: https://www.gob.mx/profeco/prensa/la-profeco-recuerda-a-las-y-los-consumidores-que-la-propina-es-voluntaria?idiom=es-MX
- Profeco, 15 de febrero de 2026: https://www.gob.mx/profeco/prensa/profeco-recuerda-a-la-poblacion-consumidora-sus-derechos-en-restaurantes-y-bares?state=published
- Ley Federal de Protección al Consumidor, artículo 10: https://www.diputados.gob.mx/LeyesBiblio/pdf/LFPC.pdf

La propina es voluntaria; no puede exigirse ni agregarse sin consentimiento. El cierre sobre gratitud o presión es un dilema moral.
''')
print('Prueba visual creada: 66 s, 1080x1920, 30 fps, sin audio.')
