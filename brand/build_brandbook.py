from pathlib import Path
import json, shutil, math
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'brand/assets'
OUT = ROOT / 'output/pdf/BSS-brandbook-v0.2.pdf'
F = ASSETS / 'fonts'
for name, file in [('Body','IBMPlexSans-Regular.ttf'),('Bold','IBMPlexSans-SemiBold.ttf'),('Display','Unbounded-SemiBold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(F/file)))
for src, dest in [('/Users/ak/Downloads/photo_2026-09-15 20.41.55.jpeg','logo-dark-reference.jpeg'),('/Users/ak/Downloads/photo_2026-09-15 20.40.47.jpeg','logo-light-reference.jpeg')]:
    shutil.copy2(src,ASSETS/dest)

C={'black':'#080A0D','panel':'#15191F','white':'#F4F6F8','silver':'#B6BEC9','muted':'#8993A0','line':'#343C48','blue':'#73B7FF','ink':'#101318','error':'#FF8C94','success':'#91D4B0'}
W,H=960,600
c=canvas.Canvas(str(OUT),pagesize=(W,H))
c.setTitle('BSS / Soft BMW Service Lviv / Брендбук v0.2')
c.setAuthor('BSS - concept developed with Codex')
notes=[]; n=0; light=False; checks=[]
def rect(x,y,w,h,col,stroke=None):
    c.setFillColor(HexColor(C.get(col,col)))
    if stroke: c.setStrokeColor(HexColor(C.get(stroke,stroke)))
    c.rect(x,H-y-h,w,h,fill=1,stroke=bool(stroke))
def line(x,y,x2,y2,col='line',width=.7):
    c.setStrokeColor(HexColor(C.get(col,col))); c.setLineWidth(width); c.line(x,H-y,x2,H-y2)
def text(s,x,y,size=14,font='Body',col=None,max_width=None):
    col=col or ('ink' if light else 'white')
    tracking=-.025 if font=='Display' else 0
    width=pdfmetrics.stringWidth(s,font,size)+max(0,len(s)-1)*tracking*size
    if max_width and width>max_width:
        size*=max_width/width
        width=max_width
    c.saveState()
    c.setFillColor(HexColor(C.get(col,col)))
    obj=c.beginText(x,H-y-size*.8)
    obj.setFont(font,size);obj.setCharSpace(tracking*size);obj.textOut(s);c.drawText(obj)
    c.restoreState()
    notes.append(s)
    checks.append((n,s,x,y,width,size))
def para(s,x,y,w,size=14,col=None,font='Body',leading=None):
    col=col or ('ink' if light else 'silver')
    st=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.45,textColor=HexColor(C.get(col,col)))
    p=Paragraph(escape(s).replace('\n','<br/>'),st); pw,ph=p.wrap(w,600)
    p.drawOn(c,x,H-y-ph); notes.append(s); checks.append((n,s,x,y,w,ph)); return ph
def img(path,x,y,w,h):
    c.drawImage(str(path),x,H-y-h,w,h,preserveAspectRatio=True,anchor='c',mask='auto')
def tag(s,x,y): text(s,x,y,10,'Bold','muted')
def page(k,title,sub='',islight=False):
    global n,light
    if n:c.showPage()
    n+=1;light=islight;notes.append('\n## '+str(n)+'. '+title+'\n')
    rect(0,0,W,H,'white' if light else 'black')
    tag('BSS  /  SOFT BMW SERVICE  /  LVIV',48,28)
    text(k.upper(),650,28,10,'Bold','muted')
    line(48,51,912,51)
    text(title,48,78,34,'Display',max_width=864)
    if sub:para(sub,48,130,820,13)
    line(48,555,912,555)
    tag('BRAND SYSTEM  /  CONCEPT V0.2  /  15.09.2026',48,569)
    text(f'{n:02}',883,567,13,'Bold','muted')
def block(num,title,body,x,y,w=255):
    text(num,x,y,12,'Bold','blue' if not light else 'muted')
    text(title,x,y+27,20,'Display',max_width=w)
    para(body,x,y+64,w,14)

page('01 / foundation','Точність має характер.')
tag('БРЕНДБУК / ПЕРША КОНЦЕПЦІЯ',48,157)
text('BSS',48,209,100,'Display',max_width=420)
para('Спеціалізований сервіс BMW у Львові.\nМінімалізм. Інженерна ясність.\nВідчуття повного контролю.',48,337,420,21,col='white')
img(ASSETS/'logo-dark-reference.jpeg',505,135,407,321)
rect(48,507,80,3,'blue');tag('АЙДЕНТИКА  /  ЦИФРОВЕ СЕРЕДОВИЩЕ  /  РУХ',147,503)

page('02 / direction','Характер бренду','Робочий напрям: Precision in Motion / Точність у русі.')
block('01 / РЕКОМЕНДОВАНО','Precision in Motion','Графіт, срібло, холодний синій. Спокійна композиція й точна реакція на дію. Баланс преміальності та ігрового відчуття.',48,199)
block('02 / АЛЬТЕРНАТИВА','Pure Monochrome','Чорний, білий і метал. Максимально стриманий образ; активні стани доведеться виразніше позначати формою та контрастом.',350,199)
block('03 / АЛЬТЕРНАТИВА','Track Interface','Щільніші панелі, спортивні підписи та сильніший акцент. Більше енергії Forza; менше вільного простору й тиші.',652,199)
line(48,417,912,417)
para('Обіцянка бренду: увага до деталей вашого BMW.\nХарактер: зібраний, компетентний, прямий. Дорогий вигляд створюють пропорції, матеріали та послідовність.',48,447,814,18,col='white')

page('03 / references','Що беремо з референсів','Зображення користувача слугують візуальними прикладами, а не інструкціями до виконання.')
base=Path('/var/folders/gd/8tpqvyl56wq7nz7m7syw8kg40000gn/T')
refs=[('codex-clipboard-5c9c3cbb-5d91-4a85-a015-0460d23a381c.png','ПАНЕЛІ','Модульна сітка, різний масштаб карток, чітка ієрархія.'),('codex-clipboard-a614f99a-a1c2-481e-afe9-b5d2ce3d1ea1.png','АКТИВНИЙ СТАН','Вибір помітний завдяки контуру, контрасту й невеликому підйому.'),('codex-clipboard-e0dbcf5c-925d-4780-a618-30a4a4cf1f60.png','ТЕХНІЧНІ ДАНІ','Рівні колонки, короткі підписи та точне вирівнювання чисел.')]
for i,(p,t,b) in enumerate(refs):
    x=48+i*296; img(base/p,x,187,272,155);tag(t,x,365);para(b,x,393,263,14)
para('Pear.no: повноекранна фонова сцена та зміна композиції при скролінгу. Для BSS пропонуємо автомобільні деталі, рух світла й повільне зміщення перспективи. Кольори BSS визначає власна палітра.',48,472,850,14)
c.linkURL('https://pear.no/',(48,H-534,912,H-471),relative=0)

page('04 / identity','Логотип: дві подачі','BSS / SOFT BMW SERVICE / LVIV. Назву та композицію беремо з наданих зображень.')
img(ASSETS/'logo-dark-reference.jpeg',48,181,415,280)
img(ASSETS/'logo-light-reference.jpeg',489,181,423,280)
tag('01 / ТЕМНА: САЙТ, ОБКЛАДИНКИ, ВИВІСКА',48,477)
tag('02 / СВІТЛА: ДОКУМЕНТИ, СВІТЛІ НОСІЇ',489,477)
para('Надані JPEG використані без перемальовування. Це референси, а не готові векторні майстер-файли для друку та вебу.',48,506,850,13)

page('05 / identity rules','Простір навколо знака','Попередні правила системи. Фінальні розміри перевіряються після підготовки векторного оригіналу.')
rect(48,188,475,314,'panel')
c.setDash(4,4);line(85,225,487,225,'muted');line(85,460,487,460,'muted');line(85,225,85,460,'muted');line(487,225,487,460,'muted');c.setDash()
text('BSS',132,283,94,'Display',max_width=310);tag('СХЕМА ПРОПОРЦІЙ, НЕ МАЙСТЕР-ЛОГОТИП',92,421)
tag('X = 1/4 ВИСОТИ МОНОГРАМИ BSS',91,205)
para('Охоронне поле: щонайменше X з усіх боків видимого знака, без урахування полів JPEG.\n\nПовний логотип: орієнтир від 220 px / 45 мм за шириною видимого блоку. На малих носіях потрібна окрема монограма.\n\nЗберігати пропорції. Не змінювати відстані між літерами та рядками. Не додавати контури, тіні, неонове сяйво чи нові емблеми.',563,193,343,15)
para('Потрібні майстер-файли: SVG / PDF; чорна, біла й окрема презентаційна металева версія. Іконку 16-32 px перевіряємо окремо.',563,449,343,13)

page('06 / colour','Графіт. Срібло. Холодне світло.','Синій є запропонованим акцентом BSS. Це власна палітра концепції, а не офіційні кольори BMW.')
swatches=[('black','Carbon','#080A0D'),('panel','Graphite','#15191F'),('white','Porcelain','#F4F6F8'),('silver','Silver','#B6BEC9'),('blue','Ice Blue','#73B7FF')]
for i,(key,name,hx) in enumerate(swatches):
    x=48+i*174;rect(x,188,164,149,key,'line');text(name,x,355,18,'Display',max_width=164);tag(hx,x,386)
para('Орієнтир у темній композиції: 70% темна база, 20% нейтральні панелі й медіа, 8% світла типографіка, 2% сині акценти. Срібний градієнт - лише на великих презентаційних поверхнях.',48,432,529,14)
def luminance(h):
    a=[int(h[i:i+2],16)/255 for i in (1,3,5)];a=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in a];return sum(v*k for v,k in zip(a,[.2126,.7152,.0722]))
