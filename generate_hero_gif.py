import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_hero_gif(output_path, num_frames=40, width=1200, height=380, fps=12):
    random.seed(1337)
    
    font_paths = {
        "title": "C:/Windows/Fonts/segoeuib.ttf",
        "sub_bold": "C:/Windows/Fonts/segoeuib.ttf",
        "sub": "C:/Windows/Fonts/segoeui.ttf",
        "mono": "C:/Windows/Fonts/consola.ttf",
        "mono_bold": "C:/Windows/Fonts/consolab.ttf",
    }
    
    f_title = ImageFont.truetype(font_paths["title"], 44)
    f_name = ImageFont.truetype(font_paths["sub_bold"], 14)
    f_desc = ImageFont.truetype(font_paths["mono"], 11)
    f_hud = ImageFont.truetype(font_paths["mono"], 10)
    f_hud_bold = ImageFont.truetype(font_paths["mono_bold"], 10)
    
    logo_path = "c:/Users/niroin/Documents/project/niro1n/assets/logo/niroin-logo-white.png"
    if not os.path.exists(logo_path):
        logo_path = "C:/Users/niroin/Documents/project/niro1n-porto/public/images/logo/niroin-logo(white).png"
    
    raw_logo = Image.open(logo_path).convert("RGBA")
    logo_size = 68
    logo_resized = raw_logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    
    particles = []
    for _ in range(24):
        particles.append({
            "x": random.uniform(50, width - 50),
            "y": random.uniform(40, height - 40),
            "vx": random.uniform(-16, 16),
            "vy": random.uniform(-8, 8),
            "radius": random.uniform(1.0, 1.8),
            "base_alpha": random.uniform(30, 80),
            "pulse_speed": random.choice([1, 2]),
            "pulse_offset": random.uniform(0, math.pi * 2)
        })
        
    frames = []
    
    margin_x, margin_y = 35, 25
    frame_w = width - margin_x * 2
    frame_h = height - margin_y * 2
    bracket_len = 16
    
    text_box = (width // 2 - 360, 45, width // 2 + 360, 285)
    top_hud_y_range = (margin_y + 4, margin_y + 26)
    bot_hud_y_range = (margin_y + frame_h - 28, margin_y + frame_h - 4)
    
    for frame_idx in range(num_frames):
        t = frame_idx / num_frames
        t_rad = t * 2 * math.pi
        
        img = Image.new("RGBA", (width, height), (8, 8, 8, 255))
        
        glow_radius = 240 + int(30 * math.sin(t_rad))
        glow_alpha = int(16 + 6 * math.sin(t_rad))
        glow_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_overlay)
        center_x, center_y = width // 2, 160
        glow_draw.ellipse(
            (center_x - glow_radius, center_y - glow_radius,
             center_x + glow_radius, center_y + glow_radius),
            fill=(255, 255, 255, glow_alpha)
        )
        glow_overlay = glow_overlay.filter(ImageFilter.GaussianBlur(glow_radius // 2))
        img = Image.alpha_composite(img, glow_overlay)
        draw = ImageDraw.Draw(img)
        
        grid_step = 36
        for gx in range(margin_x + 14, margin_x + frame_w - 14, grid_step):
            for gy in range(margin_y + 14, margin_y + frame_h - 14, grid_step):
                if (text_box[0] < gx < text_box[1] and text_box[2] < gy < text_box[3]) or \
                   (top_hud_y_range[0] <= gy <= top_hud_y_range[1]) or \
                   (bot_hud_y_range[0] <= gy <= bot_hud_y_range[1]):
                    continue
                draw.point((gx, gy), fill=(255, 255, 255, 22))
                
        for p in particles:
            px = (p["x"] + p["vx"] * t) % (width - 100) + 50
            py = (p["y"] + p["vy"] * t) % (height - 80) + 40
            if (text_box[0] < px < text_box[1] and text_box[2] < py < text_box[3]) or \
               (top_hud_y_range[0] <= py <= top_hud_y_range[1]) or \
               (bot_hud_y_range[0] <= py <= bot_hud_y_range[1]):
                continue
            p_alpha = int(p["base_alpha"] * (0.6 + 0.4 * math.sin(t_rad * p["pulse_speed"] + p["pulse_offset"])))
            r = p["radius"]
            draw.ellipse((px - r, py - r, px + r, py + r), fill=(255, 255, 255, p_alpha))
            
        scan_y = int((t * (frame_h + 80)) + margin_y - 40)
        if margin_y <= scan_y <= margin_y + frame_h:
            scan_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            scan_draw = ImageDraw.Draw(scan_overlay)
            scan_draw.line([(margin_x + 10, scan_y), (margin_x + frame_w - 10, scan_y)], fill=(255, 255, 255, 24), width=1)
            scan_draw.line([(margin_x + 20, scan_y - 1), (margin_x + frame_w - 20, scan_y - 1)], fill=(255, 255, 255, 10), width=1)
            scan_draw.line([(margin_x + 20, scan_y + 1), (margin_x + frame_w - 20, scan_y + 1)], fill=(255, 255, 255, 10), width=1)
            img = Image.alpha_composite(img, scan_overlay)
            draw = ImageDraw.Draw(img)
            
        border_alpha = int(24 + 6 * math.cos(t_rad))
        draw.rectangle(
            (margin_x, margin_y, margin_x + frame_w, margin_y + frame_h),
            outline=(255, 255, 255, border_alpha), width=1
        )
        
        c_alpha = 200
        draw.line([(margin_x, margin_y), (margin_x + bracket_len, margin_y)], fill=(255, 255, 255, c_alpha), width=2)
        draw.line([(margin_x, margin_y), (margin_x, margin_y + bracket_len)], fill=(255, 255, 255, c_alpha), width=2)
        draw.line([(margin_x + frame_w, margin_y), (margin_x + frame_w - bracket_len, margin_y)], fill=(255, 255, 255, c_alpha), width=2)
        draw.line([(margin_x + frame_w, margin_y), (margin_x + frame_w, margin_y + bracket_len)], fill=(255, 255, 255, c_alpha), width=2)
        draw.line([(margin_x, margin_y + frame_h), (margin_x + bracket_len, margin_y + frame_h)], fill=(255, 255, 255, c_alpha), width=2)
        draw.line([(margin_x, margin_y + frame_h), (margin_x, margin_y + frame_h - bracket_len)], fill=(255, 255, 255, c_alpha), width=2)
        draw.line([(margin_x + frame_w, margin_y + frame_h), (margin_x + frame_w - bracket_len, margin_y + frame_h)], fill=(255, 255, 255, c_alpha), width=2)
        draw.line([(margin_x + frame_w, margin_y + frame_h), (margin_x + frame_w, margin_y + bracket_len)], fill=(255, 255, 255, c_alpha), width=2)
        
        hud_y = margin_y + 12
        draw.text((margin_x + 16, hud_y), "NIROIN // DIGITAL IDENTITY", font=f_hud_bold, fill=(220, 220, 220, 230))
        draw.text((margin_x + 192, hud_y), "/ 01", font=f_hud, fill=(125, 125, 130, 190))
        
        coord_text = "LAT. 8.6705° S  •  LONG. 115.2126° E  •  INDONESIA"
        coord_bbox = draw.textbbox((0, 0), coord_text, font=f_hud)
        coord_w = coord_bbox[2] - coord_bbox[0]
        draw.text(((width - coord_w) // 2, hud_y), coord_text, font=f_hud, fill=(140, 140, 145, 200))
        
        status_text = "SYS.ONLINE"
        status_bbox = draw.textbbox((0, 0), status_text, font=f_hud_bold)
        status_w = status_bbox[2] - status_bbox[0]
        dot_x = margin_x + frame_w - status_w - 30
        dot_y = hud_y + 3
        dot_alpha = int(170 + 85 * math.sin(t_rad * 2))
        draw.ellipse((dot_x, dot_y, dot_x + 5, dot_y + 5), fill=(255, 255, 255, dot_alpha))
        draw.text((dot_x + 12, hud_y), status_text, font=f_hud_bold, fill=(245, 245, 245, 240))
        
        logo_y_float = 60 + 2.0 * math.sin(t_rad)
        logo_x = (width - logo_size) // 2
        logo_y = int(logo_y_float)
        
        logo_glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        lg_draw = ImageDraw.Draw(logo_glow)
        lg_draw.ellipse(
            (logo_x - 12, logo_y - 12, logo_x + logo_size + 12, logo_y + logo_size + 12),
            fill=(255, 255, 255, int(40 + 18 * math.sin(t_rad)))
        )
        logo_glow = logo_glow.filter(ImageFilter.GaussianBlur(14))
        img = Image.alpha_composite(img, logo_glow)
        img.paste(logo_resized, (logo_x, logo_y), logo_resized)
        draw = ImageDraw.Draw(img)
        
        title_str = "N  I  R  O  I  N"
        title_bbox = draw.textbbox((0, 0), title_str, font=f_title)
        title_w = title_bbox[2] - title_bbox[0]
        title_x = (width - title_w) // 2
        title_y = 142
        draw.text((title_x, title_y), title_str, font=f_title, fill=(255, 255, 255, 255))
        
        name_str = "S Y A H F R I N O   R E Z K Y   O K T A V I A N T"
        name_bbox = draw.textbbox((0, 0), name_str, font=f_name)
        name_w = name_bbox[2] - name_bbox[0]
        name_x = (width - name_w) // 2
        name_y = 208
        draw.text((name_x, name_y), name_str, font=f_name, fill=(225, 225, 230, 245))
        
        desc_str = "SOFTWARE DEVELOPER  •  SYSTEMS & DIGITAL EXPERIENCES"
        desc_bbox = draw.textbbox((0, 0), desc_str, font=f_desc)
        desc_w = desc_bbox[2] - desc_bbox[0]
        desc_x = (width - desc_w) // 2
        desc_y = 240
        draw.text((desc_x, desc_y), desc_str, font=f_desc, fill=(160, 160, 165, 220))
        
        sep_w = 200 + int(24 * math.sin(t_rad))
        sep_x1 = (width - sep_w) // 2
        sep_x2 = sep_x1 + sep_w
        sep_y = 270
        draw.line([(sep_x1, sep_y), (sep_x2, sep_y)], fill=(255, 255, 255, 50), width=1)
        draw.point((sep_x1 - 4, sep_y), fill=(255, 255, 255, 140))
        draw.point((sep_x2 + 4, sep_y), fill=(255, 255, 255, 140))
        
        b_hud_y = margin_y + frame_h - 22
        draw.text((margin_x + 16, b_hud_y), "STAGE 01 // HERO", font=f_hud, fill=(130, 130, 135, 190))
        
        b_mid_text = "[ LEARN • BUILD • SOLVE • REPEAT ]"
        b_mid_bbox = draw.textbbox((0, 0), b_mid_text, font=f_hud)
        b_mid_w = b_mid_bbox[2] - b_mid_bbox[0]
        draw.text(((width - b_mid_w) // 2, b_hud_y), b_mid_text, font=f_hud, fill=(175, 175, 180, 230))
        
        b_right_text = "NIROIN.SYSTEM // 2026"
        b_right_bbox = draw.textbbox((0, 0), b_right_text, font=f_hud)
        b_right_w = b_right_bbox[2] - b_right_bbox[0]
        draw.text((margin_x + frame_w - b_right_w - 16, b_hud_y), b_right_text, font=f_hud, fill=(130, 130, 135, 190))
        
        frame_rgb = img.convert("RGB")
        frame_p = frame_rgb.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
        frames.append(frame_p)
        
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    frame_duration = int(1000 / fps)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=frame_duration,
        loop=0,
        optimize=True
    )

if __name__ == "__main__":
    create_hero_gif("c:/Users/niroin/Documents/project/niro1n/assets/niroin-hero.gif", num_frames=36, fps=12)
    create_hero_gif("c:/Users/niroin/Documents/project/niro1n/.github/assets/niroin-hero.gif", num_frames=36, fps=12)
