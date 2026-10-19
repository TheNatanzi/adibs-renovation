from PIL import Image, ImageDraw, ImageFont
import math, sys
SRC, OUT = sys.argv[1], sys.argv[2]
PX = 11.25  # px per ft, from survey graphic scale (0–8 ft = 90 px)
im = Image.open(SRC).convert('RGBA')
ov = Image.new('RGBA', im.size, (0,0,0,0)); d = ImageDraw.Draw(ov)
F = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', s)
f = lambda s: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', s)
BLUE=(29,78,216); ORANGE=(217,119,6)
def rect(c, ang, L, W):
    a=math.radians(ang); u=(math.cos(a),math.sin(a)); n=(-u[1],u[0])
    hl,hw=L*PX/2,W*PX/2
    return [(c[0]+sx*hl*u[0]+sy*hw*n[0], c[1]+sx*hl*u[1]+sy*hw*n[1]) for sx,sy in ((-1,-1),(1,-1),(1,1),(-1,1))]
def dashed(pts, col, w=5, dash=22, gap=14):
    for i in range(4):
        (x0,y0),(x1,y1)=pts[i],pts[(i+1)%4]; L=math.hypot(x1-x0,y1-y0); t=0
        while t<L:
            t2=min(t+dash,L); d.line([(x0+(x1-x0)*t/L,y0+(y1-y0)*t/L),(x0+(x1-x0)*t2/L,y0+(y1-y0)*t2/L)],fill=col+(255,),width=w); t+=dash+gap
spots = {'A':((1836,702),170.8), 'B':((2602,983),77.3)}
for k,(c,ang) in spots.items():
    p20=rect(c,ang,20,8); d.polygon(p20, fill=BLUE+(70,)); d.line(p20+[p20[0]], fill=BLUE+(255,), width=5)
    dashed(rect(c,ang,40,8), ORANGE)
# labels
d.rounded_rectangle((1560,830,1880,910), 10, fill=(255,255,255,235), outline=(30,30,30,255), width=3)
d.text((1580,842), "A  North mark", font=F(34), fill=(20,20,20,255))
d.rounded_rectangle((2700,1180,3010,1260), 10, fill=(255,255,255,235), outline=(30,30,30,255), width=3)
d.text((2720,1192), "B  East mark", font=F(34), fill=(20,20,20,255))
img = Image.alpha_composite(im, ov)
crop = img.crop((1380,420,3060,1400)).convert('RGB')
cd = ImageDraw.Draw(crop)
# legend + scale bar
x0,y0 = 30, 640
cd.rounded_rectangle((x0-10,y0-10,x0+640,y0+320), 12, fill=(255,255,255), outline=(40,40,40), width=3)
cd.rectangle((x0+10,y0+20,x0+90,y0+52), fill=(190,205,245), outline=BLUE, width=5)
cd.text((x0+110,y0+18), "20 ft container (20′ × 8′)", font=f(30), fill=(20,20,20))
for i in range(0,80,34): cd.line((x0+10+i,y0+90,x0+10+min(i+22,80),y0+90), fill=ORANGE, width=6)
cd.text((x0+110,y0+72), "40 ft container (40′ × 8′)", font=f(30), fill=(20,20,20))
cd.rectangle((x0+10,y0+125,x0+90,y0+155), outline=(220,30,30), width=4)
cd.text((x0+110,y0+120), "Hamed's marks (2023)", font=f(30), fill=(20,20,20))
sb=int(20*PX); cd.rectangle((x0+10,y0+215,x0+10+sb,y0+230), fill=(20,20,20))
cd.rectangle((x0+10+sb//2,y0+215,x0+10+sb,y0+230), fill=(255,255,255), outline=(20,20,20), width=2)
cd.text((x0+5,y0+238), "0", font=f(26), fill=(20,20,20)); cd.text((x0+sb-10,y0+238), "20 ft", font=f(26), fill=(20,20,20))
cd.text((x0+10,y0+275), "Drawn to survey scale · centered on each mark", font=f(24), fill=(80,80,80))
crop.save(OUT, quality=90)
print(crop.size)