def contrast(a,b):
    a,b=sorted([luminance(C[a]),luminance(C[b])]);return (b+.05)/(a+.05)
para(f'Контраст sRGB\nСвітлий текст / Carbon: {contrast("white","black"):.1f}:1\nТемний текст / Ice Blue: {contrast("ink","blue"):.1f}:1\nSilver / Graphite: {contrast("silver","panel"):.1f}:1',624,433,288,13)

page('07 / typography','Типографіка в характері логотипа','Unbounded SemiBold: широкі, низькі пропорції та щільний ритм. IBM Plex Sans: основний текст.',True)
text('ТОЧНІСТЬ.',48,198,66,'Display',max_width=524)
text('У КОЖНІЙ ДЕТАЛІ.',48,282,42,'Display',max_width=524)
para('Сервіс BMW у Львові.\nЗрозуміло про стан автомобіля.\nУважно до кожного рішення.',49,372,465,21,col='ink')
for y,a,b in [(190,'H1 / 56-80 px','Unbounded 600 / 1.1'),(259,'H2 / 32-48 px','Unbounded 600 / 1.15'),(328,'BODY / 16-18 px','Plex Sans 400 / 1.5'),(397,'LABEL / 12-14 px','Plex Sans 600 / 1.3')]:
    tag(a,617,y);text(b,617,y+26,15,'Body','ink')
para('Ґґ Єє Іі Її. Mobile: H1 32-40 px, H2 24-30 px. Tracking заголовків: -0.025em. Природні пропорції шрифту, без штучного стискання. Логотип залишається окремим оригінальним знаком.',48,491,850,13,col='ink')
c.linkURL('https://github.com/googlefonts/unbounded',(616,H-310,912,H-175),relative=0)
c.linkURL('https://github.com/IBM/plex',(616,H-464,912,H-320),relative=0)

page('08 / composition','Дисципліна композиції','Вільний простір працює так само активно, як фотографія чи заголовок.')
for i in range(12):rect(48+i*43,189,35,227,'panel')
rect(48,218,293,113,'white');text('СЕРВІС BMW',64,247,28,'Display','ink',max_width=261);tag('LVIV / BSS',65,296)
rect(349,218,207,113,'blue');text('01 / ДІАГНОСТИКА',365,269,16,'Bold','ink')
line(48,359,556,359,'blue')
para('12 колонок / desktop\n4 колонки / mobile\nСистема відступів: 4, 8, 16, 24, 32, 48, 64, 96\nМіж секціями: 96-160 px / 56-80 px',48,396,505,16,col='white')
para('Прямі краї, радіус 0-4 px. Тонкі розділювачі. Сильний заголовок на одному рівні з великим медіа.\n\nУ секції є одна головна дія. Картки групуються за сенсом. Декоративні технічні мітки мають підпорядкований масштаб.\n\nДіагональ може повторювати зрізи логотипа як малий акцент. Основний текст і сітка залишаються прямими.',617,191,289,15)

