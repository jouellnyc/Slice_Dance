# K10 Slice Dance Animation
# Adapted from Waveshare RP2350 script for UNIHIKER K10
from unihiker_k10 import screen
import lvgl as lv
import time

LCD_WIDTH = 240
LCD_HEIGHT = 320
NUM_SLICES = 20
ANIMATION_SPEED = 20
SLIDE_DISTANCE = 100

def load_map_data(module_base_name):
    module = __import__(module_base_name)
    data_var_name = module_base_name
    prefix = module_base_name.replace('_data', '')
    width_var_name = f"{prefix}_width"
    height_var_name = f"{prefix}_height"
    map_data = getattr(module, data_var_name)
    map_width = getattr(module, width_var_name)
    map_height = getattr(module, height_var_name)
    return map_data, map_width, map_height

class SliceAnimation:
    def __init__(self, map_data, map_width, map_height, scr):
        self.map_data = map_data
        self.map_width = map_width
        self.map_height = map_height
        self.scr = scr
        self.slice_height = map_height // NUM_SLICES
        self.slices = []
        self.create_slices()

    def create_slices(self):
        bytes_per_pixel = 2
        row_bytes = self.map_width * bytes_per_pixel

        for i in range(NUM_SLICES):
            slice_y = i * self.slice_height
            if slice_y + self.slice_height > self.map_height:
                actual_height = self.map_height - slice_y
            else:
                actual_height = self.slice_height

            start_byte = slice_y * row_bytes
            end_byte = start_byte + (actual_height * row_bytes)
            slice_data = self.map_data[start_byte:end_byte]

            img_dsc = lv.image_dsc_t(
                dict(
                    header=dict(cf=lv.COLOR_FORMAT.RGB565, w=self.map_width, h=actual_height),
                    data_size=len(slice_data),
                    data=slice_data
                )
            )

            img = lv.image(self.scr)
            img.set_src(img_dsc)

            final_y = (LCD_HEIGHT - self.map_height) // 2 + slice_y
            if i % 2 == 0:
                start_x = -self.map_width - SLIDE_DISTANCE
            else:
                start_x = LCD_WIDTH + SLIDE_DISTANCE
            final_x = (LCD_WIDTH - self.map_width) // 2

            img.set_pos(start_x, final_y)
            self.slices.append({'img': img, 'start_x': start_x, 'final_x': final_x, 'y': final_y, 'index': i})

    def reset_positions(self):
        for slice_info in self.slices:
            slice_info['img'].set_pos(slice_info['start_x'], slice_info['y'])

    def animate_slide(self):
        steps = 40
        for step in range(steps + 1):
            progress = step / steps
            eased = 1 - (1 - progress) ** 3
            for slice_info in self.slices:
                start_x = slice_info['start_x']
                final_x = slice_info['final_x']
                current_x = int(start_x + (final_x - start_x) * eased)
                slice_info['img'].set_pos(current_x, slice_info['y'])
            time.sleep_ms(ANIMATION_SPEED)
        print("Slide complete!")

    def animate_cascade(self):
        steps_per_slice = 20
        for slice_info in self.slices:
            for step in range(steps_per_slice + 1):
                progress = step / steps_per_slice
                eased = 1 - (1 - progress) ** 3
                start_x = slice_info['start_x']
                final_x = slice_info['final_x']
                current_x = int(start_x + (final_x - start_x) * eased)
                slice_info['img'].set_pos(current_x, slice_info['y'])
                time.sleep_ms(ANIMATION_SPEED // 2)
        print("Cascade complete!")

    def animate_zoom(self):
        steps = 40
        center_x = LCD_WIDTH // 2
        for step in range(steps + 1):
            progress = step / steps
            eased = 1 - (1 - progress) ** 3
            for slice_info in self.slices:
                scale = 0.1 + (0.9 * eased)
                final_x = slice_info['final_x']
                offset = int((center_x - final_x - self.map_width // 2) * (1 - scale))
                current_x = final_x + offset
                slice_info['img'].set_pos(current_x, slice_info['y'])
            time.sleep_ms(ANIMATION_SPEED)
        print("Zoom complete!")

    def animate_bounce(self):
        import math
        steps = 60
        for step in range(steps + 1):
            progress = step / steps
            for slice_info in self.slices:
                if progress < 0.8:
                    eased = progress / 0.8
                    bounce = math.sin(eased * 3.14159) * 0.2
                    y_progress = eased + bounce
                else:
                    settle = (progress - 0.8) / 0.2
                    y_progress = 1.0 + (math.cos(settle * 6.28) * 0.05 * (1 - settle))
                start_y = -self.slice_height * 2
                final_y = slice_info['y']
                current_y = int(start_y + (final_y - start_y) * y_progress)
                x_eased = 1 - (1 - progress) ** 3
                start_x = slice_info['start_x']
                final_x = slice_info['final_x']
                current_x = int(start_x + (final_x - start_x) * x_eased)
                slice_info['img'].set_pos(current_x, current_y)
            time.sleep_ms(ANIMATION_SPEED)
        print("Bounce complete!")

    def animate_explode(self):
        import math
        total_steps = 80
        explode_end = 30
        pause_steps = 8
        for step in range(total_steps + 1):
            if step <= explode_end:
                progress = step / explode_end
                eased = progress ** 2
                direction = 1
            elif step <= explode_end + pause_steps:
                eased = 1.0
                direction = 1
            else:
                reassemble_progress = (step - explode_end - pause_steps) / (total_steps - explode_end - pause_steps)
                eased = 1.0 - (1 - (1 - reassemble_progress) ** 3)
                direction = -1

            for slice_info in self.slices:
                i = slice_info['index']
                explosion_progress = eased if direction == 1 else (1.0 - eased)
                center_x = LCD_WIDTH // 2
                center_y = LCD_HEIGHT // 2
                slice_center_x = slice_info['final_x'] + self.map_width // 2
                slice_center_y = slice_info['y'] + self.slice_height // 2
                dx = slice_center_x - center_x
                dy = slice_center_y - center_y
                distance = math.sqrt(dx*dx + dy*dy)
                if distance > 0:
                    explosion_distance = 250 * explosion_progress
                    offset_x = int((dx / distance) * explosion_distance)
                    offset_y = int((dy / distance) * explosion_distance)
                else:
                    offset_x = 0
                    offset_y = 0
                current_x = slice_info['final_x'] + offset_x
                current_y = slice_info['y'] + offset_y
                slice_info['img'].set_pos(current_x, current_y)
            time.sleep_ms(ANIMATION_SPEED // 2)
        print("Explode complete!")


# ===== MAIN =====
if __name__ == 'kd':
    DESIRED_MAP_FILE = 'cat'  # change to your image data module name

    screen.init()
    scr = screen.__dict__['screen']

    map_data, map_width, map_height = load_map_data(DESIRED_MAP_FILE)
    anim = SliceAnimation(map_data, map_width, map_height, scr)

    styles = ['slide', 'cascade', 'zoom', 'bounce', 'explode']

    try:
        while True:
            for style in styles:
                print(f"> {style.upper()}")
                anim.reset_positions()
                getattr(anim, f'animate_{style}')()
                time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped")