def draw_text(surface, text, font, color, x, y, max_width, line_spacing=5, padding=40):
    lines = wrap_text(text, font, max_width - 2 * padding)
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        text_width = text_surface.get_width()
        line_x = int(x + (max_width - text_width) / 2)  # centrowanie w obrębie max_width
        surface.blit(text_surface, (line_x, y + i * (font.get_height() + line_spacing)))

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return lines