page('09 / imagery','Світло показує форму','Артдирекція майбутніх зображень. На цій сторінці описані сцени; нові фотозображення ще не генерувалися.')
block('01 / HERO','Автомобіль у просторі','Темний BMW, ракурс 3/4, графітова студія, довге м’яке джерело світла. Автомобіль справа; 40% чистого простору зліва для заголовка.',48,189)
block('02 / DETAIL','Матеріал зблизька','Фара, метал, гальмівний диск, фактура кузова. Один об’єкт у фокусі; делікатний холодний відблиск, стримана насиченість.',350,189)
block('03 / HUMAN','Робота майстра','Реальні люди, інструменти й процес сервісу. Природний порядок та точний жест. Фото команди й приміщення на сайті мають бути справжніми.',652,189)
line(48,417,912,417)
para('Формати: hero 16:9 + окремий мобільний кадр 4:5; картки 4:3; деталі 1:1. Логотипи й типографіку накладаємо окремо. AI-візуали підходять для атмосферних сцен, але не слугують доказом робіт BSS.',48,440,850,15)
para('Генерація: через доступний інструмент ChatGPT Images. Побажання користувача - GPT Chat Image 2.5; інструмент цієї сесії не надає вибору чи підтвердження такої версії.',48,508,850,11)

page('10 / interface','Ігрове відчуття починається з реакції','Статичні зразки станів для майбутнього UI. Назви послуг тут є прикладами й потребують перевірки бізнесом.')
for i,(name,col,fg) in enumerate([('ЗАПИСАТИСЯ','blue','ink'),('ПЕРЕЛІК ПОСЛУГ','panel','white'),('НАДСИЛАННЯ…','line','silver')]):
    x=48+i*294;rect(x,187,272,48,col);text(name,x+18,202,15,'Bold',fg)
for i,(state,title) in enumerate([('DEFAULT','Діагностика'),('HOVER / FOCUS','Діагностика'),('SELECTED','Діагностика')]):
    x=48+i*294;rect(x,286,272,178,'panel','blue' if i else 'line')
    if i:rect(x,286,272,3,'blue')
    tag(state,x+18,308);text('01',x+18,342,40,'Display','blue' if i else 'silver');text(title,x+18,416,22,'Display',max_width=236)
    if i==2:text('ОБРАНО',x+179,312,10,'Bold','blue')
para('Hover: легкий підйом і світліший контур. Focus: видимий контур 2 px + відступ 4 px. Вибір: контур і текстова позначка. Натискання: коротке зменшення масштабу. На touch вибір доступний одним натисканням.',48,493,850,14)

page('11 / motion','Рух із точним завершенням','Пропоновані параметри. Остаточне відчуття налаштовується на живому прототипі.')
rows=[('Кнопка / hover','140-180 мс','Колір, стрілка +4 px; press scale 0.98.'),('Картка / фокус','180-240 мс','Підйом до 4 px; медіа scale до 1.025.'),('Поява секції','500-650 мс','Opacity + зміщення до 20 px; stagger 50 мс.'),('Перехід між панелями','300-450 мс','Короткий fade і зсув до 16 px.'),('Глибина / pointer','до ±2°','Лише медіа на desktop; текст залишається рівним.'),('Фон / scroll','залежить від скролу','Зміщення до 4% висоти; зміна світла й кадру.')]
for i,(a,b,d) in enumerate(rows):
    y=182+i*47;line(48,y+41,912,y+41);text(a,48,y+10,16,'Bold');text(b,338,y+10,14,'Body','blue');text(d,519,y+10,13)
