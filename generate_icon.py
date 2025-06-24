from PIL import Image, ImageDraw

# Crea una nuova immagine quadrata 64x64 con sfondo verde scuro
bg = Image.new('RGBA', (64, 64), '#2a8a2a')
draw = ImageDraw.Draw(bg)

# Parametri manubrio
bar_color = (220, 220, 220, 255)  # grigio chiaro
weight_color = (60, 60, 60, 255) # grigio scuro

# Barre centrali
draw.rectangle([20, 28, 44, 36], fill=bar_color)

# Pesi laterali
# Sinistra
draw.rectangle([12, 24, 20, 40], fill=weight_color)
# Destra
draw.rectangle([44, 24, 52, 40], fill=weight_color)

# Arrotonda i pesi (cerchi alle estremità)
draw.ellipse([8, 24, 16, 40], fill=weight_color)
draw.ellipse([48, 24, 56, 40], fill=weight_color)

# Salva come ICO
bg.save('icon.ico', format='ICO', sizes=[(32,32), (64,64)])
print("Icona stilizzata con manubrio creata!") 