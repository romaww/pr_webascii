import sys
from PIL import Image, ImageDraw, ImageFont

# Проверка аргументов
if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} <image_path> <ascii_width>")
    sys.exit(1)

path = sys.argv[1]
try:
    cols = int(sys.argv[2])
except ValueError:
    print("ascii_width должен быть целым числом")
    sys.exit(1)

# Символы ASCII
GRAYS = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnqkzjme wWcCgGAaPpSmMboxerErmQLapvVuTsxXwWZ@"
n = len(GRAYS)

# Загружаем шрифт (можно заменить на TTF, если нужно)
font = ImageFont.truetype("DejaVuSansMono.ttf", 15)

# Получение размеров символа с помощью getbbox()
bbox = font.getbbox("A")
char_w = bbox[2] - bbox[0]
char_h = bbox[3] - bbox[1]

# Загрузка изображения
img = Image.open(path)
W, H = img.size
aspect_ratio = H / W

# Рассчитываем количество строк
rows = int((aspect_ratio * cols) * (char_h / char_w))

# Масштабируем и переводим в градации серого
img = img.resize((cols, rows))
img = img.convert("L")  # grayscale

# Преобразуем каждый пиксель в ASCII-символ
pixels = img.getdata()
# Неинвертированные цвета
chars = [GRAYS[pixel * (n - 1) // 255] for pixel in pixels]
# Инвертироавнные цвета
#chars = [GRAYS[(255 - pixel) * (n - 1) // 255] for pixel in pixels]
ascii_lines = ["".join(chars[i:i + cols]) for i in range(0, len(chars), cols)]

# Создаем новое изображение для ASCII-арта
out_w = char_w * cols
out_h = char_h * rows
#output_image = Image.new("RGB", (out_w, out_h), color="white")
output_image = Image.new("RGB", (out_w, out_h), color="black")
draw = ImageDraw.Draw(output_image)

# Рисуем ASCII строки на изображении
y = 0
for line in ascii_lines:
    #draw.text((0, y), line, font=font, fill="black")
    draw.text((0, y), line, font=font, fill="white")
    y += char_h

# Сохраняем результат
output_image.save("ascii_output.jpg", "JPEG")
print("ASCII art saved to ascii_output.jpg")