para('Основна крива: cubic-bezier(0.22, 1, 0.36, 1). В один момент увагу веде один головний рух. Після завершення взаємодії компоненти стабілізуються.',48,481,420,13)
para('Reduced motion: прибрати parallax, tilt і просторові переходи; залишити короткий fade або миттєву зміну. Фон зупиняється поза екраном.',514,481,398,13)

page('12 / loading','Завантаження як короткий вступ','Сайт стає доступним щойно готовий основний контент. Тривалість заставки не додається штучно.')
stages=[('01 / FIRST PAINT','BSS','Готовий статичний фон і логотип. Текст та головна дія вже доступні.'),('02 / MEDIA READY','СВІТЛО','Атмосферна сцена проявляється поверх постера, коли медіа готове.'),('03 / INTERACTIVE','РУХ','Підключається рух фону й реакція карток. Повторний вхід без заставки.')]
for i,(a,b,d) in enumerate(stages):
    x=48+i*296;rect(x,188,272,177,'panel');tag(a,x+18,209);text(b,x+18,270,36,'Display',max_width=236);rect(x+18,334,236,2,'line');rect(x+18,334,70+i*83,2,'blue');para(d,x,393,260,15)
para('Лінії вище - схема переходу між станами. В інтерфейсі числовий прогрес показуємо лише за наявності вимірюваного завантаження. Якщо медіа недоступне, залишається постер. Запис на сервіс працює незалежно від 3D.',48,484,850,14)

page('13 / brand applications','Один характер на різних носіях','Концептуальні приклади композиції. Контактні дані та рекламні твердження не вигадані.')
rect(48,185,400,231,'panel');img(ASSETS/'logo-dark-reference.jpeg',123,199,250,164)
line(70,371,425,371,'line');text('СЕРВІС BMW У ЛЬВОВІ',70,385,13,'Bold')
tag('ВІЗИТІВКА / ЛИЦЬОВИЙ БІК',48,439)
rect(489,185,423,312,'white');img(ASSETS/'logo-light-reference.jpeg',615,193,171,96)
text('СЕРВІСНИЙ ЛИСТ',515,306,24,'Display','ink',max_width=371)
for y,a in [(359,'Автомобіль'),(404,'Узгоджені роботи'),(449,'Наступний крок')]:
    text(a,516,y,13,'Body','ink');line(674,y+15,885,y+15,'silver')
tag('ДОКУМЕНТ / СТРУКТУРА',489,518)
para('Вивіска: великий знак і короткий дескриптор. Одяг: монограма у 1 колір після векторизації. Соцмережі: один кадр, короткий заголовок, один акцент.',48,473,399,13)

page('14 / voice','Говоримо спокійно й конкретно','Українська - основна мова комунікації. Назва в логотипі зберігається у вихідному написанні.',True)
text('Ваш BMW.',48,190,50,'Display',max_width=864)
text('Увага до кожної деталі.',48,262,39,'Display',max_width=864)
para('BSS. Спеціалізований сервіс BMW у Львові.',48,334,815,20,col='ink')
line(48,383,912,383,'silver')
block('01','Заголовки','Короткі й предметні: «Сервіс BMW у Львові». Обіцянка має відповідати реальній роботі.',48,400)
block('02','Кнопки','«Записатися на сервіс», «Переглянути послуги», «Зателефонувати». Дія зрозуміла до натискання.',350,400)
block('03','Підтвердження','Показувати успіх лише після отримання заявки. Помилка пояснює наступний крок і зберігає введені дані.',652,400)

page('15 / digital handoff','Від брендбуку до сайту','Послідовність роботи: брендбук → UI → інтерактивний прототип → анімація та перевірка.')
items=[('01','Перший екран','BMW у сцені, чітка спеціалізація, запис.'),('02','Послуги','Модульні панелі з реальним переліком робіт.'),('03','Підхід до роботи','Зрозумілі кроки від звернення до видачі авто.'),('04','Довіра','Реальні фото, підтверджені кейси та відгуки.'),('05','Запис','Проста форма й зручний контакт телефоном.'),('06','Контакти','Адреса, карта, години роботи після уточнення.')]
for i,(a,b,d) in enumerate(items):
    y=183+i*49;text(a,48,y+8,16,'Bold','blue');text(b,91,y+8,18,'Display',max_width=224);para(d,340,y+8,548,14);line(48,y+42,912,y+42)
para('На mobile: одна колонка, видима головна дія, зони натискання від 44 px; фонові ефекти спрощені. Після реалізації перевіряємо клавіатуру, reduced motion, форму, швидкість і поведінку на touch.',48,496,850,13)

page('16 / next steps','Основа готова до обговорення.','v0.2: оновлено шрифт заголовків за вашим побажанням. Решта системи збережена.')
block('01 / ЗАРАЗ','У цій версії','Позиціонування, логотип і правила, палітра, типографіка, композиція, артдирекція, зразки UI, рух, завантаження та приклади носіїв.',48,189)
block('02 / ДАЛІ','Підготовка матеріалів','Векторний логотип; точна назва та зміст «Soft»; перелік послуг; справжні контакти, фото й докази експертизи. Це вихідні дані для сайту.',350,189)
block('03 / ПІСЛЯ ВИБОРУ','Візуальний прототип','Desktop + mobile головної сторінки. Генерація атмосферних зображень. Потім - налаштування станів, фонової сцени та анімації.',652,189)
line(48,421,912,421)
para('Джерела: два логотипи та шість ігрових зображень користувача; pear.no - референс скролінгу; Unbounded та IBM Plex - шрифти за OFL. BSS представлено як окремий бренд; офіційна афіліація з BMW не заявляється.',48,443,850,13)
text('pear.no',48,512,12,'Bold','blue');c.linkURL('https://pear.no/',(48,72,110,90),relative=0)
text('github.com/IBM/plex',180,512,12,'Bold','blue');c.linkURL('https://github.com/IBM/plex',(180,72,325,90),relative=0)
text('github.com/googlefonts/unbounded',385,512,12,'Bold','blue');c.linkURL('https://github.com/googlefonts/unbounded',(385,72,620,90),relative=0)

c.save()
# A readable companion and tokens keep the proposed system reusable at the next stage.
(ROOT/'brand/BSS-brandbook-v0.2.md').write_text('# BSS / Брендбук v0.2\n\nСтатус: оновлена типографіка для перегляду, 15.09.2026.\n'+'\n\n'.join(notes)+'\n\n## Джерела\n\n- https://pear.no/\n- https://github.com/IBM/plex\n- https://github.com/googlefonts/unbounded\n- Надані користувачем JPEG логотипів та скриншоти Forza.\n',encoding='utf-8')
tokens={'status':'typography-revision-v0.2','colors':C,'fonts':{'heading':'Unbounded','headingWeight':600,'headingLetterSpacing':'-0.025em','body':'IBM Plex Sans'},'spacing':[4,8,16,24,32,48,64,96],'radius':{'card':4,'button':2},'motion':{'microMs':180,'panelMs':350,'revealMs':600,'staggerMs':50,'ease':[.22,1,.36,1],'tiltMaxDeg':2,'parallaxMaxPercent':4,'reducedMotion':'Disable tilt, parallax and spatial transitions; short fade or instant state.'}}
(ROOT/'brand/tokens.json').write_text(json.dumps(tokens,ensure_ascii=False,indent=2)+'\n')
errors=[(p,s[:60],x,y,w,h) for p,s,x,y,w,h in checks if x+w>930 or y+h>553 and y<555]
(ROOT/'tmp/pdfs/layout-check.json').write_text(json.dumps(errors,ensure_ascii=False,indent=2))
print(json.dumps({'pdf':str(OUT),'pages':n,'possible_overflow':errors},ensure_ascii=False,indent=2))
